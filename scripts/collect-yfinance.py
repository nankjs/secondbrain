"""
yfinance 주식/ETF 데이터 수집 스크립트 (P2-T6)
n8n Execute Command 노드 또는 직접 실행 가능

설치 필요: pip install yfinance

사용법:
  python scripts/collect-yfinance.py
  python scripts/collect-yfinance.py --tickers SPY QQQ IVV --output data/stock.json
"""

import argparse
import json
from datetime import datetime

# yfinance는 선택적 임포트 (미설치 시 안내)
try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

DEFAULT_TICKERS = ["SPY", "QQQ", "IVV", "VTI", "SCHD"]


def collect_ticker(ticker_sym: str) -> dict:
    """단일 티커 데이터 수집"""
    ticker = yf.Ticker(ticker_sym)
    info = ticker.info
    hist = ticker.history(period="1wk")

    if hist.empty:
        return {"ticker": ticker_sym, "error": "데이터 없음"}

    latest = hist.iloc[-1]
    prev = hist.iloc[0] if len(hist) > 1 else latest
    week_change = ((latest["Close"] - prev["Open"]) / prev["Open"]) * 100

    # 뉴스 수집
    news = []
    try:
        for n in ticker.news[:3]:
            news.append({
                "title": n.get("title", ""),
                "url": n.get("link", ""),
                "published": datetime.fromtimestamp(
                    n.get("providerPublishTime", 0)
                ).strftime("%Y-%m-%d"),
            })
    except Exception:
        pass

    return {
        "ticker": ticker_sym,
        "name": info.get("longName", ticker_sym),
        "price": round(latest["Close"], 2),
        "week_change_pct": round(week_change, 2),
        "week_volume": int(hist["Volume"].sum()),
        "52w_high": info.get("fiftyTwoWeekHigh"),
        "52w_low": info.get("fiftyTwoWeekLow"),
        "expense_ratio": info.get("annualReportExpenseRatio"),
        "domain": "economy",
        "source_type": "market_data",
        "news": news,
        "collected_at": datetime.now().strftime("%Y-%m-%d"),
    }


def main():
    if not HAS_YFINANCE:
        print("yfinance 미설치. 설치 명령: pip install yfinance")
        print('{"error": "yfinance not installed"}')
        return

    parser = argparse.ArgumentParser(description="yfinance ETF/주식 데이터 수집")
    parser.add_argument("--tickers", nargs="+", default=DEFAULT_TICKERS)
    parser.add_argument("--output", default="-")
    args = parser.parse_args()

    results = []
    for sym in args.tickers:
        print(f"  수집 중: {sym}...", flush=True)
        try:
            data = collect_ticker(sym)
            results.append(data)
        except Exception as e:
            results.append({"ticker": sym, "error": str(e)})

    output = json.dumps({
        "collected_at": datetime.now().isoformat(),
        "count": len(results),
        "tickers": results,
    }, ensure_ascii=False, indent=2)

    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"저장 완료: {args.output}")


if __name__ == "__main__":
    main()
