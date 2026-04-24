---
title: "세컨드브레인 아키텍처 가이드"
date: 2026-04-10
type: "guide"
project: "아바타 프로젝트 / 세컨드브레인"
---

# 세컨드브레인 아키텍처 가이드

> UI 접근 주소 · 자료 저장 위치 · 사용법 레퍼런스

---

## 1. UI — 접근 가능한 화면들

| 서비스 | 주소 | 용도 |
|--------|------|------|
| **n8n** | http://localhost:15678 | 수집 파이프라인 모니터링·수동 실행 |
| **MiniFlux** | http://localhost:8080 | RSS 피드 목록·수집된 기사 확인 |
| **LightRAG** | http://localhost:9621 | 지식 그래프 시각화·검색 테스트 |
| **Obsidian** | 앱 직접 실행 | 노트 작성·조회·편집 |
| **Quartz (공개)** | https://nankjs.github.io/secondbrain/ | 외부 공개 지식 사이트 |
| **Quartz (로컬)** | http://localhost:3333 | 공개 전 로컬 미리보기 |

> Docker 컨테이너가 내려가 있으면 `docker compose up -d` 실행 후 접속

---

## 2. 자료 저장 위치

### Obsidian Vault (노트 저장소)

```
C:/Users/kjswi/Documents/googleDrive/ObsiVault/
│
├── 00-fleeting/          ← 빠른 캡처 메모 (/fleeting 스킬)
│
├── 01-literature/        ← 수집된 문헌 노트 ★ 핵심 입구
│   ├── YYYY-MM-DD-academic-*.md    ArXiv 논문
│   ├── YYYY-MM-DD-economy-*.md     주식·ETF 시세
│   ├── YYYY-MM-DD-christian-*.md   기독교 자료
│   └── YYYY-MM-DD-gemini-*.md      Gemini 대화
│
├── 02-permanent/         ← 내 언어로 재구성한 영구 노트 (/permanent 스킬)
│
├── 03-resources/
│   └── analysis/         ← /analyze 스킬이 생성한 분석 보고서
│
├── 04-templates/         ← 노트 템플릿
├── 06-index/             ← /index 스킬이 생성한 인덱스 페이지
└── 07-archive/           ← 처리 완료 자료
```

### 프로젝트 루트 (코드·설정)

```
C:/KJS/AVARTA/secondBrain/
│
├── scripts/              ← 자동화 스크립트 전체
├── n8n-workflows/        ← n8n 워크플로우 JSON 백업
├── quartz/               ← 공개 사이트 소스
│   └── content/          ← Vault에서 복사된 공개 노트
└── Docs/                 ← 기획·운영 문서
```

### Docker 볼륨 (내부 DB)

| 볼륨 | 저장 내용 |
|------|---------|
| `lightrag_data` | 지식 그래프 + 벡터 임베딩 |
| `n8n_data` | 워크플로우·실행 이력 |
| `miniflux_db_data` | RSS 피드·수집 기사 |

---

## 3. 사용법

### 자동 수집 (n8n이 자동으로 실행)

매주 크론이 자동 실행하여 `01-literature/`에 노트를 생성합니다.

```
ArXiv AI 논문  →  01-literature/YYYY-MM-DD-academic-*.md
MiniFlux RSS   →  01-literature/YYYY-MM-DD-*.md
yfinance 시세  →  01-literature/YYYY-MM-DD-economy-*.md
```

**수동 실행:**
```
http://localhost:15678 → 워크플로우 선택 → ▶ 실행 버튼
```

---

### Gemini 대화 저장 (북마크릿)

```bash
# 1단계: 서버 실행 (터미널 유지)
cd C:/KJS/AVARTA/secondBrain
python scripts/gemini-webhook.py

# 2단계: Gemini(gemini.google.com)에서 대화 후
#        북마크바의 "→ Obsidian" 클릭
#        → 01-literature/YYYY-MM-DD-gemini-제목.md 저장
```

북마크릿 등록법: `scripts/gemini-bookmarklet.txt` 전체 복사 → 북마크 URL에 붙여넣기

---

### 노트 직접 작성 (Claude Code 스킬)

```
/fleeting   아이디어·링크 빠른 메모  →  00-fleeting/
/literature 읽은 글·자료 정리        →  01-literature/
/permanent  영구 지식으로 승격        →  02-permanent/
/lint       Frontmatter 오류 검사
/index      폴더별 인덱스 페이지 생성  →  06-index/
/relate     두 노트 간 관계 분석
/analyze    질문 기반 즉시 분석 보고서 →  03-resources/analysis/
```

---

### 지식 분석 (LightRAG 기반)

```bash
# 새 노트 추가 후 임베딩 업데이트 (LightRAG 서버 필요)
python scripts/embed-vault.py

# 특정 폴더만 임베딩
python scripts/embed-vault.py --folder 01-literature

# 질문으로 즉시 분석
python scripts/analyze.py "RAG와 전통 검색의 차이점"
python scripts/analyze.py "인덱스 펀드 전략" --domain economy
python scripts/analyze.py "성경 공부 방법" --domain christian --depth deep --save

# 벡터 검색 직접 사용
python scripts/vector-search.py "attention mechanism" --mode hybrid
```

**도메인 옵션:** `academic` · `christian` · `economy` · `all`
**깊이 옵션:** `quick` (top-10) · `standard` (top-30) · `deep` (top-50)

---

### Notion 동기화

```bash
# 영구 노트를 Notion에 동기화
python scripts/sync-notion.py --folder 02-permanent

# 문헌 노트 동기화
python scripts/sync-notion.py --folder 01-literature

# 전체 동기화 (01-literature + 02-permanent)
python scripts/sync-notion.py

# 목록만 확인 (실제 전송 없음)
python scripts/sync-notion.py --dry-run
```

Notion DB: 아바타 프로젝트 페이지 하위 `SecondBrain Vault`

---

### 공개 사이트 업데이트 (Quartz)

```bash
# 로컬 미리보기 (http://localhost:3333)
bash scripts/build-quartz.sh --serve

# 노트를 공개 사이트에 반영
cp "ObsiVault/02-permanent/내노트.md" quartz/content/02-permanent/
git add quartz/content/
git commit -m "노트 추가: 내노트"
git push
# → GitHub Actions가 자동 빌드·배포 (약 3분)
```

공개 URL: **https://nankjs.github.io/secondbrain/**
사이트 내리기: GitHub → Settings → Pages → Source → None

---

## 4. 전체 흐름

```
외부 자료 (자동)                    내 생각 (수동)
ArXiv / RSS / yfinance              /fleeting · /literature
Gemini 북마크릿                     Claude Code 직접 작성
        │                                    │
        └──────────── 01-literature/ ────────┘
                             │
                    embed-vault.py
                    (LightRAG 임베딩)
                             │
                    /analyze · vector-search.py
                             │
                   03-resources/analysis/
                   (분석 보고서 자동 저장)
                             │
                    /permanent 스킬
                    (영구 노트로 승격)
                             │
              ┌──────────────┴──────────────┐
              │                             │
     sync-notion.py                 build-quartz.sh
     Notion DB 동기화               GitHub Pages 배포
     (팀·내부 공유)                 (외부 공개)
```

---

## 5. 스크립트 빠른 참조

| 스크립트 | 실행 명령 | 용도 |
|---------|---------|------|
| `collect-arxiv.py` | `python scripts/collect-arxiv.py` | ArXiv 수동 수집 |
| `collect-yfinance.py` | `python scripts/collect-yfinance.py` | 시세 수동 수집 |
| `embed-vault.py` | `python scripts/embed-vault.py` | LightRAG 임베딩 |
| `analyze.py` | `python scripts/analyze.py "질문"` | 즉시 분석 |
| `vector-search.py` | `python scripts/vector-search.py "검색어"` | 벡터 검색 |
| `auto-linking.py` | `python scripts/auto-linking.py --dry-run` | 자동 링크 미리보기 |
| `sync-notion.py` | `python scripts/sync-notion.py` | Notion 동기화 |
| `gemini-webhook.py` | `python scripts/gemini-webhook.py` | 북마크릿 서버 |
| `build-quartz.sh` | `bash scripts/build-quartz.sh --serve` | 사이트 로컬 빌드 |

---


  ---         
  서비스별 로그인 정보 및 주의사항                                           
  ---
  
  n8n — http://localhost:15678

  ID: admin@secondbrain.local
  PW: secondbrain2026!A
  
  activation key : 2e42462e-2542-4e72-9915-064cd6ed90c2
  Copy and paste the license key into settings → usage → plan → enter activation key. You have 14 days to activate your license.

  n8nAPIkey : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlOWI2Njk5Ni0zMmVkLTQ5OTktYmFkNS0wMzE0YWIzZGRmNjQiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzc1ODI2NjAxfQ.bs1JpjsvY-WO9TybpaBzy6a1ibF8AvmrkSz7z3K6sjA

  ---
  MiniFlux — http://localhost:8080

  ID: admin
  PW: secondbrain2026

  ▎ API는 Basic Auth 방식, 웹 UI도 동일 계정으로 로그인

  ---
  LightRAG — http://localhost:9621

  로그인 없음 (auth_mode: disabled)
  바로 접속되며 웹 UI에서 그래프 시각화·검색 테스트 가능

  ---
  Obsidian

  로그인 없음 — Vault 경로만 열면 됨
  경로: C:/Users/kjswi/Documents/googleDrive/ObsiVault/

  ---
  Quartz 공개 사이트

  로그인 없음 — https://nankjs.github.io/secondbrain/

  ---
  주의사항 / 조치 필요 사항
  ---
  ┌───────────────────┬────────────────────────────┬────────────────────────────────────────────────────┐    
  │       항목        │            상태            │                        조치                        │    
  ├───────────────────┼────────────────────────────┼────────────────────────────────────────────────────┤    
  │ Docker 컨테이너   │ 현재 모두 정상 실행 중     │ PC 재시작 후 docker compose up -d 필요             │    
  ├───────────────────┼────────────────────────────┼────────────────────────────────────────────────────┤    
  │ Gemini 북마크릿   │ 자동 시작 안 됨            │ 사용 전 python scripts/gemini-webhook.py 수동 실행 │    
  │ 서버              │                            │  필요                                              │    
  ├───────────────────┼────────────────────────────┼────────────────────────────────────────────────────┤    
  │ LightRAG 임베딩   │ 새 노트 추가 시 자동 반영  │ 노트 추가 후 python scripts/embed-vault.py 수동    │    
  │                   │ 안 됨                      │ 실행 필요                                          │    
  ├───────────────────┼────────────────────────────┼────────────────────────────────────────────────────┤    
  │ MiniFlux RSS      │ HN, Reuters 일부 피드      │ 네트워크 문제 (Docker DNS), 현재 ArXiv·매일경제는  │    
  │                   │ 타임아웃                   │ 정상                                               │    
  └───────────────────┴────────────────────────────┴────────────────────────────────────────────────────┘    

  PC 재시작 후 복구 순서:
  cd C:/KJS/AVARTA/secondBrain
  docker compose up -d        # 모든 서버 재시작
  # 이후 각 서비스 정상 확인









*작성: Claude Sonnet 4.6 | 2026-04-10*
