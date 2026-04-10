# 06-implementation-phases.md: 구현 Phase 계획

## 문서 정보
- **작성일**: 2026-04-10
- **버전**: 1.0
- **상태**: Draft

---

## 1. 개요

이 문서는 **Phase A ~ F**의 상세한 구현 계획을 기술한다.

- 각 Phase의 목표 및 산출물
- 일정 및 리소스
- 완료 기준
- 팀원 역할 분담

---

## 2. Phase 타임라인 개요

```
2026년 4월 ~ 2026년 6월 (9주 집중 개발)

┌──────────────────────────────────────────────────────────────┐
│ Week 1-2  │ Phase A: Obsidian 구조화 (병렬 준비)            │
├──────────────────────────────────────────────────────────────┤
│ Week 2-4  │ Phase B: n8n 수집 파이프라인 (★ 우선)          │
├──────────────────────────────────────────────────────────────┤
│ Week 4-6  │ Phase C: 지식 연결 (Phase B 완료 후)           │
├──────────────────────────────────────────────────────────────┤
│ Week 6-8  │ Phase D: 즉시 분석 (Phase C 병렬)              │
├──────────────────────────────────────────────────────────────┤
│ Week 8    │ Phase E: Notion 공유 (선택)                    │
├──────────────────────────────────────────────────────────────┤
│ Week 9    │ Phase F: Quartz 외부 공개 (선택, 낮은 우선)    │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Phase A: Obsidian Vault 구조화

### 목표
지식 저장소 기초 구축, Claude Code 스킬 정의, 개발 가이드라인 수립

### 기간
**2026-04-10 ~ 2026-04-24** (2주)

### 담당자
- **주담당**: 나 (개발자)
- **검토**: 없음 (혼자 수행)

### 산출물

| 항목 | 상세 | 위치 |
|------|------|------|
| Vault 초기화 | 폴더 구조 생성 | `/path/to/SecondBrain/` |
| Frontmatter 스키마 | YAML 표준 정의 | `docs/schema-frontmatter.md` |
| 4개 스킬 정의서 | `/fleeting`, `/literature`, `/lint`, `/index` | `docs/claude-skills/` |
| Obsidian 설정 | 플러그인, 템플릿, CSS | `.obsidian/` |
| Git 저장소 | 초기 커밋 | `github.com/...secondbrain` |
| 개발 가이드 | Phase B~F를 위한 체크리스트 | `docs/dev-guide.md` |

### 상세 작업 계획

#### Week 1 (2026-04-10 ~ 2026-04-16)

**Day 1-2: Vault 구조 설계**
```
Task A.1: Obsidian Vault 폴더 생성
  └─ 00-fleeting, 01-literature, ... 07-archive
     └─ 각 폴더에 README 작성

Task A.2: .gitignore 설정
  └─ .env, node_modules, .DS_Store 제외
  └─ /data 폴더 데이터 제외

Task A.3: Frontmatter 표준 문서화
  └─ 05-data-schema.md 참조하여 YAML 스키마 정의
  └─ 각 노트 유형별 필드 목록
```

**Day 3-4: Claude Code 스킬 정의**
```
Task A.4: /fleeting 스킬
  목적: 원문 수집 → 떠돌이 노트 변환
  입력: 원문 텍스트 + 도메인
  출력: Frontmatter + 구조화 텍스트
  테스트: 3개 샘플 노트 생성

Task A.5: /literature 스킬 (가장 중요)
  목적: 원문 → 문헌 노트 (원자화)
  입력: 원문 URL + 도메인
  출력: Frontmatter + 요약 + 핵심 개념
  테스트: 5개 샘플 노트 (다양한 소스)

Task A.6: /lint 스킬
  목적: Frontmatter 검증 및 정규화
  입력: 노트 파일
  출력: 오류 목록 + 수정 제안
  테스트: 오류 케이스 5개

Task A.7: /index 스킬
  목적: 인덱스 페이지 자동 생성
  입력: Vault 경로
  출력: index-by-domain.md, index-by-tag.md
  테스트: 샘플 Vault로 실행
```

**Day 5: Obsidian 커스터마이징**
```
Task A.8: 플러그인 설정
  ├─ Dataview (쿼리로 노트 표시)
  ├─ Graph View (관계도 시각화)
  ├─ Template (노트 템플릿)
  └─ 기타 필수 플러그인

Task A.9: CSS 커스터마이징
  └─ 테마, 폰트, 다크모드 설정

Task A.10: 단축키 설정
  └─ 자주 쓸 명령어 단축키 정의
```

**Day 6-7: Git 및 문서화**
```
Task A.11: Git 저장소 초기화
  └─ GitHub 저장소 생성
  └─ 초기 커밋 (Vault 기본 구조)
  └─ .gitignore 커밋

Task A.12: 개발 가이드 작성
  └─ Phase B~F의 작업 흐름 설명
  └─ 스킬 사용 예시
  └─ 트러블슈팅 가이드
```

#### Week 2 (2026-04-17 ~ 2026-04-23)

**Day 1-3: 스킬 통합 테스트**
```
Task A.13: /fleeting + /literature 통합 테스트
  └─ 샘플 원문 10개 처리
  └─ 결과 노트 Vault에 저장
  └─ 품질 확인

Task A.14: /lint 및 /index 통합 테스트
  └─ 생성된 노트 검증
  └─ 인덱스 페이지 생성
```

**Day 4-5: 템플릿 작성**
```
Task A.15: 노트 템플릿 생성
  ├─ template-fleeting.md
  ├─ template-literature.md
  ├─ template-permanent.md
  └─ template-project.md
  
  → 04-templates/에 저장
```

**Day 6-7: 최종 검토 및 완료**
```
Task A.16: Phase A 완료 체크리스트
  ☑ Vault 구조 완성
  ☑ 4개 스킬 작동 확인
  ☑ 샘플 노트 30개 생성 및 저장
  ☑ Git 저장소 운영 시작
  ☑ 문서화 완료

Task A.17: Phase B 준비
  └─ n8n 설치 확인
  └─ API 키 준비 (ArXiv, yfinance, Claude)
```

### 완료 기준

- **필수**: Obsidian Vault 4개 폴더 구조 + 4개 Claude 스킬 작동 확인
- **필수**: Git 저장소 설정 + 초기 커밋 완료
- **선택**: Obsidian 플러그인 및 CSS 커스터마이징

### 성공 지표

| 지표 | 목표 | 측정 |
|------|------|------|
| 스킬 작동률 | 100% | 각 스킬별 5회 테스트 |
| 샘플 노트 수 | 30개 이상 | Vault 직접 확인 |
| 문서 완성도 | 100% | 체크리스트 |

---

## 4. Phase B: n8n 수집 파이프라인 ★ 우선

### 목표
**주 1회 자동 수집** — 신뢰 소스에서 정보를 자동으로 모아서 Obsidian에 저장

### 기간
**2026-04-17 ~ 2026-05-01** (2주, Phase A와 병렬, A 완료 후 본격)

### 담당자
- **주담당**: 나 (개발자)
- **협력**: 없음

### 왜 가장 먼저?
> "날마다 새 정보가 자동 수집되어 Obsidian에 노트로 쌓인다"
> 
> 이 기능 없이는 세컨드브레인의 핵심 가치를 보여줄 수 없음.
> Phase B 완료 후 가장 먼저 "작동하는" 시스템이 된다.

### 산출물

| 항목 | 상세 | 위치 |
|------|------|------|
| n8n 워크플로우 | JSON | `n8n-workflows/collection-pipeline.json` |
| 신뢰 소스 목록 | 도메인별 20개 | `docs/trusted-sources.md` |
| n8n 설정서 | Docker Compose | `docker-compose.yml` |
| API 키 관리 | .env 파일 | `.env.example` |
| 실행 로그 | 첫 3주 로그 | `logs/collection-*.log` |

### 상세 작업 계획

#### Week 1 (2026-04-17 ~ 2026-04-23)

**Day 1-2: n8n Docker 설정 및 신뢰 소스 선정**
```
Task B.1: n8n 로컬 설치
  └─ docker-compose.yml에 n8n 추가
  └─ http://localhost:5678 접근 확인
  └─ 기본 워크플로우 템플릿 확인

Task B.2: 신뢰 소스 선정 (도메인별)
  
  기독교 도메인 (5개):
  1. 목사님 추천 뉴스
  2. 신학 저널 RSS
  3. 교회 공지
  4. 신앙 팟캐스트
  5. 설교 자료
  
  학술 도메인 (5개):
  1. ArXiv.org (기술 논문)
  2. IEEE Xplore (학술지)
  3. GitHub Trending
  4. Medium (기술 글)
  5. 대학 오픈리소스
  
  경제 도메인 (5개):
  1. 한국 금융 뉴스 (연합뉴스)
  2. 경제 신문 (매경)
  3. yfinance (주식)
  4. 암호화폐 뉴스
  5. 부동산 정보
```

**Day 3-4: n8n 워크플로우 설계 (Trigger + RSS)**
```
Task B.3: Cron 트리거 설정
  입력: 매주 월요일 09:00 KST
  출력: 워크플로우 실행 신호

Task B.4: MiniFlux 통합
  └─ docker-compose에 MiniFlux 추가
  └─ RSS 피드 20개 등록
  └─ 최신 기사 자동 수집 (REST API)

Task B.5: n8n 워크플로우 구성
  ├─ [Trigger] Cron (주 1회)
  ├─ [Step 1] MiniFlux: RSS 수집
  ├─ [Step 2] 데이터 정규화
  ├─ [Step 3] Claude API 호출 (/literature)
  ├─ [Step 4] Obsidian API 저장
  └─ [Step 5] Slack 알림
```

**Day 5-7: API 통합 (ArXiv, yfinance)**
```
Task B.6: ArXiv API 통합
  └─ 검색어: "machine learning", "transformer", "data science"
  └─ 지난 7일 논문 추출
  └─ 상위 5개 수집

Task B.7: yfinance API 통합
  └─ 주요 ETF (SPY, QQQ, IVV 등) 시세 데이터
  └─ 주간 뉴스 함께 수집

Task B.8: 데이터 검증 로직
  └─ 중복 제거 (이미 수집된 URL)
  └─ 유효성 검사 (URL, 메타데이터)
  └─ 도메인 자동 분류
```

#### Week 2 (2026-04-24 ~ 2026-05-01)

**Day 1-2: Claude API 연동 및 Obsidian 저장**
```
Task B.9: Claude /literature 스킬 연동
  입력: 원문 정보 (URL, 제목, 본문)
  출력: Frontmatter + 요약
  테스트: 각 도메인별 샘플 5개
  
  예시:
  Input:  ArXiv 논문 URL
  Output: 01-literature/2026-04-24-arxiv-ml-001.md
          (Frontmatter + 핵심 내용)

Task B.10: Obsidian 로컬 API 저장
  └─ 생성된 마크다운을 01-literature/에 저장
  └─ 파일 이름 규칙: {date}-{domain}-{title}.md
  └─ Obsidian 자동 감지 (vault reload)

Task B.11: 오류 처리 및 재시도 로직
  └─ API 타임아웃: 자동 재시도 (3회)
  └─ 저장 실패: 로그 기록 + Slack 알림
  └─ 부분 실패: 성공한 항목부터 저장
```

**Day 3-4: 실행 및 테스트**
```
Task B.12: 첫 자동 실행
  └─ 2026-04-27 (월요일 09:00) 첫 실행
  └─ 로그 모니터링
  └─ 생성된 노트 확인

Task B.13: 품질 검수
  ├─ 생성된 노트 5개 샘플 검토
  ├─ Frontmatter 정합성 확인
  ├─ 요약 정확도 평가
  └─ 필요시 프롬프트 수정

Task B.14: 로깅 및 모니터링 설정
  └─ n8n 실행 로그 저장
  └─ Slack #alerts 채널 알림
```

**Day 5: 운영 가이드 작성**
```
Task B.15: n8n 운영 매뉴얼
  ├─ 워크플로우 일시중지/재개 방법
  ├─ 수동 실행 방법
  ├─ 오류 발생시 대처 방법
  └─ API 비용 모니터링

Task B.16: Phase B 완료
  ☑ n8n 워크플로우 작동 확인
  ☑ 주 1회 자동 실행 성공 (3주 기록)
  ☑ Obsidian에 자동 노트 생성 확인
  ☑ Slack 알림 작동 확인
```

### 완료 기준

**필수**:
- n8n 워크플로우 실행 성공률 99% (3주 기록)
- 매 실행마다 5개 이상 노트 자동 생성
- 수집 → Claude 처리 → Obsidian 저장 전체 흐름 작동

**선택**:
- Slack 알림 설정
- 수동 실행 트리거 추가

### 성공 지표

| 지표 | 목표 | 측정 |
|------|------|------|
| 실행 성공률 | 99% | n8n 로그 확인 |
| 수집 자료 수 | 주 5개 이상 | Vault 노트 수 |
| 처리 시간 | < 30분 | n8n 대시보드 |
| 오류율 | < 1% | 실행 로그 |

### Phase B 후 기대 효과

✅ **매주 새로운 정보가 자동으로 쌓인다** — 세컨드브레인의 가장 기본 기능 작동
✅ **시간 절감** — 일일이 검색하던 작업 자동화
✅ **데이터 축적** — 3개월 후 100개 이상 노트 보유

---

## 5. Phase C: 지식 연결 (Zettelkasten)

### 목표
수집된 노트들을 자동으로 연결해서 지식 그래프 구축

### 기간
**2026-05-02 ~ 2026-05-16** (2주, Phase B 완료 후)

### 담당자
- **주담당**: 나 (개발자)

### 의존성
- **선행**: Phase A (스킬), Phase B (자동 수집)

### 산출물

| 항목 | 상세 | 위치 |
|------|------|------|
| Zettelkasten MCP | 설정 파일 | `mcp-config/zettelkasten.json` |
| LightRAG Docker | docker-compose 추가 | `docker-compose.yml` |
| 관계 분석 스킬 | `/relate` 스킬 정의 | `docs/claude-skills/relate.md` |
| 자동 연결 스크립트 | Python | `scripts/auto-linking.py` |
| 연결 결과 | 관계 그래프 | Obsidian Graph View |

### 상세 작업 계획

#### Week 1 (2026-05-02 ~ 2026-05-08)

**Day 1-2: LightRAG Docker 설치 및 임베딩**
```
Task C.1: LightRAG 설치
  └─ docker-compose에 lightrag 서비스 추가
  └─ http://localhost:7860 접근 확인
  └─ OpenAI API 키 설정

Task C.2: 기존 노트 임베딩
  └─ Phase B 수집 노트들 (100개 상정)
  └─ SQLite notes 테이블에서 읽기
  └─ 각 노트 → 1536차원 벡터 생성
  └─ LightRAG에 저장
```

**Day 3-4: 자동 유사도 검색**
```
Task C.3: 벡터 검색 스크립트
  입력: 새로운 문헌 노트
  처리:
    1. 노트 전문 읽기
    2. OpenAI Embedding으로 벡터화
    3. LightRAG에서 Top 20 유사 노트 검색
    4. 필터: 유사도 > 0.7
  출력: 후보 노트 목록

Task C.4: 관계 타입 정의 및 분류
  유형:
    - context: "A는 B의 배경"
    - extend: "A가 B를 확장"
    - contradict: "A가 B와 모순"
    - related: "관련 있음"
```

**Day 5-7: Claude MCP 관계 분석**
```
Task C.5: `/relate` Claude 스킬 정의
  입력:
    - 노트 A (새로 수집된 노트)
    - 노트 B (후보 관련 노트)
  처리:
    - Claude API 호출
    - 관계 분석 (유형, 강도, 설명)
  출력:
    - relation_type: "context" | "extend" | ...
    - strength: 0~1
    - description: 한 줄 설명
  
  예시:
  Q: "노트 A: 'Polars DataFrame'과 
       노트 B: 'Pandas 성능 비교'의 관계?"
  A: {
    "type": "related",
    "strength": 0.92,
    "description": "둘 다 데이터 처리 라이브러리 비교"
  }

Task C.6: 자동 연결 완전 실행
  └─ 모든 노트 쌍에 대해 관계 분석 (옵션: Top 20만)
  └─ SQLite relationships 테이블에 저장
  └─ Frontmatter related 필드 업데이트
```

#### Week 2 (2026-05-09 ~ 2026-05-16)

**Day 1-2: Obsidian 링크 생성**
```
Task C.7: Obsidian 자동 링크
  └─ Frontmatter related 필드를 읽고
  └─ 마크다운 [[노트명|설명]] 형식으로 변환
  └─ 본문 끝에 "## 관련 노트" 섹션 추가
  
  예시:
  ## 관련 노트
  - [[Pandas 성능 비교]] (related, 신뢰도 92%)
  - [[데이터 처리 기초]] (context, 신뢰도 88%)
```

**Day 3-4: 피드백 루프 및 학습**
```
Task C.8: 사용자 피드백 메커니즘
  └─ Obsidian에서 "이 연결 맞음" / "틀림" 표시
  └─ 피드백을 SQLite relationships.user_confirmed에 저장
  └─ Claude가 피드백 학습 (가중치 조정)

Task C.9: 품질 측정
  └─ 자동 연결 정확도 평가 (샘플 20개)
  └─ 목표: > 80% 정확도
  └─ 부족하면 프롬프트 개선 후 재실행
```

**Day 5: 최종 검증**
```
Task C.10: Obsidian Graph View 시각화
  └─ [[노트명]]으로 링크된 노트 네트워크 표시
  └─ 시각적 확인: 강하게 연결된 부분 있는가?
  └─ 고아 노트(연결 없음) 확인

Task C.11: 관계도 보고서
  ├─ 노트별 평균 연결 수: XX개
  ├─ 가장 중요한 노트: XXX (연결 수 YY)
  └─ 관계 타입별 분포
```

### 완료 기준

**필수**:
- LightRAG 벡터 저장소 구축 및 검색 작동
- 자동 연결 정확도 > 80%
- Obsidian 링크 생성 및 Graph View 시각화

**선택**:
- 피드백 학습 루프 구현

### 성공 지표

| 지표 | 목표 | 측정 |
|------|------|------|
| 임베딩 완성율 | 100% | LightRAG 저장 확인 |
| 연결 정확도 | > 80% | 샘플 검증 |
| 평균 연결 수 | 5개 이상 | 통계 |
| 처리 시간 | < 5분/노트 | 실행 시간 |

---

## 6. Phase D: 즉시 분석 (온디맨드)

### 목표
한 줄 질문 → 5분 내 분석 보고서 생성

### 기간
**2026-05-09 ~ 2026-05-23** (2주, Phase C와 병렬)

### 담당자
- **주담당**: 나 (개발자)

### 의존성
- **선행**: Phase A (스킬), Phase C (벡터 검색)

### 산출물

| 항목 | 상세 | 위치 |
|------|------|------|
| Web UI (선택) | FastAPI + React | `web-ui/` |
| 분석 API | Claude MCP | `skills/analyze.md` |
| GPT Researcher 연동 | 설정 | `config/researcher.yaml` |
| 분석 결과 저장 | 마크다운 | Obsidian |

### 상세 작업 계획

#### Week 1 (2026-05-09 ~ 2026-05-15)

**Day 1-2: 분석 API 설계**
```
Task D.1: `/analyze` Claude 스킬 정의
  입력:
    - 사용자 질문 (한 줄)
    - 필요한 관점 (선택)
    - 시간 범위 (선택)
  처리:
    1. 질문 파싱 (주제, 필터 추출)
    2. LightRAG 벡터 검색
    3. 관련 노트 30개 수집
    4. 컨텍스트 합성
    5. Claude로 최종 분석
  출력:
    - 마크다운 보고서
    - 근거 자료 링크
    - 신뢰도 평가

Task D.2: 벡터 검색 쿼리 최적화
  └─ 사용자 질문 → 검색 쿼리 변환
  └─ 필터: domains, 시간 범위
  └─ Top-K: 30 (요약용)
  └─ 임계값: 0.7
```

**Day 3-4: GPT Researcher 연동 (선택)**
```
Task D.3: GPT Researcher 통합 (선택)
  └─ LightRAG 결과 + GPT Researcher로 더 깊은 분석
  └─ 보고서 자동 구조화
  └─ 마크다운 생성

Task D.4: 보고서 템플릿
  ```
  # 쿼리: {{질문}}
  
  ## 요약
  {{1~2문장 답변}}
  
  ## 분석
  ### 배경
  {{컨텍스트}}
  
  ### 핵심 포인트
  {{3~5개 포인트}}
  
  ## 참고 자료
  {{링크}}
  ```
```

**Day 5-7: Web UI (선택)**
```
Task D.5: FastAPI 백엔드 (선택)
  POST /api/analyze
  {
    "query": "Python 데이터 라이브러리 비교",
    "domains": ["학술"],
    "time_range": "3개월"
  }
  
  Response:
  {
    "result": "마크다운 보고서",
    "time_seconds": 245,
    "sources_count": 20
  }

Task D.6: React 프론트엔드 (선택)
  ├─ 질문 입력창
  ├─ 로딩 바
  ├─ 마크다운 뷰어
  └─ 피드백 버튼 (유용함/유용하지 않음)
```

#### Week 2 (2026-05-16 ~ 2026-05-23)

**Day 1-2: 신뢰성 검수**
```
Task D.7: Claude 신뢰성 검증
  입력: 생성된 보고서
  검사:
    - 각 주장의 출처 확인
    - 논리적 모순 탐지
    - 가장 최신의 정보인가?
  출력: 수정 제안 또는 승인

Task D.8: 오류 처리
  └─ 검색 결과 부족: 최소 검색어 변경
  └─ API 타임아웃: 재시도
  └─ 생성 실패: 대체 템플릿 사용
```

**Day 3-4: 성능 테스트**
```
Task D.9: 응답 시간 테스트
  └─ 다양한 쿼리로 10회 실행
  └─ 평균 응답 시간 측정
  └─ 목표: 5분 이내

Task D.10: 품질 평가
  └─ 생성된 보고서 5개 샘플
  └─ 사용자 만족도 평가 (1~5점)
  └─ 목표: 4점 이상
```

**Day 5: 최종 검증**
```
Task D.11: 엔드-투-엔드 테스트
  시나리오 1: 개발자
    Q: "2026년 Python 데이터 라이브러리"
    → 5분 내 분석 보고서 생성
  
  시나리오 2: 목사님
    Q: "부모 자식 관계의 성경적 기초"
    → 신학 자료 + 설교 사례 종합
  
  시나리오 3: 대학생
    Q: "금융업 취업 면접 준비"
    → 면접 질문 + 경제 뉴스 통합

Task D.12: Phase D 완료
  ☑ 분석 API 작동
  ☑ 응답 시간 < 5분
  ☑ 보고서 품질 평가 완료
  ☑ 사용자 만족도 4/5 이상
```

### 완료 기준

**필수**:
- 분석 API 작동 (질문 → 보고서)
- 응답 시간 5분 이내 달성 (95% 확률)
- 사용자 만족도 4/5 이상

**선택**:
- Web UI 구현
- GPT Researcher 통합

---

## 7. Phase E: Notion 공유 레이어 (선택)

### 목표
역할별 팀 확장 가능성 검토

### 기간
**2026-05-24 ~ 2026-05-30** (1주)

### 담당자
- **주담당**: 나 (개발자)

### 산출물
- Notion API 동기화 스크립트
- Notion Database 템플릿
- 역할별 권한 설정

---

## 8. Phase F: Quartz 외부 공개 (선택, 낮은 우선)

### 목표
지식 자산 공개 및 포트폴리오 활용

### 기간
**2026-05-31 ~ 2026-06-06** (1주)

### 담당자
- **주담당**: 나 (개발자)

### 산출물
- Quartz 정적 사이트
- GitHub Pages 배포
- SEO 최적화

---

## 9. 전체 일정 (Gantt 차트)

```
            4월        5월        6월
         1 2 3 4   1 2 3 4   1 2 3 4
Phase A  ███
Phase B    ████ (우선)
Phase C      ████
Phase D      ████ (병렬)
Phase E          ███
Phase F            ███

주: 1 = 1~7일, 2 = 8~14일, ...
```

---

## 10. 리소스 및 예산

### 개발자 인력
- **전담**: 나, 1명
- **주당 시간**: 40시간 (풀타임)
- **총 소요**: 9주 × 40시간 = 360시간

### 외부 비용

| 항목 | 월간 예상 | 기간 | 합계 |
|------|---------|------|------|
| Claude API | $30 | 3개월 | $90 |
| OpenAI Embedding | $5 | 3개월 | $15 |
| GitHub (무료) | $0 | 3개월 | $0 |
| Docker (무료) | $0 | 3개월 | $0 |
| **합계** | **$35** | **3개월** | **$105** |

---

## 11. 위험 및 대응

| 위험 | 확률 | 영향 | 대응 |
|------|------|------|------|
| n8n 오류 | 중 | 높음 | 일일 모니터링 + 주간 수동 실행 |
| API 비용 폭증 | 저 | 중간 | 사용량 모니터링, 배치 처리 |
| 벡터 검색 부정확 | 중 | 중간 | 샘플 평가 후 프롬프트 개선 |
| Phase 지연 | 중 | 높음 | 우선순위: Phase B > C > D > E > F |

---

## 12. 성공 기준 (최종)

모든 Phase 완료 후:

- **매일 새 정보 자동 수집**: Obsidian 노트 주 5개 이상 생성
- **한 줄 질문 분석**: 5분 내 근거 있는 보고서 생성
- **노트 연결**: 3개월 내 100개 노트 이상 축적, 자동 연결 정확도 80% 이상
- **사용자 만족도**: 4/5 이상

---

## 13. 다음 단계

1. **Phase A 시작**: 2026-04-10 (지금)
2. **Phase B 우선**: 첫 자동 수집 2026-04-27 확인
3. **3개월 후 평가**: 2026-07-10 (모든 Phase 완료 후)
4. **클라우드 마이그레이션 계획**: 6개월 후 검토
