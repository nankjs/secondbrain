# 05-data-schema.md: 데이터 구조 및 스키마

## 문서 정보
- **작성일**: 2026-04-10
- **버전**: 1.0
- **상태**: Draft

---

## 1. 개요

이 문서는 세컨드브레인의 모든 데이터 구조를 정의한다.

- **Obsidian Frontmatter 스키마** (마크다운 메타데이터)
- **노트 유형별 필드 명세**
- **저장소 폴더 구조**
- **메타데이터 저장소 (SQLite)** 구조

---

## 2. Obsidian Vault 폴더 구조

### 기본 폴더 레이아웃

```
SecondBrain/
├── 00-fleeting/              # Fleeting Notes (임시, 불완전)
│   ├── 2026-04-10-idea.md    # 원문 그대로
│   └── README.md             # 폴더 가이드
│
├── 01-literature/            # Literature Notes (원자화된 문헌)
│   ├── arxiv-2026-ml-001.md
│   ├── arxiv-2026-ml-002.md
│   ├── christian-news-2026-001.md
│   ├── finance-etf-2026-001.md
│   └── README.md
│
├── 02-permanent/             # Permanent Notes (영구 노트)
│   ├── machine-learning-basics.md
│   ├── zettelkasten-method.md
│   ├── financial-literacy.md
│   ├── biblical-hermeneutics.md
│   └── README.md
│
├── 03-project/               # 프로젝트별 모음
│   ├── project-job-search/
│   │   ├── resume.md
│   │   ├── target-companies.md
│   │   └── interview-prep.md
│   ├── project-sermon/
│   │   ├── 2026-q2-themes.md
│   │   └── biblical-studies.md
│   └── README.md
│
├── 04-templates/             # 노트 템플릿
│   ├── template-literature.md
│   ├── template-permanent.md
│   ├── template-project.md
│   └── README.md
│
├── 05-attachments/           # 이미지, PDF, 첨부파일
│   ├── images/
│   │   ├── 2026-04-arxiv-diagram.png
│   │   └── ...
│   ├── pdfs/
│   │   ├── paper-arxiv-2024.pdf
│   │   └── ...
│   └── README.md
│
├── 06-index/                 # 인덱스 & 맵
│   ├── index-all.md          # 전체 노트 목록 (자동 생성)
│   ├── index-by-domain.md    # 도메인별 인덱스
│   ├── index-by-tag.md       # 태그별 인덱스
│   ├── map-permanent.md      # 영구 노트 맵 (관계도)
│   └── README.md
│
├── 07-archive/               # 아카이브 (1년 이상 미사용)
│   ├── 2025-q1/              # 분기별 정리
│   ├── 2025-q2/
│   └── README.md
│
├── .obsidian/                # Obsidian 설정 (Git 포함)
│   ├── app.json              # 앱 설정
│   ├── appearance.json        # 테마, 폰트
│   ├── core.json              # 핵심 플러그인
│   ├── plugins.json           # 커뮤니티 플러그인
│   ├── snippets/
│   │   └── theme.css          # 커스텀 CSS
│   └── hotkeys.json           # 단축키
│
├── .gitignore                # Git 제외 목록
├── README.md                 # Vault 가이드
└── .env                      # API 키 (보안, Git 제외)
```

---

## 3. Frontmatter 표준 스키마

### 3.1 공통 필드 (모든 노트)

```yaml
---
# [필수] 노트 기본 정보
type: fleeting | literature | permanent | project  # 노트 유형
id: {{unique-id}}                                   # 고유 ID (UUID 또는 timestamp)
title: {{제목}}                                     # 노트 제목
created: 2026-04-10T14:30:00Z                      # 생성 시간 (ISO 8601)
modified: 2026-04-10T14:30:00Z                     # 수정 시간

# [선택] 메타데이터
author: {{작성자}}                                  # "나", "목사님" 등
status: new | inbox | processing | completed       # 처리 상태
priority: 1 | 2 | 3                                # 우선순위 (1=높음)

# [권장] 분류
tags: [tag1, tag2, tag3]                           # 자유 태그
domains: [기독교, 학술, 경제]                      # 도메인 (고정값)
categories: [subcategory]                          # 카테고리 트리

# [AI 메타데이터]
summary: 한 줄 요약                                 # AI 자동 생성
key_concepts: [개념1, 개념2]                       # 핵심 개념 추출
embedding_updated: 2026-04-10                      # 임베딩 업데이트 일시
trust_score: 0.95                                  # AI 신뢰도 (0~1)

# [관계 그래프]
related: []                                         # 관련 노트 (자동 생성)
---
```

### 3.2 Fleeting Note (임시)

```yaml
---
type: fleeting
id: fleeting-20260410-143000
title: 새로운 아이디어: Python 데이터 라이브러리
created: 2026-04-10T14:30:00Z
modified: 2026-04-10T14:30:00Z

status: inbox
priority: 2
tags: [idea, coding, python]
domains: [학술]

# Fleeting은 최소 필드로
---

# 새로운 아이디어: Python 데이터 라이브러리

Reddit에서 본 Polars가 pandas보다 빠르다는 얘기. 
자세히 알아봐야 함.

연결 가능 노트:
- [[데이터 처리 라이브러리]]
- [[성능 최적화]]
```

**특징**:
- 최소한의 구조 (원문 그대로)
- 불완전해도 됨
- 빠른 캡처 우선

---

### 3.3 Literature Note (문헌)

**이 형식이 가장 중요** — 수집된 모든 자료가 이 형식으로 변환됨

```yaml
---
type: literature
id: lit-arxiv-2024-ml-001
title: "Attention is All You Need: Transformers in 2026"
created: 2026-04-10T10:00:00Z
modified: 2026-04-10T10:00:00Z

# [필수] 출처 정보
source_url: https://arxiv.org/abs/2406.xxxxx
source_title: "Attention is All You Need"
source_domain: arxiv.org                  # 고정: arxiv.org | github.com | ...
source_date: 2024-06-15
source_author: "Vaswani et al."

# [수집 메타데이터]
collected_by: n8n-pipeline              # 수집 도구
collection_method: arxiv-api             # 수집 방식
collection_time: 2026-04-10T09:00:00Z   # 수집 시간

# 분류
tags: [transformer, attention, llm, arxiv]
domains: [학술]
categories: [machine-learning, neural-networks]

# 요약
summary: Transformer 아키텍처는 2024년 기준 여전히 기초가 됨. 
  시계열 데이터에 특화된 변형들이 많이 제안됨.
key_concepts: [transformer, self-attention, seq2seq, neural-architecture]

# 신뢰도
trust_score: 0.98                        # 학술 논문이므로 높음
source_credibility: academic-journal

# 상태
status: completed                        # 원자화 완료
priority: 2

# AI 메타데이터
embedding_updated: 2026-04-10T10:05:00Z
language: en
word_count: 3500
reading_time_minutes: 15

# 관계 (자동 생성)
related: []
---

# Attention is All You Need: Transformers in 2026

## 논문 정보
- **저자**: Ashish Vaswani et al.
- **출판**: arXiv (2024-06-15)
- **원문**: https://arxiv.org/abs/2406.xxxxx

## 핵심 내용

### 배경
Transformer는 2017년 제안 이후 NLP의 기본 아키텍처가 됨.
이 논문은 2024년 기준 최신 변형들을 종합 정리.

### 주요 아이디어
1. **Self-Attention 메커니즘**: 시퀀스 요소 간 직접 상호작용
2. **Parallel 처리**: RNN과 달리 병렬화 가능
3. **시계열 특화 변형**: Linformer, Performer, Flash-Attention 등

### 성능 지표
- BLEU 스코어: 기존 대비 +2.3%
- 학습 시간: 기존 대비 -40%
- 메모리 사용: 기존 대비 -25%

## 주요 결론
Transformer는 계속 발전하고 있으며, 효율성 개선이 핵심 방향.

## 관련 개념
- [[Self-Attention]]
- [[Sequence-to-Sequence]]
- [[Large Language Models]]
```

**필드 설명**:
- `source_domain`: 고정 데이터셋 (검색 & 필터링용)
- `trust_score`: AI가 자동 계산 (학술 > 뉴스 > 블로그)
- `embedding_updated`: 벡터 검색용
- `related`: Phase C에서 자동 생성

---

### 3.4 Permanent Note (영구)

**가장 추상화된 형식** — 개인의 핵심 지식

```yaml
---
type: permanent
id: perm-transformer-basics
title: "Transformer 아키텍처의 기본 원리"
created: 2026-03-15T08:00:00Z
modified: 2026-04-10T14:30:00Z

status: completed
priority: 1
tags: [transformer, architecture, deep-learning]
domains: [학술]
categories: [machine-learning]

summary: Transformer는 Self-Attention을 기반으로 시퀀스 데이터를 
  병렬 처리하는 신경망 아키텍처. 2017년 이후 NLP의 표준.
  
key_concepts: [self-attention, encoder-decoder, positional-encoding, 
               multi-head-attention, feed-forward-network]

# 이 노트는 개인 작성이므로 source는 없음
author: "나"
writing_time_minutes: 45

# 관계
related: []
---

# Transformer 아키텍처의 기본 원리

## 정의
시퀀스 데이터를 **Self-Attention** 메커니즘으로 병렬 처리하는 신경망 아키텍처.

## 핵심 아이디어

### 1. Self-Attention (자기 주의)
- 각 토큰이 시퀀스 내 모든 토큰과의 관계를 학습
- 수식: Attention(Q, K, V) = softmax(QK^T / √d_k)V
- 장점: 병렬화 가능, 장거리 의존성 캡처

### 2. Multi-Head Attention
- 다양한 "표현 부분공간"에서 주의 학습
- 8개 헤드로 다양한 관점 동시 처리

### 3. 위치 인코딩
- 시퀀스 순서 정보 보존 (RNN과 다른 점)
- 계산: PE(pos, 2i) = sin(pos/10000^(2i/d_model))

### 4. Encoder-Decoder 구조
```
입력 시퀀스
    ↓
[Encoder] (Self-Attention 스택)
    ↓
중간 표현
    ↓
[Decoder] (Cross-Attention + Self-Attention)
    ↓
출력 시퀀스
```

## 개인적 이해
처음엔 복잡해 보이지만, 본질은 "시퀀스의 각 위치가 다른 모든 위치를 볼 수 있다"는 아이디어.
이것이 RNN의 순차 처리 제약을 없애고 병렬화를 가능하게 함.

## 실무 활용
- NLP: BERT, GPT 기반
- Vision: ViT (Vision Transformer)
- 멀티모달: CLIP, LLaVA

## 관련 노트
- [[Self-Attention의 수학]]
- [[Positional Encoding 실구현]]
- [[BERT vs GPT 비교]]
- [[Transformer 성능 최적화]]

## 더 읽어보기
1. "Attention is All You Need" (원본 논문) — [[arxiv-2024-transformer-2024]]
2. "The Illustrated Transformer" (Jaylaminar) — [[blog-illustrated-transformer]]
```

**특징**:
- 개인이 쓴 말로 설명
- 추상화 (수식, 원리 강조)
- 다른 노트로의 링크 (Zettelkasten)

---

### 3.5 Project Note (프로젝트)

```yaml
---
type: project
id: proj-job-search-2026
title: "2026 취업 준비"
created: 2026-01-01T00:00:00Z
modified: 2026-04-10T14:30:00Z

status: processing
priority: 1
tags: [career, job-search, resume]
domains: [경제]
categories: [personal-development]

project_goal: 상반기 3개 회사 면접 진행, 하반기 입사
project_timeline: 2026-01-01 ~ 2026-12-31
project_owner: 나

summary: 개발자로 전직하기 위한 6개월 집중 준비 기간.
  기술 역량 + 경력 전환 스토리 개발.

# 하위 노트들
sub_notes:
  - proj-resume
  - proj-target-companies
  - proj-interview-prep
  - proj-portfolio

# 관련 일반 노트들
related: []
---

# 2026 취업 준비

## 프로젝트 목표
- 상반기: 기술 역량 강화 + 포트폴리오 2개
- 중반기: 대상 회사 3곳 선정 + 면접 준비
- 하반기: 면접 진행 및 입사

## 진행 상태
- [ ] 기술 역량 강화 (Python, ML, Web)
- [ ] 포트폴리오 프로젝트 1 (진행 중)
- [ ] 포트폴리오 프로젝트 2 (계획)
- [ ] 이력서 작성
- [ ] 대상 회사 분석
- [ ] 면접 준비

## 각 영역별 상세

### 1. 기술 역량
관련 노트: [[Python-데이터-과학]], [[Machine-Learning-기초]]

현재: 기본 수료, 고급 학습 중
목표: 2개월 내 고급 수료

### 2. 포트폴리오
진행 프로젝트 1: AI 챗봇 (진행 중)
진행 프로젝트 2: 예정

### 3. 이력서 & 커버레터
작성 상태: 초안
피드백: 대기

### 4. 기업 분석
대상 회사: [[Target-Company-1]], [[Target-Company-2]], [[Target-Company-3]]

## 타임라인
- 4월: 기술 역량 완성 + 포트폴리오 1 완성
- 5월: 포트폴리오 2 진행 + 기업 분석
- 6월: 이력서 최종 + 첫 면접
```

---

## 4. 태그 체계 (분류 표준)

### 4.1 도메인 태그 (고정값, `domains` 필드)

```
domains:
  - 기독교          # 신학, 설교, 신앙
  - 학술            # 논문, 학위론문, 기술 뉴스
  - 경제            # 금융, 주식, 경제 뉴스
```

**사용 규칙**:
- 각 노트는 1~3개 도메인 선택
- 고정값만 사용 (새로운 값 추가 금지, Phase 계획 필요)

### 4.2 자유 태그 (flexible)

```
tags:
  - [topic] machine-learning, transformer, neural-networks, ...
  - [source] arxiv, github, news, book, ...
  - [status] todo, in-progress, completed, on-hold
  - [method] tutorial, research, opinion, howto
  - [entity] company-name, person-name, technology-name
```

**명명 규칙**:
- 소문자 + 하이픈 (kebab-case)
- 의미 있는 이름 (한글 가능)
- 관련 있는 것만 선택 (5개 이하 권장)

### 4.3 카테고리 (계층적)

```
categories:
  machine-learning/
    ├─ neural-networks
    ├─ nlp
    ├─ computer-vision
    └─ time-series
  
  finance/
    ├─ stocks
    ├─ crypto
    ├─ etf
    └─ risk-management
  
  theology/
    ├─ biblical-studies
    ├─ church-history
    └─ pastoral-care
```

---

## 5. SQLite 메타데이터 저장소

**목적**: Obsidian 검색 보조, 빠른 쿼리 지원

### 5.1 테이블 구조

#### `notes` 테이블
```sql
CREATE TABLE notes (
  id TEXT PRIMARY KEY,
  vault_path TEXT NOT NULL,          -- "01-literature/arxiv-2024.md"
  title TEXT NOT NULL,
  type TEXT NOT NULL,                -- "fleeting" | "literature" | "permanent" | "project"
  created TIMESTAMP NOT NULL,
  modified TIMESTAMP NOT NULL,
  author TEXT,
  status TEXT,                       -- "new" | "inbox" | "processing" | "completed"
  domains TEXT,                      -- JSON: ["학술", "경제"]
  tags TEXT,                         -- JSON: ["tag1", "tag2"]
  summary TEXT,
  trust_score REAL,                  -- 0~1
  source_url TEXT,
  source_domain TEXT,
  word_count INTEGER,
  reading_time_minutes INTEGER,
  embedding_updated TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_type ON notes(type);
CREATE INDEX idx_domains ON notes(domains);
CREATE INDEX idx_created ON notes(created);
CREATE INDEX idx_source_domain ON notes(source_domain);
```

#### `relationships` 테이블
```sql
CREATE TABLE relationships (
  source_id TEXT NOT NULL,          -- 출발 노트
  target_id TEXT NOT NULL,          -- 도착 노트
  relation_type TEXT NOT NULL,      -- "context" | "extend" | "contradict" | "related"
  strength REAL NOT NULL,           -- 0~1 신뢰도
  description TEXT,                 -- 관계 설명 (한 줄)
  user_confirmed BOOLEAN DEFAULT FALSE,  -- 사용자 피드백 유무
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  PRIMARY KEY (source_id, target_id),
  FOREIGN KEY (source_id) REFERENCES notes(id),
  FOREIGN KEY (target_id) REFERENCES notes(id)
);

CREATE INDEX idx_source ON relationships(source_id);
CREATE INDEX idx_target ON relationships(target_id);
```

#### `embeddings` 테이블
```sql
CREATE TABLE embeddings (
  note_id TEXT PRIMARY KEY,
  embedding BLOB,                   -- 1536차원 벡터 (float32 array)
  model_name TEXT,                  -- "text-embedding-3-large"
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (note_id) REFERENCES notes(id)
);

CREATE INDEX idx_embedding_updated ON embeddings(updated_at);
```

#### `search_queries` 테이블 (선택)
```sql
CREATE TABLE search_queries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  query TEXT NOT NULL,
  query_embedding BLOB,
  results_count INTEGER,
  response_time_seconds REAL,
  user_feedback REAL,               -- 1~5 별점
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5.2 쿼리 예시

```sql
-- 최근 한 달 학술 노트 조회
SELECT * FROM notes
WHERE domains LIKE '%학술%'
  AND type = 'literature'
  AND created >= datetime('now', '-30 days')
ORDER BY created DESC;

-- 신뢰도 높은 노트 조회
SELECT * FROM notes
WHERE type = 'literature'
  AND trust_score > 0.8
ORDER BY trust_score DESC
LIMIT 20;

-- 특정 노트와 관련된 모든 노트
SELECT n.* FROM notes n
JOIN relationships r ON (r.target_id = n.id OR r.source_id = n.id)
WHERE (r.source_id = 'note-id' OR r.target_id = 'note-id')
  AND r.strength > 0.7;

-- 도메인별 노트 수
SELECT domains, COUNT(*) as count
FROM notes
GROUP BY domains
ORDER BY count DESC;
```

---

## 6. 벡터 저장소 (LightRAG)

### 구조

```
노트 ID → [문헭 텍스트] → OpenAI Embedding API → 벡터 (1536차원)
                                                        ↓
                                            LightRAG 벡터 저장소
```

### 저장 형식

```json
{
  "note_id": "lit-arxiv-2024-ml-001",
  "embedding": [0.123, -0.456, ..., 0.789],  // 1536개 실수
  "metadata": {
    "title": "Attention is All You Need",
    "domains": ["학술"],
    "created": "2026-04-10T10:00:00Z",
    "trust_score": 0.98
  }
}
```

### 검색 쿼리

```python
# 벡터 검색 (코사인 유사도)
query = "Transformer 아키텍처"
query_embedding = embedding_model.encode(query)

results = vector_store.search(
    query_embedding=query_embedding,
    k=20,                           # Top 20
    filters={
        "domains": ["학술"],
        "created": {"gte": "2024-04-01"}
    },
    threshold=0.7                   # 유사도 > 0.7만
)

# 결과: [
#   {"note_id": "...", "score": 0.95, "title": "..."},
#   {"note_id": "...", "score": 0.88, "title": "..."},
#   ...
# ]
```

---

## 7. 예시 노트 전체 (Literature)

### 파일명
```
01-literature/2026-04-10-arxiv-ml-attention.md
```

### 전체 콘텐츠

```yaml
---
type: literature
id: lit-arxiv-2024-attention-001
title: "Attention Mechanisms in Modern Deep Learning"
created: 2026-04-10T10:00:00Z
modified: 2026-04-10T10:00:00Z

# 출처
source_url: https://arxiv.org/abs/2406.xxxxx
source_title: "Attention Mechanisms in Modern Deep Learning"
source_domain: arxiv.org
source_date: 2024-06-15
source_author: "Various Researchers"

# 수집
collected_by: n8n-arxiv-pipeline
collection_method: arxiv-api
collection_time: 2026-04-10T09:00:00Z

# 분류
tags: [attention, transformer, deep-learning, arxiv, 2024]
domains: [학술]
categories: [machine-learning, neural-networks]

# 요약
summary: "Attention 메커니즘은 2017년 Transformer 논문 이후 
  딥러닝의 핵심 기술이 됨. 이 논문은 2024년 기준 최신 
  Attention 변형들을 종합 정리한 서베이."
  
key_concepts: 
  - attention-mechanism
  - self-attention
  - transformer
  - multi-head-attention
  - efficient-attention

# 신뢰
trust_score: 0.97
source_credibility: academic-preprint

# 상태
status: completed
priority: 2

# AI 메타
embedding_updated: 2026-04-10T10:05:00Z
language: en
word_count: 4200
reading_time_minutes: 18

# 관계 (Phase C 자동 생성)
related: []
---

# Attention Mechanisms in Modern Deep Learning

## 논문 기본 정보
- **저자**: 논문 저자들
- **출판**: arXiv (2024-06-15)
- **링크**: https://arxiv.org/abs/2406.xxxxx
- **인용**: XXX번

## 요약

이 서베이 논문은 Attention 메커니즘의 발전 역사와 
2024년 기준 최신 변형들을 다룬다.

### 핵심 내용

1. **Self-Attention의 발전**
   - 기본 Attention (2015)
   - Multi-Head Attention (2017)
   - Efficient Attention (2020+)

2. **최신 변형들**
   - Linear Attention (Linear complexity)
   - Sparse Attention (특정 위치만 주의)
   - Cross-Attention (이미지-텍스트 등)

3. **성능 비교**
   표: 다양한 Attention 방식의 시간·공간 복잡도

4. **실무 응용**
   - NLP: BERT, GPT-4
   - Vision: ViT, DINOv2
   - Multimodal: CLIP, LLaVA

## 개인 노트

이 논문은 Attention의 진화를 잘 정리했음. 
특히 Efficient Attention이 중요한데, 
실제로 산업에서는 성능과 속도의 트레이드오프를 
신중히 고려해야 함을 배웠다.

## 관련 노트
- [[Transformer-Architecture]]
- [[Self-Attention-Mathematics]]
- [[Efficient-Transformers]]
- [[BERT vs GPT]]

---

**노트 작성일**: 2026-04-10
**마지막 업데이트**: 2026-04-10
```

---

## 8. 데이터 마이그레이션 & 유지보수

### 스키마 버전 관리

```
v1.0: 초기 스키마 (2026-04-10)
  ├─ Frontmatter 기본 필드
  ├─ SQLite 4개 테이블
  └─ 벡터 임베딩 1536차원

v1.1 계획 (6개월 후)
  └─ 새로운 필드 추가 (사용자 피드백, 중요도 등)

v2.0 계획 (1년 후)
  └─ 다중 사용자 지원 (생성자, 공유자 등)
```

### 필드 추가 절차

1. **계획**: 필드 용도 및 형식 결정
2. **문서화**: 이 스키마 문서 업데이트
3. **마이그레이션**: 기존 노트에 기본값 추가
4. **테스트**: 검색, 분석 영향도 확인
5. **배포**: 모든 환경에 반영

---

## 9. 데이터 품질 규칙

### Literature 노트 체크리스트

- [ ] `source_url` 유효한 링크 (HTTP 검증)
- [ ] `source_domain` 고정값 목록 중 선택
- [ ] `summary` 3~5문장, 한국어 가능
- [ ] `key_concepts` 3~10개 개념
- [ ] `trust_score` 0.7 이상 (낮으면 수동 검토)
- [ ] `created` 과거 날짜 (미래는 불가)

### Permanent 노트 체크리스트

- [ ] `title` 관사 없는 개념명
- [ ] `summary` 개인적 이해 포함
- [ ] `related` 최소 3개 이상 연결
- [ ] `categories` 적절한 계층 선택

---

## 10. 다음 단계

1. **Obsidian 볼트 초기화**: Phase A에서 이 스키마 적용
2. **템플릿 생성**: 04-templates/에 각 노트 유형 템플릿
3. **데이터 검증 스크립트**: `lint` 스킬로 자동 검사
4. **문서화**: 사용자 가이드 작성
