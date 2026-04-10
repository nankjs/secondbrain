"""
중복 제거 유틸리티 (P2-T8)
수집된 URL의 중복 여부를 SQLite DB로 관리
"""

import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = os.environ.get(
    "DEDUP_DB_PATH",
    "C:/KJS/AVARTA/secondBrain/.data/collected_urls.db"
)


def _get_conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS collected_urls (
            url_hash TEXT PRIMARY KEY,
            url TEXT NOT NULL,
            domain TEXT,
            collected_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def url_hash(url: str) -> str:
    return hashlib.sha256(url.strip().encode()).hexdigest()[:16]


def is_duplicate(url: str) -> bool:
    """이미 수집된 URL이면 True"""
    conn = _get_conn()
    row = conn.execute(
        "SELECT 1 FROM collected_urls WHERE url_hash = ?", (url_hash(url),)
    ).fetchone()
    conn.close()
    return row is not None


def mark_collected(url: str, domain: str = "general") -> None:
    """URL을 수집 완료로 표시"""
    conn = _get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO collected_urls VALUES (?, ?, ?, ?)",
        (url_hash(url), url.strip(), domain, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def filter_new(items: list[dict], url_key: str = "url") -> list[dict]:
    """items 리스트에서 새로운 항목만 반환하고 수집 표시"""
    new_items = []
    for item in items:
        url = item.get(url_key, "")
        if not url:
            continue
        if not is_duplicate(url):
            new_items.append(item)
            mark_collected(url, item.get("domain", "general"))
    return new_items


def stats() -> dict:
    """수집 통계"""
    conn = _get_conn()
    total = conn.execute("SELECT COUNT(*) FROM collected_urls").fetchone()[0]
    by_domain = conn.execute(
        "SELECT domain, COUNT(*) FROM collected_urls GROUP BY domain"
    ).fetchall()
    conn.close()
    return {"total": total, "by_domain": dict(by_domain)}


if __name__ == "__main__":
    print("중복 제거 DB 통계:")
    s = stats()
    print(f"  총 수집: {s['total']}개")
    for domain, count in s["by_domain"].items():
        print(f"  {domain}: {count}개")
