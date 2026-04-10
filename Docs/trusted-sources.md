# 신뢰 소스 목록

n8n 자동 수집 대상 소스. MiniFlux RSS + API 직접 통합.

최종 업데이트: 2026-04-10

---

## 기독교 도메인 (Christian)

| # | 소스명 | 유형 | URL / API | 수집 방식 | 우선순위 |
|---|--------|------|-----------|---------|---------|
| C1 | 갓피플 뉴스 | 뉴스 | https://news.godpeople.com/rss | RSS | 높음 |
| C2 | 기독일보 | 뉴스 | https://www.christiandaily.co.kr/rss/all | RSS | 높음 |
| C3 | 기독교한국루터회 | 신학 | https://www.lck.kr/rss | RSS | 중간 |
| C4 | 복음과상황 | 잡지 | https://www.goscon.co.kr/rss | RSS | 중간 |
| C5 | 목사님 추천 (수동) | 설교/자료 | 별도 지정 | 수동 입력 | 높음 |

---

## 학술 도메인 (Academic)

| # | 소스명 | 유형 | URL / API | 수집 방식 | 우선순위 |
|---|--------|------|-----------|---------|---------|
| A1 | ArXiv cs.AI | 논문 | https://arxiv.org/rss/cs.AI | RSS | 높음 |
| A2 | ArXiv cs.LG | 논문 | https://arxiv.org/rss/cs.LG | RSS | 높음 |
| A3 | GitHub Trending | 코드 | https://github.com/trending (scrape) | 크롤링 | 중간 |
| A4 | Hacker News | 기술뉴스 | https://hnrss.org/frontpage | RSS | 높음 |
| A5 | Papers With Code | 논문+코드 | https://paperswithcode.com/rss | RSS | 높음 |

---

## 경제 도메인 (Economy)

| # | 소스명 | 유형 | URL / API | 수집 방식 | 우선순위 |
|---|--------|------|-----------|---------|---------|
| E1 | 연합뉴스 경제 | 뉴스 | https://www.yna.co.kr/economy/all/feed | RSS | 높음 |
| E2 | 매일경제 | 뉴스 | https://www.mk.co.kr/rss/30100041/ | RSS | 높음 |
| E3 | yfinance SPY | 주식 | Python yfinance API | API | 높음 |
| E4 | yfinance QQQ | 주식 | Python yfinance API | API | 중간 |
| E5 | yfinance IVV | 주식 | Python yfinance API | API | 중간 |

---

## n8n 등록 순서 (우선순위 기준)

### Phase 1차 등록 (MVP — 높음 우선순위, 9개)
1. C1: 갓피플 뉴스 RSS
2. C2: 기독일보 RSS
3. A1: ArXiv cs.AI RSS
4. A2: ArXiv cs.LG RSS
5. A4: Hacker News RSS
6. A5: Papers With Code RSS
7. E1: 연합뉴스 경제 RSS
8. E2: 매일경제 RSS
9. E3/E4/E5: yfinance API (별도 Python 스크립트)

### Phase 2차 등록 (안정화 후, 중간 우선순위)
- C3, C4, A3 추가

---

## 수집 필터링 규칙

| 규칙 | 설명 |
|------|------|
| 중복 제거 | 동일 URL은 1회만 수집 (SQLite에 URL 해시 저장) |
| 최소 길이 | 본문 200자 미만 제외 |
| 날짜 필터 | 7일 이내 발행 기사만 |
| 도메인 분류 | URL/키워드 기반 자동 분류, 불명확 시 general |

---

## yfinance 수집 스크립트 위치

`scripts/collect-yfinance.py` (P2-T6에서 작성)

수집 항목:
- 주간 종가, 거래량
- 52주 최고/최저
- 관련 뉴스 헤드라인 (Yahoo Finance)
