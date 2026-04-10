"""
LightRAG 벡터/그래프 검색 스크립트 (P3-T3)
유사 노트 검색 및 관련 지식 탐색

사용법:
  python scripts/vector-search.py "transformer attention mechanism"
  python scripts/vector-search.py "인덱스 펀드 장기 투자" --mode hybrid
  python scripts/vector-search.py "RAG 검색 방법" --mode global
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse

LIGHTRAG_API = "http://localhost:9621"


def search(query: str, mode: str = "hybrid") -> dict:
    """
    LightRAG 검색 수행
    mode: naive | local | global | hybrid
      - naive: 벡터 유사도만
      - local: 지역 그래프 탐색
      - global: 전역 그래프 탐색
      - hybrid: naive + local 결합 (권장)
    """
    payload = json.dumps({
        "query": query,
        "mode": mode,
        "only_need_context": False,
        "response_type": "Multiple Paragraphs",
        "top_k": 5,
        "max_token_for_text_unit": 4000,
        "max_token_for_global_context": 4000,
        "max_token_for_local_context": 4000
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{LIGHTRAG_API}/query",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}: {body[:500]}"}
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="LightRAG 지식 검색")
    parser.add_argument("query", help="검색 질문")
    parser.add_argument(
        "--mode",
        default="hybrid",
        choices=["naive", "local", "global", "hybrid"],
        help="검색 모드 (기본: hybrid)"
    )
    parser.add_argument("--json", action="store_true", help="JSON 출력")
    args = parser.parse_args()

    print(f"[검색] '{args.query}' (mode={args.mode})")
    print("-" * 60)

    result = search(args.query, args.mode)

    if "error" in result:
        print(f"[FAIL] {result['error']}")
        sys.exit(1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 응답 텍스트 출력
        response = result.get("response", result.get("answer", str(result)))
        print(response)


if __name__ == "__main__":
    main()
