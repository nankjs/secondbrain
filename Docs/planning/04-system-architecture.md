# 04-system-architecture.md: 시스템 아키텍처

## 문서 정보
- **작성일**: 2026-04-10
- **버전**: 1.0
- **상태**: Draft

---

## 1. 전체 시스템 개요

### 시스템 레이어 다이어그램

```
┌────────────────────────────────────────────────────────────────────┐
│                        사용자 인터페이스 (UI Layer)                 │
│  ┌──────────────────────┐    ┌──────────────────────────────────┐  │
│  │  Obsidian Client     │    │  Web UI (FastAPI + React)        │  │
│  │  (Phase A~D)         │    │  (Phase E+ 계획)                 │  │
│  └──────────────────────┘    └──────────────────────────────────┘  │
└────────────┬──────────────────────────────────────────────────────┘
             │
┌────────────▼──────────────────────────────────────────────────────┐
│                   지식 관리 계층 (Knowledge Layer)                  │
│  ┌─────────────────────────┐  ┌───────────────────────────────┐  │
│  │  Claude Code Skills     │  │  Zettelkasten MCP              │  │
│  │  - /fleeting            │  │  - 노트 관계 추적             │  │
│  │  - /literature          │  │  - 링크 자동화               │  │
│  │  - /permanent           │  │                                │  │
│  │  - /lint                │  │                                │  │
│  │  - /index               │  │                                │  │
│  │  - /relate              │  │                                │  │
│  └─────────────────────────┘  └───────────────────────────────┘  │
└────────────┬──────────────────────────────────────────────────────┘
             │
┌────────────▼──────────────────────────────────────────────────────┐
│                   AI 분석 계층 (AI Layer)                          │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐  │
│  │  LightRAG (Docker)   │  │  Claude API + MCP                 │  │
│  │  - 벡터 검색         │  │  - 보고서 생성                   │  │
│  │  - 임베딩            │  │  - 신뢰성 검수                  │  │
│  │  - 의존성 그래프     │  │                                  │  │
│  └──────────────────────┘  └──────────────────────────────────┘  │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  GPT Researcher (선택, Phase D+)                          │  │
│  │  - 자동 보고서 생성                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬──────────────────────────────────────────────────────┘
             │
┌────────────▼──────────────────────────────────────────────────────┐
│              수집 & 통합 계층 (Integration Layer)                  │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐  │
│  │  n8n (Docker)        │  │  API Connectors                  │  │
│  │  - 스케줄 실행       │  │  - ArXiv API                     │  │
│  │  - 워크플로우 조율   │  │  - yfinance API                  │  │
│  └──────────────────────┘  │  - RSS Feeds                     │  │
│                             │  - Notion API                   │  │
│  ┌──────────────────────┐  │                                  │  │
│  │  MiniFlux (Docker)   │  │  GitHub (Quartz)               │  │
│  │  - RSS 수집 & 통합   │  │  - 정적 사이트 배포            │  │
│  └──────────────────────┘  └──────────────────────────────────┘  │
└────────────┬──────────────────────────────────────────────────────┘
             │
┌────────────▼──────────────────────────────────────────────────────┐
│                  저장소 계층 (Storage Layer)                       │
│  ┌─────────────────────────┐  ┌────────────────────────────────┐  │
│  │  Obsidian Vault         │  │  메타데이터 저장소              │  │
│  │  (마크다운 + Metadata)  │  │  - SQLite (노트 인덱스)         │  │
│  │  - 00-fleeting/         │  │  - 벡터 스토어                 │  │
│  │  - 01-literature/       │  │                                │  │
│  │  - 02-permanent/        │  │  백업 & 아카이브               │  │
│  │  - 03-project/          │  │  - Git 저장소                  │  │
│  │  - 04-templates/        │  │  - 월간 아카이브               │  │
│  └─────────────────────────┘  └────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

---

## 2. Phase별 아키텍처 진화

### Phase A: Obsidian Vault 구조화

**목표**: 지식 저장소 기초 구축

```
개발자 설계
    ↓
[스키마 정의]
    ├─ Frontmatter 표준
    ├─ 폴더 구조
    └─ 태그 분류
    ↓
[Claude Code 스킬 정의]
    ├─ /fleeting (원문 → 떠돌이)
    ├─ /literature (원문 → 문헌)
    └─ /lint (검증)
    ↓
[Obsidian 설정]
    ├─ 플러그인 (Dataview, Graph, Templates)
    └─ 커스터마이징 (CSS, 테마)
    ↓
[GitOps 준비]
    └─ Vault → Git 저장소 (백업)
```

**산출물**: Obsidian Vault 템플릿, 스킬 정의서

---

### Phase B: n8n 수집 파이프라인

**목표**: 24/7 자동 정보 수집 (주 1회 실행)

```
신뢰 소스 목록 (도메인별)
    ↓
[n8n Workflow 설계]
    ├─ Trigger: Cron (주 1회)
    ├─ Step 1: RSS 수집 (MiniFlux)
    ├─ Step 2: API 수집 (ArXiv, yfinance)
    └─ Step 3: 데이터 검증
    ↓
[Claude 변환]
    └─ /literature 스킬 (원문 → 마크다운)
    ↓
[Obsidian 저장]
    └─ 01-literature/ 폴더에 자동 쓰기
    ↓
[알림 & 로깅]
    ├─ Slack 알림 (완료/실패)
    └─ n8n 대시보드 로깅
```

**산출물**: n8n 워크플로우 JSON, 신뢰 소스 목록

---

### Phase C: Zettelkasten 지식 연결

**목표**: 노트 간 자동 관계 생성 및 관리

```
새 문헌 노트 (Phase B 수집)
    ↓
[LightRAG 임베딩]
    └─ 벡터 생성 (1536차원)
    ↓
[유사도 검색]
    ├─ Top 20 유사 노트 추출 (코사인 유사도)
    ├─ 필터링: 임계값 > 0.7
    └─ 근거: "왜 이 노트와 관련?"
    ↓
[Claude 관계 분석]
    ├─ 관계 유형 결정 (맥락/보완/모순)
    └─ 신뢰도 점수 매김
    ↓
[Frontmatter 업데이트]
    └─ related: [노트ID] (자동 생성)
    ↓
[Obsidian 자동 링크]
    └─ [[노트명]] 형식으로 표시
    ↓
[사용자 피드백 루프]
    ├─ "맞음" → 가중치 +
    └─ "틀림" → 가중치 - (AI 학습)
```

**산출물**: Zettelkasten 정규화 프로세스, MCP 설정

---

### Phase D: 즉시 분석 시스템

**목표**: 한 줄 질문 → 5분 내 분석 보고서

```
사용자 질문 (Obsidian 또는 Web)
    ↓
[질문 파싱]
    ├─ 주제 추출
    ├─ 필요 관점 식별
    └─ 시간 범위 결정
    ↓
[LightRAG 벡터 검색]
    ├─ 쿼리 임베딩
    ├─ 관련 노트 검색 (Top 30)
    ├─ 필터링: domains, 시간 범위
    └─ 컨텍스트 구성
    ↓
[GPT Researcher 보고서 생성]
    ├─ 구조화 (배경/포인트/결론)
    ├─ 근거 나열 (출처 명시)
    └─ 마크다운 포맷
    ↓
[Claude 신뢰성 검수]
    ├─ 출처 검증
    ├─ 모순 탐지
    └─ 요약 확인
    ↓
[결과 반환]
    ├─ 마크다운 (기본)
    ├─ 슬라이드/표 (선택)
    └─ 관련 노트 링크
    ↓
[저장 & 피드백]
    ├─ 분석 결과 아카이브
    └─ 사용자 평가 기록
```

**산출물**: 분석 결과 마크다운, 벡터 검색 쿼리 로그

---

### Phase E: Notion 공유 레이어

**목표**: 역할별 팀 확장 (권한 관리)

```
Obsidian Vault (권한 없음 사용자도 접근)
    ↓
[Python 동기화 스크립트]
    ├─ Obsidian → JSON 변환
    ├─ 권한 필터링 (사용자별)
    │  ├─ 관리자: 전체
    │  ├─ 도메인 담당자: 도메인별
    │  └─ 뷰어: 요약 + 링크
    └─ Notion API로 업로드
    ↓
[Notion Database]
    ├─ 각 역할별 View
    ├─ 검색/필터링 기능
    └─ 댓글 (피드백)
    ↓
[양방향 동기화]
    └─ Notion 댓글 → Obsidian (선택)
```

**산출물**: 동기화 스크립트, Notion 템플릿 DB

---

### Phase F: Quartz 외부 공개

**목표**: 지식 자산 공개 및 팀 협업 활성화

```
Obsidian Vault (영구 노트 + 인덱스)
    ↓
[Quartz 정적 사이트 생성]
    ├─ 마크다운 → HTML
    ├─ [[링크]] → 자동 하이퍼링크
    ├─ 백링크 (역참조) 표시
    └─ 검색 기능 (클라이언트 사이드)
    ↓
[GitHub Pages 배포]
    ├─ CI/CD (GitHub Actions)
    ├─ 자동 업데이트 (매 푸시)
    └─ 커스텀 도메인 (선택)
    ↓
[공개 설정]
    ├─ 공개/비공개 태그 분류
    ├─ SEO 최적화
    └─ 분석 (Google Analytics)
```

**산출물**: Quartz 사이트, GitHub Actions 워크플로우

---

## 3. 데이터 흐름 (End-to-End)

### 메인 흐름: 수집 → 연결 → 분석

```
┌─────────────────────────────────────────────────────────────────┐
│ [1] 수집 (Collection) — Phase B                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  신뢰 소스                                                      │
│  ├─ RSS (기독교 뉴스, 학술 저널)                               │
│  ├─ API (ArXiv, yfinance, GitHub)                            │
│  └─ 웹사이트 (직접 방문)                                       │
│                │                                               │
│                ▼                                               │
│  [n8n] 주 1회 워크플로우 실행                                  │
│  ├─ 신규 항목 검색                                            │
│  ├─ 중복 제거                                                 │
│  ├─ 형식 정규화                                               │
│  └─ Claude API 호출                                           │
│                │                                               │
│                ▼                                               │
│  [Claude /literature 스킬]                                     │
│  ├─ 원문 파싱                                                 │
│  ├─ 메타데이터 추출 (저자, 날짜, 도메인)                      │
│  ├─ 핵심 요약 (3문장)                                         │
│  └─ Frontmatter 생성                                          │
│                │                                               │
│                ▼                                               │
│  [Obsidian API] 01-literature/ 저장                            │
│  └─ 파일: {date}-{domain}-{title}.md                         │
│     (예: 2026-04-10-arxiv-ml-attention.md)                  │
│                │                                               │
│                ▼                                               │
│  📊 결과: 주 5~10개 새 노트 자동 생성                         │
│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ [2] 연결 (Linking) — Phase C                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  새로운 문헌 노트 (위의 Phase B 산출물)                         │
│                │                                               │
│                ▼                                               │
│  [LightRAG] 임베딩 생성                                        │
│  ├─ 노트 전문 읽기                                            │
│  ├─ OpenAI Embedding API 호출                                │
│  └─ 벡터 저장 (1536차원)                                      │
│                │                                               │
│                ▼                                               │
│  [벡터 검색] 유사 노트 추출                                    │
│  ├─ 쿼리: 새 노트의 벡터                                      │
│  ├─ Top-K 검색: 20개 후보                                     │
│  ├─ 필터: 코사인 유사도 > 0.7                               │
│  └─ 시간 가중치: 최신 노트 선호                              │
│                │                                               │
│                ▼                                               │
│  [Claude MCP] 관계 분석                                        │
│  ├─ 프롬프트: "다음 두 노트의 관계?"                          │
│  ├─ 관계 유형:                                                │
│  │  ├─ context: "A는 B의 배경"                              │
│  │  ├─ extend: "A는 B를 확장"                               │
│  │  ├─ contradict: "A는 B와 모순"                           │
│  │  └─ related: "관련 있음"                                 │
│  ├─ 신뢰도: 0~1 스코어                                       │
│  └─ 설명: "왜 이런 관계인가?" (1문장)                        │
│                │                                               │
│                ▼                                               │
│  [Frontmatter] related 필드 업데이트                          │
│  ├─ related: [                                                │
│  │    { id: "note-001", type: "context", score: 0.95 },    │
│  │    { id: "note-002", type: "extend", score: 0.87 },     │
│  │    ...                                                   │
│  │  ]                                                        │
│  └─ Obsidian 링크: [[note-001|관계설명]]                     │
│                │                                               │
│                ▼                                               │
│  📊 결과: 3개월 내 100개 노트 자동 연결                       │
│          자동 연결 정확도 > 80%                              │
│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ [3] 분석 (Analysis) — Phase D                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  사용자 질문                                                    │
│  (예: "2026 Python 데이터 라이브러리 비교")                    │
│                │                                               │
│                ▼                                               │
│  [쿼리 파싱]                                                   │
│  ├─ 질문 텍스트 분석                                          │
│  ├─ 필요 도메인: 학술                                        │
│  ├─ 시간 범위: 2024-04 ~ 2026-04                           │
│  └─ 필터 설정                                                 │
│                │                                               │
│                ▼                                               │
│  [LightRAG 검색]                                               │
│  ├─ 쿼리 임베딩 (OpenAI)                                      │
│  ├─ 벡터 검색 (Top 30)                                        │
│  ├─ 메타데이터 필터:                                          │
│  │  ├─ domains: includes("학술")                            │
│  │  ├─ created: >= 2024-04                                 │
│  │  └─ type: "literature" OR "permanent"                   │
│  └─ 결과 정렬: 관련도 + 최신도                                │
│                │                                               │
│                ▼                                               │
│  [컨텍스트 구성]                                              │
│  ├─ 추출 노트들의 핵심 콘텐츠 합성                            │
│  ├─ 중복 제거 (같은 내용 병합)                                │
│  ├─ 관계 그래프 구성 (관련 노트간 연결)                       │
│  └─ 최종 컨텍스트 (5000 토큰 이내)                           │
│                │                                               │
│                ▼                                               │
│  [GPT Researcher 보고서 생성]                                 │
│  ├─ 입력: 질문 + 컨텍스트                                     │
│  ├─ 템플릿:                                                   │
│  │  ├─ ## 배경                                              │
│  │  ├─ ## 핵심 포인트                                       │
│  │  ├─ ## 비교 분석 (표)                                    │
│  │  ├─ ## 결론                                              │
│  │  └─ ## 참고 자료                                         │
│  └─ 마크다운 생성                                            │
│                │                                               │
│                ▼                                               │
│  [Claude 신뢰성 검수]                                         │
│  ├─ 각 주장의 출처 확인                                       │
│  ├─ 논리적 모순 탐지                                          │
│  ├─ 필요시 내용 수정                                          │
│  └─ 최종 승인                                                 │
│                │                                               │
│                ▼                                               │
│  [결과 반환]                                                   │
│  ├─ 형식: 마크다운                                            │
│  ├─ 포함:                                                      │
│  │  ├─ 종합 답변 (1~2문장)                                  │
│  │  ├─ 상세 분석 (섹션별)                                    │
│  │  ├─ 근거 자료 (링크: [[노트명]])                         │
│  │  └─ 관련 차트/표                                         │
│  └─ 전송 채널:                                                │
│     ├─ Obsidian (마크다운)                                   │
│     ├─ Web UI (HTML)                                        │
│     └─ Slack (요약)                                          │
│                │                                               │
│                ▼                                               │
│  📊 결과: 5분 내 분석 완료                                     │
│          사용자 만족도 4/5 이상                               │
│
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. 컴포넌트 인터페이스 (API/통신)

### 4.1 n8n ↔ Claude API

```
Request (n8n → Claude):
POST https://api.anthropic.com/v1/messages
Content-Type: application/json

{
  "model": "claude-opus",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "다음 원문을 문헌 노트로 변환:\n{원문}"
    }
  ],
  "system": "/literature 스킬 프롬프트"
}

Response:
{
  "content": [
    {
      "type": "text",
      "text": "---\ntype: literature\nsource_url: ...\n---\n\n# 제목\n\n내용..."
    }
  ],
  "stop_reason": "end_turn"
}
```

### 4.2 Obsidian API (로컬)

```python
from obsidian import Vault

vault = Vault("/path/to/SecondBrain")

# 새 노트 생성
note = vault.create_note(
    path="01-literature/2026-04-10-arxiv-ml.md",
    frontmatter={
        "type": "literature",
        "source_url": "https://arxiv.org/abs/...",
        "created": "2026-04-10T14:30:00Z",
        "domains": ["학술"],
        "tags": ["machine-learning", "arxiv"],
        "summary": "한 줄 요약"
    },
    content="# 제목\n\n## 요약\n..."
)

# 노트 업데이트
note.frontmatter["related"] = [
    {"id": "note-001", "type": "context", "score": 0.95}
]
note.save()
```

### 4.3 LightRAG API (Docker)

```python
import requests

# 임베딩 생성
response = requests.post(
    "http://localhost:7860/api/embeddings",
    json={
        "text": "노트 전문 텍스트",
        "model": "text-embedding-3-large"
    }
)
embedding = response.json()["embedding"]  # 1536차원

# 벡터 검색
search_response = requests.post(
    "http://localhost:7860/api/search",
    json={
        "query_embedding": embedding,
        "k": 20,
        "filters": {
            "domains": ["학술"],
            "created": {"gte": "2024-04-01"}
        }
    }
)
results = search_response.json()["results"]
# results[0] = {"id": "note-001", "score": 0.95, "content": "..."}
```

### 4.4 Notion API

```python
from notion_client import Client

notion = Client(auth="NOTION_API_KEY")

# 데이터베이스 쿼리
results = notion.databases.query(
    database_id="DATABASE_ID",
    filter={
        "property": "domains",
        "multi_select": {"contains": "학술"}
    }
)

# 페이지 생성
page = notion.pages.create(
    parent={"database_id": "DATABASE_ID"},
    properties={
        "Title": {"title": [{"text": {"content": "노트 제목"}}]},
        "Content": {"rich_text": [{"text": {"content": "내용"}}]},
        "Tags": {"multi_select": [{"name": "tag1"}]}
    }
)
```

---

## 5. 배포 환경 (Docker Compose)

### Docker Compose 구성

```yaml
version: '3.8'

services:
  # n8n: 워크플로우 자동화
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_HOST=n8n.local
      - N8N_PROTOCOL=http
      - N8N_SECURE_COOKIE=false
      - N8N_EDITOR_BASE_URL=http://localhost:5678/
    volumes:
      - ./data/n8n:/home/node/.n8n
      - ./n8n-workflows:/workflows
    networks:
      - secondbrain
    restart: unless-stopped

  # LightRAG: 벡터 저장소 & 임베딩
  lightrag:
    image: lightrag/lightrag:latest
    ports:
      - "7860:7860"
    environment:
      - EMBEDDING_MODEL=text-embedding-3-large
      - DATABASE_PATH=/data/lightrag.db
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data/lightrag:/data
      - ./lightrag_config:/config
    networks:
      - secondbrain
    restart: unless-stopped

  # MiniFlux: RSS 수집 및 통합
  minixflux:
    image: miniflux/miniflux:latest
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=sqlite3:///data/miniflux.db
      - ADMIN_USERNAME=${MINIFLUX_USER}
      - ADMIN_PASSWORD=${MINIFLUX_PASSWORD}
      - WORKER_POOL_SIZE=10
      - POLLING_FREQUENCY=30
    volumes:
      - ./data/miniflux:/data
    networks:
      - secondbrain
    depends_on:
      - lightrag
    restart: unless-stopped

  # Postgres: 메타데이터 저장 (향후)
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=secondbrain
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    networks:
      - secondbrain
    restart: unless-stopped

networks:
  secondbrain:
    driver: bridge
```

### 실행 명령어

```bash
# 환경 변수 설정
cp .env.example .env
# .env 파일 수정 (API 키, 비밀번호 등)

# 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f n8n
docker-compose logs -f lightrag

# 상태 확인
docker-compose ps

# 서비스 중지
docker-compose down

# 데이터 백업
docker-compose exec postgres pg_dump -U ${DB_USER} secondbrain > backup.sql
```

---

## 6. 백업 & 복구 전략

### 백업 항목 및 주기

| 항목 | 저장소 | 주기 | 방법 |
|------|--------|------|------|
| Obsidian Vault | Git + GitHub | 매일 | auto-commit |
| SQLite DB | 로컬 + S3 | 일일 | cron 스크립트 |
| 벡터 DB | Docker 볼륨 | 월 1회 | export |
| n8n 설정 | Git | 변경시 | 수동 커밋 |

### 복구 절차

**Obsidian Vault 복구**:
```bash
cd /path/to/SecondBrain
git log --oneline
git checkout <commit-hash>
```

**LightRAG 복구**:
```bash
docker-compose exec lightrag /bin/sh
sqlite3 /data/lightrag.db ".restore /backup/lightrag.db.backup"
```

---

## 7. 모니터링 & 운영

### 모니터링 대시보드

| 지표 | 도구 | 대상 |
|------|------|------|
| n8n 실행 | n8n UI | 워크플로우 성공/실패율 |
| API 응답 | 커스텀 로깅 | 임베딩, 분석 지연 |
| 저장소 용량 | df 명령 | Vault, DB 용량 |
| 에러율 | 로그 수집 | 각 서비스 |

### Slack 알림 연동

```
n8n Workflow 실패 → Slack #alerts

예시:
"❌ Weekly Collection Failed
시간: 2026-04-10 09:00 UTC
오류: ArXiv API 타임아웃
재시도: 자동 (09:30)"
```

### 정기 점검 체크리스트

**주 1회**:
- n8n 실행 로그 검토
- 수집 자료 품질 샘플링
- API 비용 추적

**월 1회**:
- Vault 용량 확인
- 벡터 검색 정확도 테스트
- 백업 복구 테스트

**분기별**:
- 전체 시스템 성능 분석
- 의존성 업그레이드 검토
- 아키텍처 개선 사항 도출

---

## 8. 확장성 및 미래 계획

### 단기 확장 (6개월)

```
Notion 공유 레이어 추가
    └─ 역할별 권한 관리
    └─ 팀 협업 활성화

Web UI 개발
    └─ FastAPI + React
    └─ 브라우저 기반 접근
```

### 중기 확장 (1년)

```
클라우드 마이그레이션
    └─ AWS/GCP 검토
    └─ 24/7 안정성 향상

추가 도메인 수집
    └─ 산업별 도메인 (의료, 법률 등)
    └─ 사용자별 커스터마이징
```

### 장기 확장 (2년+)

```
다중 사용자 협업 플랫폼
    └─ 실시간 동기화
    └─ 권한 기반 접근 제어

AI 고도화
    └─ 사용자 피드백 학습
    └─ 자동 분류 & 요약 정확도 향상

외부 공개 (Quartz)
    └─ 개인 지식 자산 공개
    └─ 커뮤니티 기여
```

---

## 9. 다음 단계

1. **Docker 환경 구축**: Phase B 전에 로컬 테스트
2. **n8n 프로토타입**: 첫 워크플로우 간단한 버전
3. **성능 테스트**: 수집 → 저장 → 검색 전체 흐름 검증
4. **모니터링 설계**: 운영 대시보드 준비
