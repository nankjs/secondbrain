"""
ArXiv 수집 → 원자료 저장 + Vault MD 노트 생성 파이프라인

실행: python3 /home/node/scripts/pipeline-arxiv.py
  - 원자료: /vault/data/raw/{date}/arxiv.json
  - 노트: /vault/01-literature/{date}-arxiv-{slug}.md
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

VAULT = os.environ.get("OBSIDIAN_VAULT_PATH", "/vault")
ARXIV_API = "https://export.arxiv.org/api/query"
QUERY = "cat:cs.AI OR cat:cs.LG OR cat:cs.CL"
MAX_RESULTS = 8
DAYS_BACK = 14


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s가-힣]", "", text)
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", text.strip()))[:50].lower().strip("-")


def fetch_papers() -> list:
    cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)
    params = {
        "search_query": QUERY,
        "start": 0,
        "max_results": MAX_RESULTS * 3,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = ARXIV_API + "?" + urllib.parse.urlencode(params)

    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            content = r.read().decode("utf-8")
    except Exception as e:
        print(f"[FAIL] ArXiv API: {e}", file=sys.stderr)
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(content)
    papers = []

    for entry in root.findall("atom:entry", ns):
        pub_str = entry.findtext("atom:published", "", ns)
        try:
            published = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
        except Exception:
            continue
        if published < cutoff:
            continue

        arxiv_id = entry.findtext("atom:id", "", ns).split("/abs/")[-1]
        title = entry.findtext("atom:title", "", ns).strip().replace("\n", " ")
        summary = entry.findtext("atom:summary", "", ns).strip().replace("\n", " ")
        authors = [a.findtext("atom:name", "", ns) for a in entry.findall("atom:author", ns)]

        # 카테고리
        cats = [c.get("term", "") for c in entry.findall("atom:category", ns)]

        papers.append({
            "id": arxiv_id,
            "title": title,
            "authors": authors[:3],
            "summary": summary[:800],
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
            "published": published.strftime("%Y-%m-%d"),
            "categories": cats[:3],
        })

        if len(papers) >= MAX_RESULTS:
            break

    return papers


def make_note(paper: dict, today: str) -> str:
    authors_str = ", ".join(paper["authors"]) or "Unknown"
    cats_str = ", ".join(paper["categories"])

    return f"""---
title: "{paper['title'][:80].replace('"', "'")}"
date: {today}
type: "literature"
source: "arxiv"
domain: "academic"
url: "{paper['url']}"
authors: "{authors_str}"
published: "{paper['published']}"
tags: [arxiv, academic, literature]
---

# {paper['title']}

> 출처: ArXiv | 발행: {paper['published']} | 저자: {authors_str}

[PDF]({paper['pdf_url']}) | [Abstract]({paper['url']})

---

## 요약

{paper['summary']}

---

- **카테고리**: {cats_str}
"""


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    vault = Path(VAULT)
    raw_dir = vault / "07-archive" / today
    lit_dir = vault / "01-literature"
    raw_dir.mkdir(parents=True, exist_ok=True)
    lit_dir.mkdir(parents=True, exist_ok=True)

    print("[ArXiv] 논문 수집 중...", file=sys.stderr)
    papers = fetch_papers()

    if not papers:
        print("[ArXiv] 수집된 논문 없음", file=sys.stderr)
        print(json.dumps({"source": "arxiv", "count": 0, "files": []}))
        return

    print(f"[ArXiv] {len(papers)}편 수집", file=sys.stderr)

    # 원자료 저장
    raw_file = raw_dir / "arxiv.json"
    raw_file.write_text(json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ArXiv] 원자료: {raw_file}", file=sys.stderr)

    # MD 노트 생성
    saved = []
    for paper in papers:
        slug = slugify(paper["title"])
        filepath = lit_dir / f"{today}-arxiv-{slug}.md"
        if filepath.exists():
            print(f"  [SKIP] {filepath.name}", file=sys.stderr)
            continue
        filepath.write_text(make_note(paper, today), encoding="utf-8")
        saved.append(str(filepath))
        print(f"  [저장] {filepath.name}", file=sys.stderr)

    result = {"source": "arxiv", "count": len(saved), "files": saved}
    print(json.dumps(result, ensure_ascii=False))
    print(f"[ArXiv] 완료: {len(saved)}개 노트", file=sys.stderr)


if __name__ == "__main__":
    main()
