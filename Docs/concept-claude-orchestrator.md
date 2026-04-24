# Claude 온디맨드 오케스트레이터 — 설계 개념도

**작성일**: 2026-04-23  
**목적**: 세컨드브레인 시스템에서 Claude의 역할과 각 구현체의 연결 의도를 기록

---

## 핵심 설계 원칙

> Claude는 **사용자 요청 시에만** 작동한다. 토큰 비용이 발생하므로 자동 실행하지 않는다.

시스템은 두 개의 독립된 레이어로 구성된다.

```
┌─────────────────────────────────────────────┐
│  [자동 레이어] n8n 파이프라인 — 매일 07:00  │
│  수집 → 요약 → 임베딩 → 연결 → Notion → Linear │
│  Claude 개입 없음. 비용: LLM API(DeepSeek)만  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  [온디맨드 레이어] 사용자 요청 시에만        │
│  Claude가 직접 판단하고 실행                 │
│  비용: Claude 토큰 소비 → 사용자가 제어      │
└─────────────────────────────────────────────┘
```

---

## 시스템 전체 구조

```
사용자
  │
  │ (요청)
  ▼
Claude (온디맨드 오케스트레이터)
  │
  ├── Zettelkasten MCP ──→ ObsiVault 직접 읽기/쓰기
  │     C:/Users/kjswi/Documents/googleDrive/ObsiVault
  │     C:/KJS/tools/zettelkasten-mcp
  │
  ├── LightRAG (/analyze 스킬) ──→ 기존 지식 시맨틱 검색
  │     http://localhost:9621
  │     266개 문서 임베딩됨 (2026-04-23 기준)
  │
  ├── GPT Researcher ──→ 심층 웹 리서치
  │     http://localhost:8888
  │     DeepSeek V3 + Tavily/Google Search
  │
  └── 리서치 사이클 오케스트레이션
        Researcher Bot → Critic Bot (Gemini Flash) → 반복

              ↓ 결과
        ObsiVault/03-project/{프로젝트명}/
              ↓ 임베딩
        LightRAG (자동 파이프라인이 처리)
```

---

## Claude가 온디맨드로 수행하는 작업 유형

### 1. 지식 탐색 및 분석
- `/analyze` 스킬: 질문 → LightRAG 검색 → 즉시 분석 보고서
- Zettelkasten MCP로 Vault 내 특정 노트 직접 읽기
- 노트 간 관계 분석 및 연결 제안

### 2. 심층 리서치 오케스트레이션
- 복잡한 질문을 세부 질문으로 분해
- GPT Researcher / Perplexity API에 실행 지시
- 결과를 `03-project/{프로젝트명}/research-*.md`로 저장

### 3. 반자동 증폭 리서치 사이클 (N회, 사용자 지정)
```
[Researcher Bot] 초안 생성 (GPT Researcher / Perplexity)
      ↓
[Critic Bot] 비판 생성 (Gemini Flash 무료 티어)
  — 빠진 관점, 약한 근거, 상충하는 주장 지적
      ↓
[Researcher Bot] 비판 기반 보완 리서치
      ↓
(N회 반복 후 사용자 검토)
      ↓
최종 보고서 → 02-permanent/ 승격
```

### 4. 도메인 특화 문서 수집 지시
- 크롤링 대상 URL 및 조건 정의
- 수집 스크립트 실행 감독
- 파싱 결과 품질 확인 후 임베딩 승인

---

## 각 구현체와 존재 이유

| 구현체 | 위치 | Claude가 사용하는 방식 |
|--------|------|----------------------|
| Zettelkasten MCP | `C:/KJS/tools/zettelkasten-mcp` | Vault 직접 읽기/쓰기. `.mcp.json`으로 등록 |
| LightRAG | `localhost:9621` | `/analyze` 스킬, 시맨틱 검색 |
| GPT Researcher | `localhost:8888` | 심층 리서치 실행 |
| auto-linking.py | `scripts/` | `--days-back 1`로 신규 노트만 연결 (n8n 자동) |
| sync-notion.py | `scripts/` | 결과물을 Notion에 공유 (n8n 자동) |
| /analyze 스킬 | `.claude/skills/` | 온디맨드 분석 진입점 |
| /relate 스킬 | `.claude/skills/` | 두 노트 간 관계 판단 |

---

## Vault 폴더 구조와 Claude의 역할

```
ObsiVault/
  00-fleeting/     ← Claude가 임시 메모 작성 가능
  01-literature/   ← n8n 자동 수집 (Claude 직접 개입 최소화)
  02-permanent/    ← Claude가 핵심 인사이트 승격 기록
  03-project/      ← Claude의 주 작업 공간
    └── {프로젝트명}/
          _overview.md     ← 프로젝트 정의, 핵심 질문
          _questions.md    ← 연구 질문 목록 + 답변 상태
          research-*.md    ← GPT Researcher / Perplexity 보고서
          synthesis-*.md   ← Claude가 종합한 노트
  04-gemini/       ← 관심사 신호 (자동 생성)
  06-index/        ← 인덱스 (자동 생성)
  07-archive/      ← 원본 데이터 보관
```

---

## 자동 레이어 (참고 — Claude 개입 없음)

n8n 워크플로우 ID: `tpP9M1RQgIQLAlwl`

```
매일 07:00 (또는 수동 트리거)
  → MiniFlux (starred 항목 + trafilatura 전문 크롤링)
  → ArXiv (cs.AI/LG/CL 최신 논문)
  → yfinance (ETF 데이터)
  → DeepSeek V3 요약
  → LightRAG 임베딩
  → auto-linking (--days-back 1)
  → Notion 동기화
  → Linear PRI-5 알림
```

---

## 미완성 / 향후 구현 예정

### 즉시 가능
- [ ] GPT Researcher → `03-project/` 자동 저장 스크립트
- [ ] Perplexity API 연결 (`.env`에 `PERPLEXITY_API_KEY` 추가)
- [ ] Google Custom Search API 연결 (100쿼리/일 무료)

### 리서치 품질 향상
- [ ] Researcher Bot + Critic Bot 사이클 스크립트 (`scripts/research-cycle.py`)
  - Gemini Flash (무료) → Critic Bot 역할
  - 사이클 수: 사용자 지정 (기본 2회)
- [ ] 병렬 엔진 실행: GPT Researcher + Perplexity 동시 실행 후 교차 검증

### 도메인 특화 문서 수집
- [ ] PDF 크롤러 (`scripts/crawl-domain.py`)
  - Playwright + PyMuPDF
  - 조항 번호 기준 청킹 (토큰 단위 아님)
  - 메타데이터: 문서명, 발행기관, 버전, 발행일, 조항ID
  - 저장: `07-archive/{source}/{version}/`
  - Lazy loading: 목차만 먼저 임베딩, 필요 시 챕터 전문 임베딩
- [ ] 버전 관리: LightRAG 질의 시 버전 필터 적용

### n8n 연동 (선택)
- [ ] GPT Researcher 결과 → `03-project/` 자동 저장 노드
- [ ] 리서치 사이클 완료 → Linear 알림

---

## 설계 의도 요약

이 시스템의 목표는 **Claude가 세컨드브레인을 외부 기억 장치이자 연구 도구로 사용**하는 것이다.

- n8n은 지식의 **자동 유입**을 담당한다
- LightRAG는 지식의 **검색과 연결**을 담당한다
- Claude는 지식의 **해석, 종합, 생산**을 담당한다
- Vault는 모든 지식의 **영구 저장소**다

Claude가 이 시스템을 사용할 때의 원칙:
1. 사용자 요청이 있을 때만 작동한다
2. 결과는 반드시 Vault에 기록한다 (세션 종료 후에도 남도록)
3. 자동 레이어를 신뢰한다 — 매일 새 지식이 LightRAG에 들어온다
4. 토큰 사용량을 사용자가 인지할 수 있도록 작업 범위를 명시한다
