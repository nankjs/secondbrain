"""
yfinance ETF 수집 → 원자료 저장 + Vault MD 노트 생성 파이프라인

실행: python3 /home/node/scripts/pipeline-yfinance.py
  - 원자료: /vault/data/raw/{date}/yfinance.json
  - 노트: /vault/01-literature/{date}-yfinance-etf-weekly.md
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    print("[FAIL] yfinance 미설치: pip install yfinance", file=sys.stderr)
    sys.exit(1)

VAULT = os.environ.get("OBSIDIAN_VAULT_PATH", "/vault")
TICKERS = ["SPY", "QQQ", "IVV", "VTI", "SCHD"]


def fetch_ticker(symbol: str) -> dict | None:
    try:
        t = yf.Ticker(symbol)
        info = t.info
        hist = t.history(period="1wk")
        if hist.empty:
            return None

        last_close = float(hist["Close"].iloc[-1])
        first_open = float(hist["Open"].iloc[0])
        week_change = (last_close - first_open) / first_open * 100

        news = []
        try:
            for n in (t.news or [])[:3]:
                news.append({
                    "title": n.get("title", ""),
                    "url": n.get("link", ""),
                })
        except Exception:
            pass

        return {
            "ticker": symbol,
            "name": info.get("longName", symbol),
            "price": round(last_close, 2),
            "week_change_pct": round(week_change, 2),
            "52w_high": round(info.get("fiftyTwoWeekHigh") or 0, 2),
            "52w_low": round(info.get("fiftyTwoWeekLow") or 0, 2),
            "news": news,
        }
    except Exception as e:
        print(f"  [WARN] {symbol} 실패: {e}", file=sys.stderr)
        return None


def make_note(data_list: list, today: str) -> str:
    summary_rows = ""
    for d in data_list:
        arrow = "▲" if d["week_change_pct"] >= 0 else "▼"
        summary_rows += f"| {d['ticker']} | {d['name'][:30]} | ${d['price']} | {arrow} {abs(d['week_change_pct']):.2f}% |\n"

    detail_blocks = ""
    for d in data_list:
        news_lines = ""
        for n in d.get("news", []):
            if n.get("title"):
                news_lines += f"- [{n['title']}]({n.get('url', '')})\n"

        detail_blocks += f"""
### {d['ticker']} — {d['name']}

| 현재가 | 주간 등락 | 52주 고 | 52주 저 |
|--------|----------|---------|---------|
| ${d['price']} | {d['week_change_pct']:+.2f}% | ${d['52w_high']} | ${d['52w_low']} |

{news_lines}"""

    return f"""---
title: "ETF 주간 동향 {today}"
date: {today}
type: "literature"
source: "yfinance"
domain: "economy"
tags: [yfinance, etf, economy, literature]
---

# ETF 주간 동향 {today}

> 출처: Yahoo Finance | 수집일: {today}

---

## 요약

| 티커 | 이름 | 가격 | 주간 등락 |
|------|------|------|----------|
{summary_rows}
## 상세

{detail_blocks}
"""


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    vault = Path(VAULT)
    raw_dir = vault / "07-archive" / today
    lit_dir = vault / "01-literature"
    raw_dir.mkdir(parents=True, exist_ok=True)
    lit_dir.mkdir(parents=True, exist_ok=True)

    # 중복 노트 방지
    filepath = lit_dir / f"{today}-yfinance-etf-weekly.md"
    if filepath.exists():
        print(f"[yfinance] 오늘 노트 이미 존재: {filepath.name}", file=sys.stderr)
        print(json.dumps({"source": "yfinance", "count": 0, "files": []}))
        return

    print("[yfinance] ETF 데이터 수집 중...", file=sys.stderr)
    data_list = []
    for sym in TICKERS:
        d = fetch_ticker(sym)
        if d:
            data_list.append(d)
            print(f"  [OK] {sym}: ${d['price']} ({d['week_change_pct']:+.2f}%)", file=sys.stderr)

    if not data_list:
        print("[yfinance] 수집된 데이터 없음", file=sys.stderr)
        print(json.dumps({"source": "yfinance", "count": 0, "files": []}))
        return

    # 원자료 저장
    raw_file = raw_dir / "yfinance.json"
    raw_file.write_text(json.dumps(data_list, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[yfinance] 원자료: {raw_file}", file=sys.stderr)

    # MD 노트 생성
    filepath.write_text(make_note(data_list, today), encoding="utf-8")
    print(f"[yfinance] 저장: {filepath.name}", file=sys.stderr)

    result = {"source": "yfinance", "count": 1, "files": [str(filepath)]}
    print(json.dumps(result, ensure_ascii=False))
    print("[yfinance] 완료", file=sys.stderr)


if __name__ == "__main__":
    main()
