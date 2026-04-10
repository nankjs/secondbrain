---
title: "세컨드브레인 구축 전 과정 요약"
date: 2026-04-10
type: "report"
project: "아바타 프로젝트 / 세컨드브레인"
---

# 세컨드브레인 구축 전 과정 요약

> 2026-04-10 하루 동안 초안 연구 → 설계 → 구현 → 배포까지 완주한 기록

---

## 1. 출발점: 초안 연구 (Docs/draft/)

### 문제의식

메모는 열심히 쌓지만 **지식으로 전환되지 않는** 구조적 결함에서 시작.

초안 4개 문서를 통해 핵심 인사이트를 도출했다.

| 문서 | 핵심 내용 |
|------|---------|
| `01_오픈소스_스택_v1` | 수집 레이어 완성 (MiniFlux, ArXiv, yfinance 등 6개 도메인) |
| `02_LLM_자동_지식_연결` | 루만 제텔카스텐 + Karpathy 워크플로우 통합 아이디어 |
| `03_카르파티_지식기반` | frontmatter 캐싱으로 토큰 1/10 절감, 증분 위키 빌드 |
| `04_아키텍처_재검토_v2` | v1의 3대 결함 수정 → LightRAG + Obsidian 구조 확정 |

### v1 아키텍처의 3대 결함 (v2에서 해결)

1. **수집→저장 사이 지식 연결 레이어 없음** → LightRAG 도입
2. **노트 간 연결이 수동** → auto-linking.py 자동화
3. **Chroma 단독 채택** → LightRAG의 그래프+벡터 하이브리드로 교체

---

## 2. 최종 아키텍처 결정

```
[수집] MiniFlux RSS + ArXiv + yfinance
    ↓ n8n 오케스트레이션
[원자화] /fleeting → /literature → /permanent (Claude Code 스킬)
    ↓
[지식 연결] LightRAG (그래프 + 벡터 하이브리드, port 9621)
    ↓
[즉시 분석] /analyze 스킬 → 보고서 생성
    ↓
[공유] Notion 동기화 + Quartz 공개 사이트
```

**채택 스택:**

| 레이어 | 도구 | 포트 |
|--------|------|------|
| 오케스트레이션 | n8n | 15678 |
| RSS 수집 | MiniFlux | 8080 |
| 지식 연결 | LightRAG | 9621 |
| 노트 관리 | Obsidian Vault | 로컬 |
| 공유 | Notion API + Quartz | - |

---

## 3. 단계별 구현

### P0: 프로젝트 초기 설정 (15:01)
- Git 저장소, .gitignore, docker-compose.yml
- .env.example, 폴더 구조 (n8n-workflows/, scripts/, mcp-config/)
- 기획 문서 9개 (PRD, TRD, 시스템 아키텍처, 태스크 등)

### P1: Obsidian Vault + 스킬 (15:14)
- Vault 폴더 구조 8개 (00-fleeting ~ 07-archive)
- Frontmatter 스키마 표준 정의
- Claude Code 스킬 6개:

| 스킬 | 역할 |
|------|------|
| `/fleeting` | 빠른 캡처 → 떠돌이 노트 |
| `/literature` | 원문 → 문헌 노트 (n8n 연동) |
| `/permanent` | 문헌 → 영구 노트 |
| `/lint` | Frontmatter 검증 |
| `/index` | 인덱스 자동 생성 |
| `/relate` | 노트 관계 분석 |

### P2: 수집 파이프라인 (15:22 ~ 15:49)
- `scripts/collect-arxiv.py`: AI/ML 논문 ArXiv 수집
- `scripts/collect-yfinance.py`: 주식·ETF 시세 수집
- `scripts/setup-miniflux.py`: RSS 6개 자동 등록
  - ArXiv AI × 3개 피드
  - Hacker News
  - 매일경제 RSS
  - BBC Korea RSS
- `scripts/setup-n8n-workflow.py`: n8n 4-노드 워크플로우 API 등록
  - Cron → MiniFlux → ArXiv → yfinance 파이프라인
- `Docs/n8n-operations-guide.md`: 운영 매뉴얼

**검증:** n8n 워크플로우 ID `tpP9M1RQgIQLAlwl` 정상 등록, Vault 문헌 노트 6개 자동 생성

### P3: LightRAG 지식 연결 (세션 전환 후)
- `docker-compose.yml`: LightRAG 컨테이너 활성화 (gpt-4o-mini + text-embedding-3-small)
- `scripts/embed-vault.py`: Vault 노트 8개 일괄 임베딩
  - 00-fleeting 3개, 01-literature 5개
- `scripts/vector-search.py`: hybrid/naive/local/global 4가지 검색 모드
- `scripts/auto-linking.py`: 임계값(0.7) 기반 자동 노트 링크 생성
- `.claude/skills/relate/`: `/relate` 스킬 (6가지 관계 타입)

**검증:** 8개 노트 임베딩 0 failed, 벡터 검색 한국어/영어 모두 정상

### P4: /analyze 스킬 (세션 전환 후)
- `scripts/analyze.py`: 깊이별(quick/standard/deep) 분석, 도메인 필터
- `.claude/skills/analyze/`: `/analyze` 스킬 정의
  - 입력: 질문 + 도메인 + 깊이
  - 출력: 핵심 답변 + 상세 분석 + 출처 + Vault 자동 저장

**E2E 테스트 3개 시나리오 통과:**
1. "RAG와 전통 검색의 차이점" → 구조화 보고서
2. "성경 공부 지식 관리 방법" → 신학 자료 종합
3. "인덱스 펀드 ETF 투자 전략" → Vault 저장

### P5: Notion 공유 (17:43)

**발생한 에러 & 해결:**
- 이전 세션에서 curl + shell 보간으로 JSON 생성 → 이모지가 서로게이트 페어로 깨짐
- Notion API 400 오류: `"no low surrogate in string: line 1 column 191927"`
- **해결:** Python urllib + `json.dumps(ensure_ascii=False)` + 90블록 청킹 업로드

`scripts/sync-notion.py` 기능:
- `--setup`: 아바타 프로젝트 페이지 하위에 SecondBrain Vault DB 생성
- 마크다운 → Notion 블록 변환 (heading/bullet/code/paragraph)
- Frontmatter 파싱 → Notion 속성 자동 매핑
- 중복 방지 (기존 페이지 스킵)

**검증:** 01-literature 5개 노트 Notion 동기화 5/5 성공

### P6: Quartz 공개 사이트 (18:13 ~ 18:41)

**설치 과정의 시행착오:**
- 첫 번째 `git clone`: v4 브랜치가 inner 소스만 포함 (package.json 없음) → 재클론
- `cd quartz` 명령이 CWD에 누적되어 triple 중첩 발생 → 절대경로로 해결
- `npx quartz` Windows 경로 오류 (`./` 인식 불가) → `node bootstrap-cli.mjs`로 직접 실행

**결과:**
- `quartz/quartz.config.ts`: 한국어(ko-KR), 사이트명 SecondBrain 설정
- `scripts/build-quartz.sh`: Vault→content 복사 + 빌드 자동화
- 로컬 빌드: 8개 노트 → 54개 정적 파일 생성
- GitHub Actions 워크플로우 작성 (CI/CD)
  - `jackyzha0/quartz` 자동 클론 후 config/content 오버라이드
  - configure-pages 단계 제거 (첫 배포 실패 원인, 불필요)
- **배포 완료:** https://nankjs.github.io/secondbrain/

### 보너스: Gemini → Obsidian 북마크릿 (18:37)
- `scripts/gemini-webhook.py`: 로컬 HTTP 서버 (포트 19999)
- `scripts/gemini-bookmarklet.js`: Gemini DOM 스크래퍼
  - user/model 메시지 추출 → Frontmatter 포함 문헌 노트로 변환
  - 저장 위치: `01-literature/YYYY-MM-DD-gemini-*.md`

---

## 4. 최종 현황

| Phase | 상태 | 핵심 산출물 |
|-------|------|-----------|
| P0 | ✅ | Git, Docker, 기획 문서 9개 |
| P1 | ✅ | Obsidian Vault 구조 + 스킬 6개 |
| P2 | ✅ | n8n + MiniFlux + ArXiv + yfinance |
| P3 | ✅ | LightRAG (8개 노트 임베딩) |
| P4 | ✅ | /analyze 스킬 + E2E 테스트 3개 통과 |
| P5 | ✅ | Notion DB + 5개 노트 동기화 |
| P6 | ✅ | https://nankjs.github.io/secondbrain/ |
| 보너스 | ✅ | Gemini → Obsidian 북마크릿 |

---

## 5. 주요 교훈 및 결정 사항

| 항목 | 결정 |
|------|------|
| 벡터 DB | Chroma 포기 → LightRAG (그래프+벡터 통합) |
| Notion 업로드 | curl 금지 → Python urllib + ensure_ascii=False |
| Quartz 실행 | npx 금지 → node bootstrap-cli.mjs 직접 실행 |
| GitHub Actions | configure-pages 단계 제거 (불필요, 오류 원인) |
| 노트 구조 | Frontmatter 캐싱으로 토큰 1/10 절감 (Karpathy 방식 개선) |

---

## 6. 스크립트 목록

```
scripts/
├── collect-arxiv.py      # ArXiv 논문 수집
├── collect-yfinance.py   # 주식·ETF 수집
├── dedup.py              # 중복 제거
├── save-to-vault.py      # Vault 저장
├── setup-miniflux.py     # MiniFlux RSS 등록
├── setup-n8n-workflow.py # n8n 워크플로우 등록
├── embed-vault.py        # LightRAG 임베딩
├── auto-linking.py       # 자동 노트 링크
├── vector-search.py      # 벡터 검색
├── analyze.py            # 즉시 분석
├── sync-notion.py        # Notion 동기화
├── build-quartz.sh       # Quartz 빌드
├── gemini-webhook.py     # Gemini 저장 서버
└── gemini-bookmarklet.js # 북마크릿 소스
```

---

*작성: Claude Sonnet 4.6 | 2026-04-10*
