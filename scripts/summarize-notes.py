"""
DeepSeek V3로 오늘 수집된 노트 요약 재작성

실행: python3 /home/node/scripts/summarize-notes.py
  - 대상: /vault/01-literature/ 중 오늘 날짜 + summarized 태그 없는 노트
  - yfinance ETF 노트는 이미 구조화되어 있으므로 건너뜀
  - 요약 후 frontmatter에 summarized: true 추가
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

VAULT = os.environ.get("OBSIDIAN_VAULT_PATH", "/vault")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"

SYSTEM_PROMPT = """당신은 세컨드브레인 지식 관리 시스템의 요약 에이전트입니다.
주어진 문헌 노트를 읽고 다음 형식으로 한국어 요약 섹션을 작성합니다:

## 핵심 요약
(2~3문장으로 핵심 내용 요약)

## 주요 포인트
- 포인트 1
- 포인트 2
- 포인트 3

## 연결 아이디어
(이 내용과 연결될 수 있는 개념이나 질문 1~2개)

규칙:
- 요약은 반드시 한국어로 작성
- 기술 용어는 영어 병기 가능
- 원본의 ## 내용 섹션을 위 3개 섹션으로 교체
- frontmatter와 메타데이터(출처, 링크 등)는 그대로 유지
- 전체 노트를 반환 (frontmatter 포함)"""


def call_deepseek(note_content: str) -> str:
    if not DEEPSEEK_API_KEY:
        print("[FAIL] DEEPSEEK_API_KEY 없음", file=sys.stderr)
        return ""

    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"다음 노트를 요약해 주세요:\n\n{note_content}"}
        ],
        "max_tokens": 1000,
        "temperature": 0.3,
    }).encode("utf-8")

    req = urllib.request.Request(
        DEEPSEEK_API,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            result = json.loads(r.read())
            return result["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  [FAIL] DeepSeek HTTP {e.code}: {body[:200]}", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"  [FAIL] DeepSeek 오류: {e}", file=sys.stderr)
        return ""


def already_summarized(content: str) -> bool:
    return bool(re.search(r"^summarized:\s*true", content, re.MULTILINE))


def add_summarized_flag(content: str) -> str:
    return re.sub(
        r"(^---\n)(.*?)(^---\n)",
        lambda m: m.group(1) + m.group(2) + "summarized: true\n" + m.group(3),
        content,
        count=1,
        flags=re.MULTILINE | re.DOTALL
    )


def should_skip(filepath: Path) -> bool:
    # ETF 노트: 이미 표 형식으로 구조화됨
    if "yfinance" in filepath.name:
        return True
    return False


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    vault = Path(VAULT)
    lit_dir = vault / "01-literature"

    if not lit_dir.exists():
        print("[FAIL] 01-literature 폴더 없음", file=sys.stderr)
        sys.exit(1)

    # 오늘 날짜 노트 중 아직 요약 안 된 것
    targets = [
        f for f in sorted(lit_dir.glob(f"{today}-*.md"))
        if not should_skip(f)
    ]

    if not targets:
        print(f"[Summarize] 오늘({today}) 요약할 노트 없음", file=sys.stderr)
        print(json.dumps({"summarized": 0, "skipped": 0}))
        return

    summarized = skipped = 0
    for filepath in targets:
        content = filepath.read_text(encoding="utf-8")

        if already_summarized(content):
            print(f"  [SKIP] {filepath.name} (이미 요약됨)", file=sys.stderr)
            skipped += 1
            continue

        print(f"  [요약] {filepath.name}...", file=sys.stderr, end=" ")
        new_content = call_deepseek(content)

        if not new_content:
            print("실패", file=sys.stderr)
            continue

        # summarized 플래그 추가
        new_content = add_summarized_flag(new_content)
        filepath.write_text(new_content, encoding="utf-8")
        summarized += 1
        print("OK", file=sys.stderr)

    result = {"summarized": summarized, "skipped": skipped}
    print(json.dumps(result, ensure_ascii=False))
    print(f"[Summarize] 완료: {summarized}개 요약, {skipped}개 건너뜀", file=sys.stderr)


if __name__ == "__main__":
    main()
