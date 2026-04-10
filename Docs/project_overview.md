---
project: 세컨드브레인 구축 (아바타 프로젝트)
created: 2026-04-10
leader: Claude → Gemini (인계)
status: active
---

# TASKS.md — 세컨드브레인 개발문서 작성 계획

> **목표**: draft 초안들을 출발점으로, /socrates 스킬을 활용하여 소크라테스식 문답법으로 요구사항을 구체화하고 전체 개발문서를 완성한다.

---

## 프로젝트 배경

**아바타 프로젝트 / 세컨드브레인 구축**

- Karpathy LLM Wiki 방법론 + 루만 제텔카스텐을 합친 개인 지식 관리 시스템
- 6개 도메인(학술·뉴스·커뮤니티·소셜·경제·기독교) 자동 수집 파이프라인
- 수집 → 원자화 → 지식 연결 → 창발적 아이디어 생산이 핵심 가치
- v2 아키텍처 초안이 완성된 상태 (04_오픈소스_스택과_아키텍처_재검토_v2.md 참고)

**핵심 기술 스택 (v2)**:
- 수집: Firecrawl, MiniFlux, newspaper4k, ArXiv, Semantic Scholar, PRAW, yt-dlp+Whisper, yfinance, pykrx, DART-FSS, FRED
- 파이프라인: n8n
- 원자화: Claude Code 스킬 (/fleeting, /literature)
- 지식 연결: Zettelkasten MCP + /permanent, /lint, /index
- 검색: LightRAG (Chroma 대체, 그래프+벡터 하이브리드)
- 저장: Obsidian Vault (Zettelkasten 구조)
- 공유: Notion 벡터 RAG + Quartz

---

## 참조 문서 (초안)

| 파일 | 내용 |
|------|------|
| `Docs/draft/01_오픈소스_스택과_아키텍처_검토_v1.md` | 수집 스택 초안 |
| `Docs/draft/02_LLM_자동_지식_연결_세컨드브레인_창발_아키텍처_연구.md` | Karpathy + 제텔카스텐 분석, 토큰 절약 3전략 |
| `Docs/draft/03_안드레이_카르파티_개인용_지식_기반_구축.md` | Karpathy 원문 번역 및 인사이트 |
| `Docs/draft/04_오픈소스_스택과_아키텍처_재검토_v2.md` | **최신 아키텍처 v2** (이것이 기준) |
| `Docs/draft/오픈소스_스택_참조_목록.md` | 도구별 GitHub 링크 및 설치 방법 |

---

## 작업 계획

### Phase 0: 스킬 기반 마련

| ID | 작업 | 목표 | 우선순위 |
|----|------|------|---------|
| T00 | `/socrates` 스킬 정의 작성 | 소크라테스식 문답으로 요구사항 도출하는 스킬 | 🔴 최우선 |

**T00 상세**: `/socrates` 스킬은 다음 방식으로 동작한다:
- 작성할 문서의 목적을 먼저 선언
- LLM이 5~7개의 핵심 질문을 순서대로 제시
- 사용자가 답변하면 LLM이 요약·정제하여 문서 섹션으로 구성
- 불명확한 답변은 재질문
- 모든 질문 완료 후 문서 초안 생성

---

### Phase 1: 핵심 기획 문서

| ID | 작업 | 출력 파일 | 의존성 |
|----|------|---------|-------|
| T01 | PRD 작성 | `Docs/planning/01-PRD.md` | T00 |
| T02 | TRD 작성 | `Docs/planning/02-TRD.md` | T01 |
| T03 | 아키텍처 문서 | `Docs/planning/03-Architecture.md` | T02 |

**T01 PRD 핵심 질문 영역**:
- 사용자 페르소나 (누가 쓸 것인가)
- 핵심 사용 시나리오 (어떤 상황에서, 무엇을 얻는가)
- 성공 지표 (지식 연결 수, 창발 노트 생성 빈도 등)
- 범위 경계 (무엇을 하지 않을 것인가)

**T02 TRD 핵심 질문 영역**:
- 각 레이어별 기술 선택 근거 (v2 아키텍처 기반)
- 데이터 흐름 및 인터페이스 명세
- frontmatter 스키마 확정
- 비기능 요구사항 (성능, 토큰 비용, 오프라인 지원 등)

---

### Phase 2: 스킬 정의 문서

| ID | 작업 | 출력 파일 | 의존성 |
|----|------|---------|-------|
| T04 | frontmatter 스키마 확정 | `Docs/planning/04-Frontmatter-Schema.md` | T02 |
| T05 | `/fleeting` 스킬 정의 | `.claude/skills/fleeting.md` | T04 |
| T06 | `/literature` 스킬 정의 | `.claude/skills/literature.md` | T04 |
| T07 | `/permanent` 스킬 정의 | `.claude/skills/permanent.md` | T05, T06 |
| T08 | `/lint` 스킬 정의 | `.claude/skills/lint.md` | T07 |
| T09 | `/index` 스킬 정의 | `.claude/skills/index.md` | T07 |
| T10 | `/query` 스킬 정의 | `.claude/skills/query.md` | T09 |
| T11 | `/loop` 스킬 정의 | `.claude/skills/loop.md` | T10 |

---

### Phase 3: 인프라 설계 문서

| ID | 작업 | 출력 파일 | 의존성 |
|----|------|---------|-------|
| T12 | Obsidian Vault 구조 설계 | `Docs/planning/05-Vault-Structure.md` | T03 |
| T13 | n8n 워크플로우 설계 | `Docs/planning/06-n8n-Workflows.md` | T03 |
| T14 | LightRAG 통합 설계 | `Docs/planning/07-LightRAG-Integration.md` | T03 |
| T15 | Zettelkasten MCP 설정 | `Docs/planning/08-ZettelkastenMCP.md` | T03 |
| T16 | 배포/설치 가이드 | `Docs/planning/09-Setup-Guide.md` | T12~T15 |

---

### Phase 4: 운영 문서

| ID | 작업 | 출력 파일 |
|----|------|---------|
| T17 | 주간 운영 매뉴얼 | `Docs/planning/10-Operations.md` |
| T18 | 확장성 로드맵 | `Docs/planning/11-Roadmap.md` |

---

## 진행 상태

| ID | 상태 | 완료일 |
|----|------|-------|
| T00 | ⬜ 대기 | - |
| T01 | ⬜ 대기 | - |
| T02 | ⬜ 대기 | - |
| T03 | ⬜ 대기 | - |
| T04 | ⬜ 대기 | - |
| T05~T11 | ⬜ 대기 | - |
| T12~T16 | ⬜ 대기 | - |
| T17~T18 | ⬜ 대기 | - |

---

## 작업 규칙

1. **소크라테스 원칙**: 문서를 직접 쓰기 전에 /socrates 스킬로 요구사항 먼저 도출
2. **초안 우선**: draft 폴더 문서를 항상 먼저 참조하고 출발점으로 삼는다
3. **단계 준수**: 의존성 순서를 지킨다. PRD 없이 TRD 작성 금지
4. **파일 저장 위치**: `Docs/planning/` 폴더에 순서대로 저장
5. **승인 대기**: 각 Phase 완료 후 사용자 확인을 받고 다음 Phase 진행

---

*작성: 2026-04-10 | Claude → Gemini 인계*
