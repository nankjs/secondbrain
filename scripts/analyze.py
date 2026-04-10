"""
즉시 분석 스크립트 (P4-T2/T3)
사용자 질문 → LightRAG 검색 → 구조화된 보고서 생성

사용법:
  python scripts/analyze.py "RAG와 전통 검색의 차이점"
  python scripts/analyze.py "인덱스 펀드 전략" --domain economy
  python scripts/analyze.py "제텔카스텐과 AI" --depth deep --save
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

LIGHTRAG_API = "http://localhost:9621"
VAULT_PATH = os.environ.get(
    "OBSIDIAN_VAULT_PATH",
    "C:/Users/kjswi/Documents/googleDrive/ObsiVault"
)

DEPTH_CONFIG = {
    "quick":    {"top_k": 10, "mode": "naive"},
    "standard": {"top_k": 30, "mode": "hybrid"},
    "deep":     {"top_k": 50, "mode": "global"},
}


def check_lightrag() -> bool:
    try:
        with urllib.request.urlopen(f"{LIGHTRAG_API}/health", timeout=5) as r:
            return json.loads(r.read()).get("status") == "healthy"
    except Exception:
        return False


def search_context(query: str, mode: str = "hybrid", top_k: int = 30) -> tuple[str, int]:
    """LightRAG에서 관련 컨텍스트 검색, (answer_text, source_count) 반환"""
    payload = json.dumps({
        "query": query,
        "mode": mode,
        "only_need_context": False,
        "response_type": "Multiple Paragraphs",
        "top_k": top_k,
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
            result = json.loads(r.read())
            context = result.get("response", "")
            # 출처 개수 추정 (References 섹션 파싱)
            refs = re.findall(r'\[\d+\]', context)
            source_count = len(set(refs)) if refs else (1 if context else 0)
            return context, source_count
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[FAIL] 검색 오류 HTTP {e.code}: {body[:200]}", file=sys.stderr)
        return "", 0
    except Exception as e:
        print(f"[FAIL] 검색 오류: {e}", file=sys.stderr)
        return "", 0


def generate_report(query: str, context: str, domain: str,
                    source_count: int, depth: str) -> str:
    """검색 컨텍스트 기반 보고서 생성"""
    today = datetime.now().strftime("%Y-%m-%d")

    if not context or context.strip() == "No relevant context found for the query.":
        return f"""# {query}

**분석일**: {today}
**도메인**: {domain}

---

## 결과 없음

현재 Vault에 이 주제와 관련된 노트가 없습니다.

**권장 액션**:
- `/literature` 스킬로 관련 자료 노트 작성
- n8n 수집 파이프라인에서 해당 주제 키워드 추가
- ArXiv 또는 RSS 피드에서 관련 자료 수집
"""

    report = f"""# {query}

**분석일**: {today}
**도메인**: {domain}
**깊이**: {depth}
**출처**: Vault 내 관련 노트 {source_count}개 참조

---

## 핵심 답변

{context.split(chr(10))[0] if context else "내용 없음"}

## 상세 분석

{context}

---
*이 보고서는 세컨드브레인 Vault의 지식을 바탕으로 생성되었습니다.*
*새 자료를 추가하면 다음 분석에 반영됩니다.*
"""
    return report


def save_report(report: str, query: str) -> Path:
    """보고서를 Vault에 저장"""
    vault = Path(VAULT_PATH)
    analysis_dir = vault / "03-resources" / "analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    # 파일명용 슬러그 생성
    slug = re.sub(r'[^\w가-힣]', '-', query)[:40].strip('-').lower()
    slug = re.sub(r'-+', '-', slug)

    file_path = analysis_dir / f"{today}-analysis-{slug}.md"
    file_path.write_text(report, encoding="utf-8")
    return file_path


def main():
    parser = argparse.ArgumentParser(description="세컨드브레인 즉시 분석")
    parser.add_argument("query", help="분석할 질문")
    parser.add_argument("--domain", default="all",
                        choices=["academic", "christian", "economy", "all"])
    parser.add_argument("--depth", default="standard",
                        choices=["quick", "standard", "deep"])
    parser.add_argument("--save", action="store_true", help="Vault에 보고서 저장")
    parser.add_argument("--no-print", action="store_true", help="보고서 출력 생략")
    args = parser.parse_args()

    # LightRAG 확인
    if not check_lightrag():
        print("[FAIL] LightRAG가 실행 중이지 않습니다.")
        print("  실행: docker compose up -d lightrag")
        sys.exit(1)

    config = DEPTH_CONFIG[args.depth]
    print(f"[분석] '{args.query}' (도메인={args.domain}, 깊이={args.depth})", file=sys.stderr)

    # 도메인 필터를 쿼리에 포함
    search_query = args.query
    if args.domain != "all":
        domain_map = {
            "academic": "academic research AI machine learning",
            "christian": "christian theology bible faith",
            "economy": "economy finance investment"
        }
        search_query = f"{args.query} {domain_map.get(args.domain, '')}"

    # 검색
    context, source_count = search_context(
        search_query,
        mode=config["mode"],
        top_k=config["top_k"]
    )

    # 보고서 생성
    report = generate_report(
        args.query, context, args.domain, source_count, args.depth
    )

    # 출력
    if not args.no_print:
        print(report)

    # 저장
    if args.save:
        saved_path = save_report(report, args.query)
        print(f"\n[저장] {saved_path}", file=sys.stderr)

    return report


if __name__ == "__main__":
    main()
