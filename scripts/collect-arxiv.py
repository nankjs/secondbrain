"""
ArXiv 논문 수집 스크립트 (P2-T5)
n8n Execute Command 노드 또는 직접 실행 가능

사용법:
  python scripts/collect-arxiv.py --domain academic --max 5
"""

import argparse
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

QUERIES = {
    "ai": "cat:cs.AI",
    "ml": "cat:cs.LG",
    "nlp": "cat:cs.CL",
    "combined": "cat:cs.AI OR cat:cs.LG OR cat:cs.CL",
}

ARXIV_API = "https://export.arxiv.org/api/query"


def fetch_arxiv(query: str, max_results: int = 5, days_back: int = 7) -> list[dict]:
    """ArXiv API에서 최신 논문 수집"""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)

    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results * 3,  # 날짜 필터 후 부족할 수 있어 여유 있게
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = ARXIV_API + "?" + urllib.parse.urlencode(params)

    with urllib.request.urlopen(url, timeout=30) as resp:
        content = resp.read().decode("utf-8")

    # XML 파싱
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(content)
    papers = []

    for entry in root.findall("atom:entry", ns):
        published_str = entry.findtext("atom:published", "", ns)
        try:
            published = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
        except Exception:
            continue

        if published < cutoff:
            continue

        arxiv_id = entry.findtext("atom:id", "", ns).split("/abs/")[-1]
        title = entry.findtext("atom:title", "", ns).strip().replace("\n", " ")
        summary = entry.findtext("atom:summary", "", ns).strip().replace("\n", " ")
        authors = [a.findtext("atom:name", "", ns)
                   for a in entry.findall("atom:author", ns)]

        papers.append({
            "id": arxiv_id,
            "title": title,
            "authors": authors[:3],  # 최대 3명
            "summary": summary[:500] + ("..." if len(summary) > 500 else ""),
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "published": published.strftime("%Y-%m-%d"),
            "domain": "academic",
            "source_type": "paper",
        })

        if len(papers) >= max_results:
            break

    return papers


def main():
    parser = argparse.ArgumentParser(description="ArXiv 논문 수집")
    parser.add_argument("--query", default="combined", choices=list(QUERIES.keys()))
    parser.add_argument("--max", type=int, default=5)
    parser.add_argument("--days", type=int, default=14)
    parser.add_argument("--output", default="-", help="출력 파일 (- = stdout)")
    args = parser.parse_args()

    papers = fetch_arxiv(QUERIES[args.query], args.max, args.days)

    result = {
        "collected_at": datetime.now().isoformat(),
        "query": args.query,
        "count": len(papers),
        "papers": papers,
    }

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"저장 완료: {args.output} ({len(papers)}개 논문)")


if __name__ == "__main__":
    main()
