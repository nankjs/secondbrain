# 02-trd.md: 기술 요구사항 정의서 (TRD)

## 문서 정보
- **작성일**: 2026-04-10
- **버전**: 1.0
- **상태**: Draft

---

## 1. 기술 스택 개요

### 시스템 아키텍처 레이어

```
┌─────────────────────────────────────────────────┐
│  사용자 인터페이스 (UI)                          │
│  - Obsidian (클라이언트)                         │
│  - Web UI (FastAPI + React, 향후)               │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│  지식 관리 계층 (Knowledge Layer)               │
│  - Claude Code 스킬 (/fleeting, /permanent 등) │
│  - Zettelkasten MCP                            │
│  - 임베딩 + 벡터 DB                            │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│  AI 분석 계층 (AI Layer)                        │
│  - LightRAG (Docker)                           │
│  - GPT Researcher                              │
│  - Claude API                                  │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│  수집 & 통합 계층 (Integration Layer)          │
│  - n8n (Docker) — 스케줄 & 워크플로우          │
│  - RSS Reader (MiniFlux)                       │
│  - API Connectors (ArXiv, yfinance 등)        │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│  저장소 계층 (Storage Layer)                    │
│  - Obsidian Vault (마크다운)                   │
│  - SQLite (메타데이터)                         │
│  - 벡터 스토어 (임베딩)                        │
└─────────────────────────────────────────────────┘
```

---

## 2. 모듈별 기술 명세

### 2.1 Phase A: Obsidian Vault 구조화

**담당**: 초기 설계, 모든 Phase 기초

#### 저장소 구조
```
SecondBrain/
├── 00-fleeting/           # 임시 노트 (수집 직후)
├── 01-literature/         # 문헌 노트 (원문 정보)
├── 02-permanent/          # 영구 노트 (핵심 지식)
├── 03-project/            # 프로젝트별 모음
├── 04-templates/          # 노트 템플릿
├── 05-attachments/        # 이미지, PDF 등
├── 06-index/              # 인덱스 & 맵
├── 07-archive/            # 아카이브 (분기별)
└── .obsidian/
    ├── plugins.json       # 플러그인 설정
    └── snippets/          # CSS 커스터마이징
```

#### Frontmatter 표준 스키마
```yaml
---
# 기본 정보
type: fleeting|literature|permanent|project
created: 2026-04-10T14:30:00Z
modified: 2026-04-10T14:30:00Z

# 수집 정보 (literature 전용)
source_url: https://...
source_title: 원문 제목
source_domain: arxiv.org | christian.or.kr | ...
source_date: 2026-04-10

# 분류
tags: [category, topic1, topic2]
domains: [기독교, 학술, 경제]
status: new | inbox | processing | completed

# 연결 정보
related: [note-id-1, note-id-2]  # 자동 생성
projects: [프로젝트명]

# AI 메타데이터
summary: 한 줄 요약
key_concepts: [개념1, 개념2]
embedding_updated: 2026-04-10
---
```

#### Claude Code 스킬 정의
- `/fleeting` — 수집된 원문 → 떠돌이 노트 변환
- `/literature` — 수집된 자료 → 문헌 노트 원자화
- `/permanent` — 문헌 노트 → 영구 노트 추상화
- `/lint` — 스키마 검증 및 정규화
- `/index` — 인덱스 페이지 자동 생성
- `/relate` — 노트 간 관계 자동 제안

**기술**:
- Obsidian Vault API
- Claude MCP (로컬 스킬 정의)
- Python 3.11+ (스크립트 자동화)

---

### 2.2 Phase B: n8n 수집 파이프라인

**담당**: 자동 수집, 주 1회 실행, **가장 먼저 작동 확인**

#### 아키텍처
```
n8n Workflow (주 1회 실행)
├── [Trigger] Cron Job (매주 월요일 09:00 KST)
├── [RSS 수집] MiniFlux → Fetch New Items
│   ├── 도메인1: 기독교 (5개 소스)
│   ├── 도메인2: 학술 (5개 소스)
│   └── 도메인3: 경제 (5개 소스)
├── [API 수집] ArXiv & yfinance
│   ├── ArXiv: 최근 "machine learning" 논문 10개
│   └── yfinance: 주요 ETF 시세 + 뉴스
├── [AI 처리] Claude API → /literature 스킬
│   ├── 각 수집 항목 → 원문 정보 추출
│   └── Obsidian Frontmatter 생성
├── [저장] Obsidian Vault API
│   └── 01-literature/ 폴더에 마크다운 생성
└── [알림] Slack/이메일 (완료 알림)
```

#### 기술 스택
| 컴포넌트 | 기술 | 상세 |
|---------|------|------|
| 스케줄 | n8n | Docker 컨테이너, 주 1회 |
| RSS 수집 | MiniFlux | RSS 피드 통합 |
| API | ArXiv API | 논문 검색 (무료) |
| API | yfinance | 주식 데이터 (무료) |
| 변환 | Claude API | 정보 추출 및 원자화 |
| 저장 | Obsidian API | 로컬 Vault에 마크다운 쓰기 |

#### 신뢰 소스 목록 (Phase B 초기화)

**기독교 도메인** (5개 소스)
- 목사님 추천 기독교 뉴스 매체
- 신학 학술지 RSS
- 교회 공지 및 설교록

**학술 도메인** (5개 소스)
- ArXiv.org (기술 논문)
- IEEE Xplore (학술지)
- 대학 오픈리소스 (GitHub Trending)

**경제 도메인** (5개 소스)
- 한국 금융 뉴스 (연합뉴스, 매경)
- ETF 추적 (yfinance)
- 암호화폐 기초 (데이터 기반)

#### 데이터 흐름
```
원문 (RSS/API)
    ↓
[n8n] 수집 & 검증
    ↓
[Claude] 원자화 (정보 추출)
    ↓
Frontmatter 생성
    ↓
[Obsidian] 01-literature/ 저장
    ↓
완료 알림 (Slack)
```

#### 성공 기준
- 주 1회 자동 실행 성공률 99%
- 매실행마다 5개 이상 노트 생성
- 수집 후 저장까지 소요 시간 < 30분

---

### 2.3 Phase C: Zettelkasten 지식 연결

**담당**: 노트 간 관계 자동화, 지식 그래프 구축

#### 아키텍처
```
새로운 문헌 노트
    ↓
[LightRAG] 임베딩 생성
    ↓
[Vector Search] 유사 노트 검색 (Top 10)
    ↓
[Claude] 관계 분석
    ├─ "이 노트는 X의 맥락"
    ├─ "Y 개념과 모순 없음"
    └─ "Z와 보완 관계"
    ↓
[Frontmatter] related 필드 업데이트
    ↓
[Obsidian] 자동 링크 생성
    ↓
사용자 피드백 (수동 수정) → 학습
```

#### 기술 스택
| 컴포넌트 | 기술 | 설정 |
|---------|------|------|
| 벡터 DB | LightRAG | Docker 기반, 로컬 배포 |
| 임베딩 | OpenAI Embedding | 대체: Claude Embedding |
| 검색 | Cosine Similarity | 유사도 > 0.7 필터링 |
| MCP | Zettelkasten MCP | 노트 관계 관리 |
| 저장소 | Obsidian | 링크 자동 생성 |

#### Zettelkasten 3단계 진화

| 단계 | 유형 | 특징 | 저장 위치 |
|------|------|------|---------|
| 1 | Fleeting (떠돌이) | 원문 그대로, 불완전 | 00-fleeting/ |
| 2 | Literature (문헌) | 원문 정보 + 메타 | 01-literature/ |
| 3 | Permanent (영구) | 핵심 개념 추상화 | 02-permanent/ |

**단계별 예시**:

Fleeting (원문):
```
머신러닝으로 주식 가격 예측...
```

Literature (원자화된 문헌 노트):
```yaml
---
type: literature
source_url: https://arxiv.org/abs/2401.12345
---

# 머신러닝 주식 가격 예측 모델

## 원문 정보
- 저자: Smith et al.
- 출판: arXiv 2024-01

## 주요 내용
- LSTM 기반 시계열 모델
- 예측 정확도: RMSE 2.3%
- 평균 예측 기간: 30일

## 핵심 개념
- 시계열 분석
- 신경망 예측
```

Permanent (영구 노트):
```yaml
---
type: permanent
---

# 금융 시장 예측 원리

## 정의
시계열 데이터 + 머신러닝으로 미래 가격 추정

## 기본 아이디어
1. 과거 패턴 학습 (LSTM, GRU)
2. 새로운 데이터로 예측
3. 예측 오차 역시 불가피 (확률론적)

## 관련 개념
- [[시계열 분석]]
- [[신경망 모델]]
- [[시장 효율성 가설]]

## 실무 적용 제약
- 과거 데이터 품질 의존
- 급변하는 시장 환경 반영 한계
```

#### 성공 기준
- 3개월 내 연결 노트 100개 이상
- 자동 연결 정확도 > 80% (사용자 수정 < 20%)

---

### 2.4 Phase D: 즉시 분석 시스템

**담당**: 온디맨드 보고서 생성, 5분 안에 응답

#### 아키텍처
```
사용자 질문 (한 줄)
    ↓
[LightRAG] 벡터 검색
    ├─ 관련 노트 추출 (Top 20)
    └─ 컨텍스트 구성
    ↓
[GPT Researcher] 보고서 생성
    ├─ 논거 수집
    ├─ 구조화
    └─ 마크다운 포맷
    ↓
[Claude API] 최종 검수
    ├─ 신뢰성 확인
    ├─ 출처 명시
    └─ 요약 생성
    ↓
사용자 반환 (마크다운)
```

#### 기술 스택
| 컴포넌트 | 기술 | 역할 |
|---------|------|------|
| 질문 입력 | Web UI (FastAPI + React) | 로컬/원격 |
| 검색 | LightRAG Vector DB | 노트 기반 검색 |
| 생성 | GPT Researcher | 보고서 템플릿 |
| 검수 | Claude API | 신뢰성 확인 |
| 저장 | Obsidian Vault | 분석 결과 기록 |

#### 보고서 포맷 (마크다운)

**기본 형식** (5분):
```markdown
# 쿼리: {사용자 질문}

## 요약
- 핵심 답변 (1~2문장)
- 근거 자료 3개

## 분석
### 배경
설명...

### 핵심 포인트
1. 포인트 1
2. 포인트 2

## 참고 자료
- [[노트1]] (관련도 95%)
- [[노트2]] (관련도 88%)
```

**선택 형식**:
- **슬라이드 형식**: JSON 변환 후 reveal.js로 렌더링
- **표 형식**: 비교 데이터 정렬

#### 응답 시간 SLA
- 쿼리 → 검색: < 1초
- 검색 → 생성: < 3분
- 생성 → 검수: < 1분
- **총 응답 시간**: < 5분

#### 성공 기준
- 응답 시간 SLA 95% 달성
- 사용자 만족도 4/5 이상

---

### 2.5 Phase E: Notion 공유 레이어

**담당**: 역할별 팀 배포 준비

#### 아키텍처
```
Obsidian Vault
    ↓
[Python 동기화 스크립트]
    ├─ Obsidian → JSON 변환
    └─ 권한 필터링 (역할별)
    ↓
Notion Database
    ├─ 관리자 (전체 보기)
    ├─ 도메인 담당자 (도메인별)
    └─ 뷰어 (요약만)
```

**기술**: Notion API + Python SDK

---

### 2.6 Phase F: Quartz 외부 공개 (선택)

**담당**: 지식 자산 공개 및 팀 협업 활성화

#### 아키텍처
```
Obsidian Vault (영구 노트 + 인덱스)
    ↓
[Quartz] 정적 사이트 생성
    ├─ 마크다운 → HTML
    └─ 자동 링크 생성
    ↓
GitHub Pages 배포
```

**기술**: Quartz v4 + GitHub Actions

---

## 3. 비기능 요구사항 (NFR)

### 3.1 성능 (Performance)

| 요구사항 | 목표 | 측정 방법 |
|---------|------|---------|
| 쿼리 응답 | < 5분 | 실시간 타이머 |
| 수집 파이프라인 | < 30분 | n8n 실행 로그 |
| Vault 용량 | 1GB 이내 | 월 1회 점검 |
| 벡터 검색 | < 1초 | LightRAG 메트릭 |

### 3.2 가용성 (Availability)

| 요구사항 | 목표 | 대응 |
|---------|------|------|
| n8n 자동 실행 | 99% | 실패 시 수동 트리거 |
| Vault 데이터 | 100% 백업 | Git 주 1회 커밋 |
| API 서비스 | 99.5% | 클라우드 이전 검토 |

### 3.3 보안 (Security)

| 요구사항 | 구현 |
|---------|------|
| 데이터 암호화 | Obsidian 기본 + Git 암호화 |
| API 키 관리 | .env 파일 (민감 정보) |
| 접근 제어 | 로컬 Vault (기본), Notion 권한 (팀) |
| 감사 로깅 | n8n 실행 로그 보존 |

### 3.4 확장성 (Scalability)

| 시나리오 | 설계 |
|---------|------|
| 노트 1000개 | 벡터 DB 인덱싱 최적화 |
| 사용자 5명 → 10명 | Notion 권한 확장, Quartz 배포 |
| 도메인 추가 | n8n 워크플로우 복제 |

### 3.5 유지보수성 (Maintainability)

| 요구사항 | 구현 |
|---------|------|
| 코드 문서화 | 스킬별 README |
| 의존성 관리 | requirements.txt, package.json |
| 모니터링 | n8n 대시보드 + Slack 알림 |
| 로깅 | 구조화된 로그 (JSON) |

---

## 4. 인터페이스 명세

### 4.1 사용자 인터페이스 (UI)

#### Phase A~D: Obsidian 기본 UI
- 플러그인: Dataview (쿼리), Graph View (관계), Template (템플릿)
- 커스터마이징: CSS Snippet으로 테마 정의

#### Phase E 이후: Web UI (선택)
```
GET /api/notes?query=...
POST /api/analysis (질문 전송)
GET /api/analysis/{id} (결과 조회)
```

**기술**: FastAPI + React

### 4.2 API 인터페이스

#### n8n Webhook
```
POST /webhook/collect
{
  "domain": "학술",
  "items": [
    {
      "title": "논문 제목",
      "url": "https://...",
      "date": "2026-04-10"
    }
  ]
}
```

#### Obsidian API
```python
from obsidian import Vault

vault = Vault("/path/to/SecondBrain")
note = vault.create_note(
    path="01-literature/note.md",
    frontmatter={
        "type": "literature",
        "source_url": "...",
        "domains": ["학술"]
    },
    content="내용..."
)
```

#### Claude MCP
```python
response = claude.skills.call(
    skill="/literature",
    params={
        "source_text": "원문...",
        "domain": "학술"
    }
)
```

### 4.3 데이터 저장소 인터페이스

#### Obsidian Vault (마크다운)
```
SecondBrain/
├── 01-literature/
│   ├── arxiv-2024-ml-001.md
│   ├── christian-news-2024-001.md
│   └── ...
└── 02-permanent/
    ├── machine-learning-basics.md
    └── ...
```

#### SQLite (메타데이터)
```sql
CREATE TABLE notes (
  id TEXT PRIMARY KEY,
  path TEXT,
  type TEXT,
  created TIMESTAMP,
  domains TEXT[],
  summary TEXT,
  embedding VECTOR(1536)
);

CREATE TABLE relationships (
  source_id TEXT,
  target_id TEXT,
  strength FLOAT,
  user_confirmed BOOLEAN
);
```

#### 벡터 저장소 (LightRAG)
- 임베딩 차원: 1536 (OpenAI)
- 검색 메트릭: 코사인 유사도
- 필터링: domains, created_date

---

## 5. 배포 및 운영

### 5.1 배포 환경
- **개발**: Windows 11 로컬 PC
- **운영**: 동일 PC (24/7 가동)
- **클라우드 검토**: 6개월 이후

### 5.2 Docker Compose 구성

```yaml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=***
    volumes:
      - ./n8n_data:/home/node/.n8n

  lightrag:
    image: lightrag/lightrag:latest
    ports:
      - "7860:7860"
    volumes:
      - ./lightrag_data:/data
    environment:
      - OBSIDIAN_PATH=/data/vault

  minixflux:
    image: miniflux/miniflux:latest
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=sqlite3:///data/miniflux.db
    volumes:
      - ./miniflux_data:/data
```

### 5.3 모니터링 및 알림
- n8n 실행 로그: 대시보드 확인
- Slack 알림: 수집 완료 / 오류 발생
- 주 1회 수동 점검: 데이터 품질 확인

### 5.4 백업 전략
- Obsidian Vault: Git 저장소 (주 1회 커밋)
- SQLite DB: 일일 백업
- 벡터 DB: 월 1회 내보내기

---

## 6. 개발 로드맵 요약

| Phase | 담당 스킬 | 예상 기간 | 완료 기준 |
|-------|---------|---------|---------|
| A | Claude Code | 1주 | 스키마 + 스킬 정의 완료 |
| B | n8n + Claude | 2주 | 주 1회 자동 수집 성공 |
| C | MCP + LightRAG | 2주 | 100개 노트 연결 달성 |
| D | LightRAG + API | 2주 | 5분 내 분석 결과 생성 |
| E | Notion API | 1주 | 역할별 권한 설정 완료 |
| F | Quartz | 1주 | 외부 공개 준비 (선택) |

---

## 7. 위험 및 대응

### 7.1 기술 위험

| 위험 | 영향 | 대응 |
|------|------|------|
| n8n 복잡도 증가 | 유지보수 난제 | 문서화 철저, 모듈화 설계 |
| LightRAG 성능 저하 | 응답 지연 | 로컬 캐싱, 배치 처리 |
| Claude API 비용 | 월 예산 초과 | 사용량 모니터링, 대체 모델 검토 |
| Obsidian Vault 용량 | 저장 공간 부족 | 분기별 아카이빙, 용량 계획 |

### 7.2 운영 위험

| 위험 | 영향 | 대응 |
|------|------|------|
| PC 다운타임 | 수집 중단 | 클라우드 이전 계획 (6개월) |
| 데이터 손상 | 작업 재수행 | Git 백업 + 월 1회 검증 |
| 소스 폐쇄 | 수집 불가 | 대체 소스 사전 준비 |

---

## 8. 다음 단계

1. **기술 검증**: Phase B (n8n) 프로토타입 개발
2. **스케줄 확정**: 각 Phase 구체적 시작/종료 날짜
3. **의존성 설치**: Docker, Python, n8n 로컬 환경 구성
4. **Phase A 완료**: Obsidian 스키마 + Claude 스킬 정의
