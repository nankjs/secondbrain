"""
MiniFlux RSS 피드 일괄 등록 스크립트 (P2-T4)
신뢰 소스 목록의 RSS 피드를 MiniFlux에 자동 등록
"""

import json
import urllib.request
import urllib.parse
import base64
import sys

MINIFLUX_URL = "http://localhost:8080"
USERNAME = "admin"
PASSWORD = "secondbrain2026"

# 신뢰 소스 목록 (Docs/trusted-sources.md 기반, RSS 가능한 소스만)
FEEDS = [
    # 기독교 (국내 기독교 RSS 접근 제한 많음 → 대체 소스 사용)
    {"url": "https://rss.cnn.com/rss/edition_world.rss",   "category": "기독교", "title": "CNN World (대체)"},
    {"url": "https://feeds.bbci.co.uk/news/rss.xml",       "category": "기독교", "title": "BBC News (대체)"},
    # 학술
    {"url": "https://arxiv.org/rss/cs.AI",                 "category": "학술",   "title": "ArXiv cs.AI"},
    {"url": "https://arxiv.org/rss/cs.LG",                 "category": "학술",   "title": "ArXiv cs.LG"},
    {"url": "https://hnrss.org/frontpage",                 "category": "학술",   "title": "Hacker News"},
    {"url": "https://arxiv.org/rss/cs.CL",                 "category": "학술",   "title": "ArXiv cs.CL (NLP)"},
    # 경제
    {"url": "https://feeds.reuters.com/reuters/businessNews", "category": "경제", "title": "Reuters Business"},
    {"url": "https://www.mk.co.kr/rss/30100041/",          "category": "경제",   "title": "매일경제"},
]


def api_request(method: str, path: str, data: dict = None) -> dict:
    url = MINIFLUX_URL + path
    token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode()
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        content = e.read().decode()
        return {"error": f"HTTP {e.code}: {content[:200]}"}
    except Exception as e:
        return {"error": str(e)}


def get_or_create_category(name: str) -> int:
    """카테고리가 없으면 생성하고 ID 반환"""
    cats = api_request("GET", "/v1/categories")
    if isinstance(cats, list):
        for cat in cats:
            if cat.get("title") == name:
                return cat["id"]
    result = api_request("POST", "/v1/categories", {"title": name})
    return result.get("id", 0)


def add_feed(feed_url: str, category_id: int, title: str) -> dict:
    return api_request("POST", "/v1/feeds", {
        "feed_url": feed_url,
        "category_id": category_id,
        "title": title,
        "crawler": False,
        "scraper_rules": "",
        "rewrite_rules": "",
    })


def main():
    print("MiniFlux RSS 피드 등록 시작")
    print(f"  대상: {MINIFLUX_URL}")
    print(f"  등록할 피드: {len(FEEDS)}개\n")

    # 카테고리 생성
    categories = {}
    for cat_name in set(f["category"] for f in FEEDS):
        cat_id = get_or_create_category(cat_name)
        categories[cat_name] = cat_id
        print(f"  카테고리 [{cat_name}] ID={cat_id}")

    print()

    # 피드 등록
    ok, fail = 0, 0
    for feed in FEEDS:
        cat_id = categories.get(feed["category"], 0)
        result = add_feed(feed["url"], cat_id, feed["title"])
        if "error" in result:
            if "already_subscribed" in str(result.get("error", "")):
                print(f"  [SKIP] {feed['title']} - already registered")
                ok += 1
            else:
                print(f"  [FAIL] {feed['title']} - {result['error'][:80]}")
                fail += 1
        else:
            print(f"  [OK] {feed['title']} (ID={result.get('id', '?')})")
            ok += 1

    print(f"\n완료: 성공 {ok}개 / 실패 {fail}개")

    if fail > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
