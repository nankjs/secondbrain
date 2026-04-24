"""
Linear 파이프라인 실행 결과 알림

실행: python3 /home/node/scripts/notify-linear.py
  - 오늘 01-literature/ 노트 수를 집계하여 Linear 이슈에 댓글 추가
  - LINEAR_API_KEY, LINEAR_ISSUE_ID 환경변수 필요
"""

import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY", "")
LINEAR_ISSUE_ID = os.environ.get("LINEAR_ISSUE_ID", "PRI-5")
VAULT = os.environ.get("OBSIDIAN_VAULT_PATH", "/vault")
LINEAR_API_URL = "https://api.linear.app/graphql"


def get_issue_uuid(identifier: str) -> str:
    query = f'{{ issue(id: "{identifier}") {{ id }} }}'
    payload = json.dumps({"query": query}).encode("utf-8")
    req = urllib.request.Request(
        LINEAR_API_URL,
        data=payload,
        headers={
            "Authorization": LINEAR_API_KEY,
            "Content-Type": "application/json",
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    return data["data"]["issue"]["id"]


def post_comment(issue_uuid: str, body: str) -> bool:
    mutation = """
    mutation CommentCreate($issueId: String!, $body: String!) {
      commentCreate(input: { issueId: $issueId, body: $body }) {
        success
      }
    }
    """
    payload = json.dumps({
        "query": mutation,
        "variables": {"issueId": issue_uuid, "body": body}
    }).encode("utf-8")

    req = urllib.request.Request(
        LINEAR_API_URL,
        data=payload,
        headers={
            "Authorization": LINEAR_API_KEY,
            "Content-Type": "application/json",
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    return data.get("data", {}).get("commentCreate", {}).get("success", False)


def count_notes_by_source(today: str) -> dict:
    lit_dir = Path(VAULT) / "01-literature"
    counts = {"miniflux": 0, "arxiv": 0, "yfinance": 0, "total": 0}

    if not lit_dir.exists():
        return counts

    for f in lit_dir.glob(f"{today}-*.md"):
        counts["total"] += 1
        if "-rss-" in f.name:
            counts["miniflux"] += 1
        elif "-arxiv-" in f.name:
            counts["arxiv"] += 1
        elif "-yfinance-" in f.name:
            counts["yfinance"] += 1

    return counts


def build_comment(today: str, counts: dict, error: str = "") -> str:
    status = "✅ 정상 완료" if not error else "❌ 오류 발생"
    lines = [
        f"## {status} — {today} 07:00 KST",
        "",
        "| 단계 | 결과 |",
        "|------|------|",
        f"| MiniFlux RSS | {counts['miniflux']}개 노트 |",
        f"| ArXiv 논문 | {counts['arxiv']}개 노트 |",
        f"| yfinance ETF | {counts['yfinance']}개 노트 |",
        f"| **합계** | **{counts['total']}개** |",
    ]

    if error:
        lines += ["", f"**오류 내용:**", f"```", error, "```"]

    return "\n".join(lines)


def main():
    if not LINEAR_API_KEY:
        print("[FAIL] LINEAR_API_KEY 미설정", file=sys.stderr)
        sys.exit(1)

    today = datetime.now().strftime("%Y-%m-%d")
    error_msg = ""

    # stdin으로 오류 메시지 수신 (n8n에서 파이프로 전달 가능)
    if not sys.stdin.isatty():
        error_msg = sys.stdin.read().strip()

    counts = count_notes_by_source(today)
    comment = build_comment(today, counts, error_msg)

    try:
        issue_uuid = get_issue_uuid(LINEAR_ISSUE_ID)
        success = post_comment(issue_uuid, comment)
        if success:
            print(f"[Linear] 댓글 추가 완료 → {LINEAR_ISSUE_ID}", file=sys.stderr)
        else:
            print("[Linear] 댓글 추가 실패 (API 응답 오류)", file=sys.stderr)
    except Exception as e:
        print(f"[Linear] 오류: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps({"source": "linear", "issue": LINEAR_ISSUE_ID, "notes": counts["total"]}))


if __name__ == "__main__":
    main()
