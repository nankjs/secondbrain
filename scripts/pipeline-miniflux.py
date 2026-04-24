"""
MiniFlux 별표(★) 항목 → 원문 크롤링 → Vault MD 노트 생성 파이프라인

실행: python3 /home/node/scripts/pipeline-miniflux.py
  - starred=true 항목만 수집
  - 원문 URL 크롤링 (trafilatura)
  - 원자료: /vault/07-archive/{date}/miniflux.json
  - 노트: /vault/01-literature/{date}-rss-{slug}.md
"""

import base64
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

VAULT = os.environ.get("OBSIDIAN_VAULT_PATH", "/vault")
MINIFLUX_BASE = os.environ.get("MINIFLUX_BASE", "http://host.docker.internal:8080")
MINIFLUX_USER = os.environ.get("MINIFLUX_ADMIN_USERNAME", "admin")
MINIFLUX_PASS = os.environ.get("MINIFLUX_ADMIN_PASSWORD", "secondbrain2026")
LIMIT = 50

CATEGORY_DOMAIN = {
    "학술": "academic",
    "경제": "economy",
    "기독교": "christian",
}


class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []

    def handle_data(self, data):
        self._parts.append(data)

    def get_text(self):
        return " ".join(self._parts).strip()


def strip_html(html: str) -> str:
    s = _HTMLStripper()
    try:
        s.feed(html or "")
    except Exception:
        pass
    return s.get_text()


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s가-힣]", "", text)
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", text.strip()))[:50].lower().strip("-")


def _auth_header() -> dict:
    cred = base64.b64encode(f"{MINIFLUX_USER}:{MINIFLUX_PASS}".encode()).decode()
    return {"Authorization": f"Basic {cred}"}


def fetch_starred() -> list:
    url = f"{MINIFLUX_BASE}/v1/entries?starred=true&limit={LIMIT}&order=published_at&direction=desc"
    req = urllib.request.Request(url, headers=_auth_header())
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read()).get("entries", [])
    except Exception as e:
        print(f"[FAIL] MiniFlux API: {e}", file=sys.stderr)
        return []


def unstar(entry_id: int) -> None:
    """처리 완료 항목 별표 해제 (재수집 방지)"""
    req = urllib.request.Request(
        f"{MINIFLUX_BASE}/v1/entries/{entry_id}/bookmark",
        data=b"",
        headers=_auth_header(),
        method="PUT"
    )
    try:
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception as e:
        print(f"  [WARN] 별표 해제 실패 {entry_id}: {e}", file=sys.stderr)


def fetch_fulltext(url: str) -> str:
    """trafilatura로 원문 전문 추출"""
    try:
        import trafilatura
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=False,
                no_fallback=False,
            )
            if text and len(text) > 100:
                return text.strip()
    except Exception as e:
        print(f"  [WARN] 크롤링 실패 ({url[:60]}): {e}", file=sys.stderr)
    return ""


def make_note(entry: dict, fulltext: str, today: str) -> str:
    title = entry.get("title", "Untitled").replace('"', "'")
    url = entry.get("url", "")
    feed_title = entry.get("feed", {}).get("title", "RSS")
    published = (entry.get("published_at") or today)[:10]
    category = entry.get("feed", {}).get("category", {}).get("title", "")
    domain = CATEGORY_DOMAIN.get(category, "general")

    if fulltext:
        body = fulltext[:3000]
        content_source = "원문 크롤링"
    else:
        body = strip_html(entry.get("content", ""))[:600]
        content_source = "RSS 요약"

    return f"""---
title: "{title[:80]}"
date: {today}
type: "literature"
source: "rss"
domain: "{domain}"
feed: "{feed_title}"
url: "{url}"
published: "{published}"
content_source: "{content_source}"
tags: [rss, literature, {domain}]
---

# {title}

> 출처: {feed_title} | 발행: {published} | {content_source}

[원문 보기]({url})

---

## 내용

{body}
"""


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    vault = Path(VAULT)
    raw_dir = vault / "07-archive" / today
    lit_dir = vault / "01-literature"
    raw_dir.mkdir(parents=True, exist_ok=True)
    lit_dir.mkdir(parents=True, exist_ok=True)

    print("[MiniFlux] 별표 항목 수집 중...", file=sys.stderr)
    entries = fetch_starred()

    if not entries:
        print("[MiniFlux] 별표 항목 없음", file=sys.stderr)
        print(json.dumps({"source": "miniflux", "count": 0, "files": []}))
        return

    print(f"[MiniFlux] {len(entries)}개 별표 항목 발견", file=sys.stderr)

    raw_file = raw_dir / "miniflux.json"
    raw_file.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[MiniFlux] 원자료: {raw_file}", file=sys.stderr)

    saved = []
    for entry in entries:
        slug = slugify(entry.get("title", "untitled"))
        filepath = lit_dir / f"{today}-rss-{slug}.md"

        if filepath.exists():
            print(f"  [SKIP] 이미 존재: {filepath.name}", file=sys.stderr)
            unstar(entry["id"])
            continue

        url = entry.get("url", "")
        print(f"  [크롤링] {entry.get('title', '')[:50]}", file=sys.stderr)
        fulltext = fetch_fulltext(url) if url else ""

        note = make_note(entry, fulltext, today)
        filepath.write_text(note, encoding="utf-8")
        saved.append(str(filepath))
        label = "전문" if fulltext else "RSS요약"
        print(f"  [저장] {filepath.name} ({label})", file=sys.stderr)

        unstar(entry["id"])

    result = {"source": "miniflux", "count": len(saved), "files": saved}
    print(json.dumps(result, ensure_ascii=False))
    print(f"[MiniFlux] 완료: {len(saved)}개 노트 저장", file=sys.stderr)


if __name__ == "__main__":
    main()
