# 06-tasks.md: 세컨드브레인 구현 TASKS

## 메타데이터

- **프로젝트명**: 세컨드브레인 (아바타 프로젝트)
- **생성일**: 2026-04-10
- **기반 문서**: `docs/planning/06-implementation-phases.md`
- **총 Phase**: 7개 (P0 + P1~P6)
- **총 Task**: 77개
- **MVP 우선순위**: **Phase B** (n8n 자동 수집)
- **상태**: 초안 (Draft)

---

## P0: 프로젝트 초기 설정

### P0-T1: Git 저장소 초기화

- **Status**: pending
- **Priority**: high
- **Dependencies**: 없음
- **Assignee**: 개발자
- **Description**: GitHub 저장소 생성, .gitignore 설정, 초기 커밋
- **Acceptance Criteria**:
  - [ ] GitHub 저장소 생성 완료 (github.com/...secondbrain)
  - [ ] `.gitignore` 파일 작성 (.env, node_modules, .DS_Store, /data 제외)
  - [ ] 초기 커밋 완료 (Vault 기본 구조)

### P0-T2: Docker Compose 기반 설정

- **Status**: pending
- **Priority**: high
- **Dependencies**: 없음
- **Assignee**: 개발자
- **Description**: docker-compose.yml 초기 파일 생성
- **Acceptance Criteria**:
  - [ ] `docker-compose.yml` 파일 생성 (PostgreSQL, Redis 포함)
  - [ ] 로컬 환경에서 `docker-compose up` 성공
  - [ ] 컨테이너 상태 정상 확인

### P0-T3: .env 환경 변수 설정

- **Status**: pending
- **Priority**: high
- **Dependencies**: P0-T1
- **Assignee**: 개발자
- **Description**: Claude API 키, OpenAI API 키, 기타 API 키 설정
- **Acceptance Criteria**:
  - [ ] `.env.example` 파일 작성 (template with dummy values)
  - [ ] 개인 `.env` 파일 생성 (로컬 개발용)
  - [ ] 모든 필수 API 키 환경 변수 설정

### P0-T4: 프로젝트 폴더 구조 생성

- **Status**: pending
- **Priority**: high
- **Dependencies**: P0-T1
- **Assignee**: 개발자
- **Description**: docs/, n8n-workflows/, scripts/, logs/ 폴더 생성
- **Acceptance Criteria**:
  - [ ] 폴더 구조 생성 완료 (모든 경로 확인)
  - [ ] 각 폴더에 README.md 작성
  - [ ] .gitkeep 파일 배치 (빈 폴더 git 추적)

---

## P1: Phase A — Obsidian Vault + Claude Code 스킬

**기간**: 2026-04-10 ~ 2026-04-24 (2주)
**담당**: 개발자
**우선순위**: high

### P1-T1: Obsidian Vault 폴더 구조 생성

- **Status**: pending
- **Priority**: high
- **Dependencies**: P0-T4
- **Assignee**: 개발자
- **Description**: 00-fleeting ~ 07-archive 폴더 + 각 README
- **Acceptance Criteria**:
  - [ ] 8개 폴더 생성 (00-fleeting, 01-literature, 02-permanent, 03-projects, 04-templates, 05-archive, 06-index, 07-resources)
  - [ ] 각 폴더별 README.md 작성
  - [ ] Obsidian vault 초기화 (.obsidian 폴더 생성)

### P1-T2: Frontmatter 스키마 정의

- **Status**: pending
- **Priority**: high
- **Dependencies**: P1-T1
- **Assignee**: 개발자
- **Description**: type/created/modified/domain/tags/source 등 YAML 스키마 문서화
- **Acceptance Criteria**:
  - [ ] `docs/schema-frontmatter.md` 작성 (모든 필드 정의)
  - [ ] 노트 유형별 필드 목록 작성 (fleeting/literature/permanent)
  - [ ] 샘플 Frontmatter 3개 제공

### P1-T3: /fleeting 스킬 정의

- **Status**: pending
- **Priority**: medium
- **Dependencies**: P1-T2
- **Assignee**: 개발자
- **Description**: 원문 수집 → 떠돌이 노트 변환 스킬 마크다운 작성
- **Acceptance Criteria**:
  - [ ] `docs/claude-skills/fleeting.md` 작성 (목적, 입력, 출력, 예시)
  - [ ] 스킬 테스트 3회 완료 (샘플 원문)
  - [ ] 생성된 노트 검증 완료

### P1-T4: /literature 스킬 정의 ★ 가장 중요

- **Status**: pending
- **Priority**: high
- **Dependencies**: P1-T2
- **Assignee**: 개발자
- **Description**: 원문 → 문헌 노트(원자화) 스킬 마크다운 작성. Phase B 자동 수집의 핵심
- **Acceptance Criteria**:
  - [ ] `docs/claude-skills/literature.md` 작성 (요약 + 핵심 개념 추출)
  - [ ] 다양한 도메인 샘플 5개로 테스트 (기독교, 학술, 경제 각 1~2개)
  - [ ] 생성 품질 평가 완료 (정확도 > 85%)

### P1-T5: /permanent 스킬 정의

- **Status**: pending
- **Priority**: medium
- **Dependencies**: P1-T2
- **Assignee**: 개발자
- **Description**: 문헌 노트 → 영구 노트 변환 스킬 마크다운 작성
- **Acceptance Criteria**:
  - [ ] `docs/claude-skills/permanent.md` 작성
  - [ ] 스킬 테스트 3회 완료
  - [ ] 영구 노트 포맷 검증 완료

### P1-T6: /lint 스킬 정의

- **Status**: pending
- **Priority**: medium
- **Dependencies**: P1-T2
- **Assignee**: 개발자
- **Description**: Frontmatter 검증 및 정규화 스킬 마크다운 작성
- **Acceptance Criteria**:
  - [ ] `docs/claude-skills/lint.md` 작성 (유효성 검사 규칙)
  - [ ] 오류 케이스 5개로 테스트
  - [ ] 수정 제안 자동화 확인

### P1-T7: /index 스킬 정의

- **Status**: pending
- **Priority**: medium
- **Dependencies**: P1-T2
- **Assignee**: 개발자
- **Description**: 인덱스 페이지 자동 생성 스킬 마크다운 작성
- **Acceptance Criteria**:
  - [ ] `docs/claude-skills/index.md` 작성
  - [ ] 샘플 Vault(10개 노트)로 인덱스 생성 테스트
  - [ ] domain/tag 별 인덱스 페이지 생성 확인

### P1-T8: Obsidian 플러그인 설정

- **Status**: pending
- **Priority**: low
- **Dependencies**: P1-T1
- **Assignee**: 개발자
- **Description**: Dataview, Graph View, Template, Templater 설치 및 설정
- **Acceptance Criteria**:
  - [ ] 4개 핵심 플러그인 설치 완료
  - [ ] 플러그인별 기본 설정 완료
  - [ ] 테스트 (Dataview 쿼리 작동 확인)

### P1-T9: 노트 템플릿 생성

- **Status**: pending
- **Priority**: medium
- **Dependencies**: P1-T2
- **Assignee**: 개발자
- **Description**: template-fleeting/literature/permanent/project.md 작성
- **Acceptance Criteria**:
  - [ ] 4개 템플릿 파일 생성 (04-templates/)
  - [ ] 각 템플릿에 Frontmatter + 기본 섹션 포함
  - [ ] Obsidian Template 플러그인 연동 확인

### P1-T10: 스킬 통합 테스트

- **Status**: pending
- **Priority**: high
- **Dependencies**: P1-T3, P1-T4, P1-T5, P1-T6, P1-T7
- **Assignee**: 개발자
- **Description**: /fleeting + /literature 샘플 10개 처리, /lint /index 통합 테스트
- **Acceptance Criteria**:
  - [ ] 샘플 원문 10개 → 노트 생성 완료
  - [ ] /lint 검증 통과율 100%
  - [ ] /index 인덱스 페이지 생성 확인 (3개)

### P1-T11: Phase A 완료 체크리스트

- **Status**: pending
- **Priority**: high
- **Dependencies**: P1-T10
- **Assignee**: 개발자
- **Description**: Vault 구조 확인, 스킬 작동 확인(5회/스킬), 샘플 노트 30개 생성 확인
- **Acceptance Criteria**:
  - [ ] 모든 8개 폴더 + README 확인
  - [ ] 각 스킬별 5회 이상 테스트 기록
  - [ ] Vault에 30개 이상 샘플 노트 저장 (4개 스킬)

**병렬 가능**: P1-T3, P1-T4, P1-T5, P1-T6, P1-T7 (동시 실행 가능)
**병렬 가능**: P1-T8, P1-T9 (P1-T1 완료 후 동시)

---

## P2: Phase B — n8n 수집 파이프라인 ★ MVP 최우선

**기간**: 2026-04-17 ~ 2026-05-01 (2주, Phase A와 병렬, A 완료 후 본격)
**담당**: 개발자
**우선순위**: **critical** (MVP 핵심)

### P2-T1: n8n Docker 설치

- **Status**: pending
- **Priority**: critical
- **Dependencies**: P0-T2
- **Assignee**: 개발자
- **Description**: docker-compose.yml에 n8n 서비스 추가. http://localhost:5678 접근 확인
- **Acceptance Criteria**:
  - [ ] docker-compose.yml에 n8n 서비스 추가
  - [ ] `docker-compose up n8n` 성공
  - [ ] http://localhost:5678 접근 가능

### P2-T2: MiniFlux Docker 설치

- **Status**: pending
- **Priority**: critical
- **Dependencies**: P0-T2
- **Assignee**: 개발자
- **Description**: docker-compose.yml에 MiniFlux RSS 리더 추가
- **Acceptance Criteria**:
  - [ ] docker-compose.yml에 miniflux 서비스 추가
  - [ ] http://localhost:8080 접근 가능
  - [ ] 기본 사용자 생성 완료

### P2-T3: 신뢰 소스 선정

- **Status**: pending
- **Priority**: critical
- **Dependencies**: 없음
- **Assignee**: 개발자
- **Description**: 기독교 5개, 학술 5개, 경제 5개 RSS/API 소스 목록 작성 (docs/trusted-sources.md)
- **Acceptance Criteria**:
  - [ ] `docs/trusted-sources.md` 작성 (15개 소스 목록)
  - [ ] 각 소스별 RSS URL/API endpoint 확인
  - [ ] 접근 가능성 검증 (5개 이상 테스트)

### P2-T4: MiniFlux RSS 피드 등록

- **Status**: pending
- **Priority**: critical
- **Dependencies**: P2-T2, P2-T3
- **Assignee**: 개발자
- **Description**: 선정된 20개 소스 MiniFlux에 등록
- **Acceptance Criteria**:
  - [ ] 20개 피드 등록 완료
  - [ ] 각 피드별 최신 기사 2개 이상 수집 확인
  - [ ] MiniFlux UI에서 피드 목록 표시 확인

### P2-T5: ArXiv API 통합

- **Status**: pending
- **Priority**: high
- **Dependencies**: P2-T1
- **Assignee**: 개발자
- **Description**: ArXiv 논문 수집 n8n 노드 구현. 검색어: ML/transformer/data science, 지난 7일 상위 5개
- **Acceptance Criteria**:
  - [ ] n8n ArXiv API 노드 구현
  - [ ] 검색어 3개 (ML, transformer, data science) 테스트
  - [ ] 지난 7일 논문 최대 5개 추출 확인

### P2-T6: yfinance API 통합

- **Status**: pending
- **Priority**: high
- **Dependencies**: P2-T1
- **Assignee**: 개발자
- **Description**: 주요 ETF(SPY/QQQ/IVV) 시세 + 주간 뉴스 수집 노드 구현
- **Acceptance Criteria**:
  - [ ] n8n yfinance 노드 구현
  - [ ] 3개 ETF 시세 데이터 추출 확인
  - [ ] 주간 뉴스 데이터 수집 확인

### P2-T7: n8n 워크플로우 설계

- **Status**: pending
- **Priority**: critical
- **Dependencies**: P2-T1, P2-T4
- **Assignee**: 개발자
- **Description**: Cron(주 1회 월요일 09:00 KST) → RSS수집 → 정규화 → Claude API → Obsidian 저장 → Slack 알림
- **Acceptance Criteria**:
  - [ ] n8n 워크플로우 설계 완료 (5개 스텝 이상)
  - [ ] Cron 트리거 설정 (매주 월요일 09:00 KST)
  - [ ] 각 스텝별 테스트 완료

### P2-T8: 데이터 중복 제거 로직

- **Status**: pending
- **Priority**: high
- **Dependencies**: P2-T7
- **Assignee**: 개발자
- **Description**: 이미 수집된 URL 체크, 유효성 검사, 도메인 자동 분류
- **Acceptance Criteria**:
  - [ ] 중복 URL 검사 로직 구현 (SQLite 활용)
  - [ ] 유효성 검사 (제목, 본문, URL)
  - [ ] 도메인 자동 분류 (기독교/학술/경제)

### P2-T9: Claude /literature 스킬 연동

- **Status**: pending
- **Priority**: critical
- **Dependencies**: P2-T7, P1-T4
- **Assignee**: 개발자
- **Description**: n8n에서 Claude API 호출하여 /literature 스킬 실행. 원문→노트 변환
- **Acceptance Criteria**:
  - [ ] n8n Claude API 노드 구현
  - [ ] /literature 스킬 연동 확인 (샘플 5개)
  - [ ] 생성된 노트 품질 검증 (정확도 > 80%)

### P2-T10: Obsidian 로컬 저장 연동

- **Status**: pending
- **Priority**: critical
- **Dependencies**: P2-T9
- **Assignee**: 개발자
- **Description**: 생성된 마크다운을 01-literature/에 저장. 파일명 규칙: {date}-{domain}-{title}.md
- **Acceptance Criteria**:
  - [ ] Obsidian 로컬 저장 경로 설정 (01-literature/)
  - [ ] 파일명 규칙 자동화 구현
  - [ ] 샘플 5개 저장 및 Obsidian 자동 감지 확인

### P2-T11: 오류 처리 및 재시도 로직

- **Status**: pending
- **Priority**: high
- **Dependencies**: P2-T10
- **Assignee**: 개발자
- **Description**: API 타임아웃 재시도(3회), 저장 실패 로그+Slack알림, 부분 실패 처리
- **Acceptance Criteria**:
  - [ ] API 타임아웃 재시도 로직 구현 (최대 3회)
  - [ ] 저장 실패 시 Slack 알림 설정
  - [ ] 부분 실패 처리 (성공 항목 저장, 실패 항목 로그)

### P2-T12: 첫 자동 실행 및 검수

- **Status**: pending
- **Priority**: critical
- **Dependencies**: P2-T11
- **Assignee**: 개발자
- **Description**: 2026-04-27(월) 첫 실행. 생성 노트 5개 샘플 검토. Frontmatter 정합성 확인
- **Acceptance Criteria**:
  - [ ] 2026-04-27 09:00 자동 실행 완료
  - [ ] 5개 이상 노트 생성 확인
  - [ ] Frontmatter 검증 (모든 필수 필드 존재)

### P2-T13: n8n 운영 매뉴얼 작성

- **Status**: pending
- **Priority**: medium
- **Dependencies**: P2-T12
- **Assignee**: 개발자
- **Description**: 워크플로우 일시중지/재개/수동실행/오류대처/API비용 모니터링 가이드
- **Acceptance Criteria**:
  - [ ] `docs/n8n-operations.md` 작성 (5개 섹션 이상)
  - [ ] 스크린샷 5개 이상 포함
  - [ ] 트러블슈팅 가이드 작성

### P2-T14: Phase B 완료 체크리스트

- **Status**: pending
- **Priority**: critical
- **Dependencies**: P2-T13
- **Assignee**: 개발자
- **Description**: 실행 성공률 99%(3주), 매 실행 5개+ 노트 생성, Slack 알림 작동 확인
- **Acceptance Criteria**:
  - [ ] 3주 실행 기록 (2026-04-27, 05-04, 05-11)
  - [ ] 실행 성공률 99% 이상 (최소 2/3 성공)
  - [ ] Slack 알림 작동 확인 (3회 이상)

**병렬 가능**: P2-T1, P2-T2, P2-T3 (동시 실행 가능)
**병렬 가능**: P2-T5, P2-T6 (동시 실행 가능)

---

## P3: Phase C — 지식 연결 Zettelkasten

**기간**: 2026-05-02 ~ 2026-05-16 (2주, Phase B 완료 후)
**담당**: 개발자
**우선순위**: high

### P3-T1: LightRAG Docker 설치

- **Status**: pending
- **Priority**: high
- **Dependencies**: P0-T2
- **Assignee**: 개발자
- **Description**: docker-compose.yml에 LightRAG 추가. http://localhost:7860 확인
- **Acceptance Criteria**:
  - [ ] docker-compose.yml에 lightrag 서비스 추가
  - [ ] http://localhost:7860 접근 가능
  - [ ] OpenAI API 키 설정 완료

### P3-T2: 기존 노트 임베딩

- **Status**: pending
- **Priority**: high
- **Dependencies**: P3-T1, P2-T14
- **Assignee**: 개발자
- **Description**: Phase B 수집 노트들 LightRAG에 임베딩. SQLite notes 테이블 연동
- **Acceptance Criteria**:
  - [ ] Phase B 수집 노트 (100개 상정) 임베딩 완료
  - [ ] SQLite notes 테이블에 저장 확인
  - [ ] 벡터 저장소 상태 점검 (저장된 벡터 수 확인)

### P3-T3: 벡터 검색 스크립트

- **Status**: pending
- **Priority**: high
- **Dependencies**: P3-T2
- **Assignee**: 개발자
- **Description**: 새 노트 → 벡터화 → LightRAG Top20 유사 검색 (유사도 > 0.7)
- **Acceptance Criteria**:
  - [ ] 검색 스크립트 구현 (Python)
  - [ ] 샘플 노트 3개로 Top20 검색 테스트
  - [ ] 유사도 필터 (> 0.7) 적용 확인

### P3-T4: 관계 타입 정의

- **Status**: pending
- **Priority**: high
- **Dependencies**: 없음
- **Assignee**: 개발자
- **Description**: context/extend/contradict/related 4가지 관계 타입 스키마 정의
- **Acceptance Criteria**:
  - [ ] `docs/relationship-types.md` 작성 (4가지 타입 정의)
  - [ ] 각 타입별 예시 3개 작성
  - [ ] SQLite schema 정의 (relationships 테이블)

### P3-T5: /relate 스킬 정의

- **Status**: pending
- **Priority**: high
- **Dependencies**: P3-T4
- **Assignee**: 개발자
- **Description**: 노트A + 노트B → 관계 분석 (타입, 강도 0~1, 설명) 스킬 마크다운 작성
- **Acceptance Criteria**:
  - [ ] `docs/claude-skills/relate.md` 작성
  - [ ] 스킬 테스트 5회 완료 (다양한 관계 유형)
  - [ ] 출력 포맷 검증 (type, strength, description)

### P3-T6: 자동 연결 스크립트

- **Status**: pending
- **Priority**: high
- **Dependencies**: P3-T3, P3-T5
- **Assignee**: 개발자
- **Description**: 모든 노트 쌍 관계 분석. SQLite relationships 테이블 저장. Frontmatter related 필드 업데이트
- **Acceptance Criteria**:
  - [ ] 자동 연결 스크립트 구현 (Python)
  - [ ] 샘플 노트 10개의 모든 쌍 분석 (최대 Top20)
  - [ ] SQLite relationships 테이블에 저장 확인

### P3-T7: Obsidian 링크 자동 생성

- **Status**: pending
- **Priority**: high
- **Dependencies**: P3-T6
- **Assignee**: 개발자
- **Description**: related 필드 → [[노트명|설명]] 마크다운 변환. "## 관련 노트" 섹션 추가
- **Acceptance Criteria**:
  - [ ] 마크다운 링크 변환 로직 구현
  - [ ] "## 관련 노트" 섹션 자동 추가
  - [ ] 샘플 노트 5개 확인 (Obsidian에서 링크 표시)

### P3-T8: 사용자 피드백 메커니즘

- **Status**: pending
- **Priority**: medium
- **Dependencies**: P3-T7
- **Assignee**: 개발자
- **Description**: Obsidian "연결 맞음/틀림" 표시 → SQLite relationships.user_confirmed 저장
- **Acceptance Criteria**:
  - [ ] Obsidian 플러그인 또는 메뉴 옵션 구현
  - [ ] 피드백 데이터 SQLite에 저장
  - [ ] 샘플 5개 피드백 저장 테스트

### P3-T9: 연결 정확도 평가

- **Status**: pending
- **Priority**: high
- **Dependencies**: P3-T8
- **Assignee**: 개발자
- **Description**: 샘플 20개 자동 연결 정확도 측정. 목표 > 80%. 부족 시 프롬프트 개선
- **Acceptance Criteria**:
  - [ ] 샘플 20개 노트 쌍의 자동 연결 정확도 측정
  - [ ] 정확도 > 80% 달성 또는 프롬프트 개선
  - [ ] 평가 보고서 작성 (docs/phase-c-accuracy.md)

### P3-T10: Obsidian Graph View 시각화 확인

- **Status**: pending
- **Priority**: medium
- **Dependencies**: P3-T9
- **Assignee**: 개발자
- **Description**: 링크된 노트 네트워크 시각적 확인. 고아 노트(연결 없음) 확인
- **Acceptance Criteria**:
  - [ ] Obsidian Graph View에서 네트워크 시각화 확인
  - [ ] 강하게 연결된 노트 그룹 확인
  - [ ] 고아 노트 목록 파악 및 분석

### P3-T11: Phase C 완료 체크리스트

- **Status**: pending
- **Priority**: high
- **Dependencies**: P3-T10
- **Assignee**: 개발자
- **Description**: LightRAG 검색 작동, 연결 정확도 > 80%, Graph View 시각화 확인
- **Acceptance Criteria**:
  - [ ] LightRAG 벡터 검색 테스트 (5회 이상)
  - [ ] 연결 정확도 > 80% 달성
  - [ ] Graph View 스크린샷 3개 이상 저장

**병렬 가능**: P3-T1, P3-T4 (동시 실행 가능)
**병렬 가능**: P3-T5, P3-T3 (P3-T2 완료 후 동시)

---

## P4: Phase D — 즉시 분석 온디맨드

**기간**: 2026-05-09 ~ 2026-05-23 (2주, Phase C와 병렬)
**담당**: 개발자
**우선순위**: high

### P4-T1: /analyze 스킬 정의

- **Status**: pending
- **Priority**: high
- **Dependencies**: P3-T2
- **Assignee**: 개발자
- **Description**: 질문 파싱 → LightRAG 검색(30개) → 컨텍스트 합성 → Claude 분석 → 마크다운 보고서
- **Acceptance Criteria**:
  - [ ] `docs/claude-skills/analyze.md` 작성
  - [ ] 스킬 입력/출력 형식 정의
  - [ ] 샘플 질문 3개로 테스트 (보고서 생성)

### P4-T2: 벡터 검색 쿼리 최적화

- **Status**: pending
- **Priority**: high
- **Dependencies**: P4-T1
- **Assignee**: 개발자
- **Description**: 사용자 질문 → 검색 쿼리 변환. 필터(domains/시간범위), Top-K=30, 임계값 0.7
- **Acceptance Criteria**:
  - [ ] 쿼리 변환 로직 구현
  - [ ] 필터링 (domain, time_range) 적용 확인
  - [ ] Top-K=30, 임계값 0.7 설정 확인

### P4-T3: 보고서 템플릿 정의

- **Status**: pending
- **Priority**: high
- **Dependencies**: 없음
- **Assignee**: 개발자
- **Description**: 쿼리/요약/배경/핵심포인트/참고자료 섹션 마크다운 템플릿 작성
- **Acceptance Criteria**:
  - [ ] `docs/report-template.md` 작성
  - [ ] 5개 섹션 정의 및 예시 제공
  - [ ] 샘플 보고서 1개 생성

### P4-T4: Claude 신뢰성 검증 로직

- **Status**: pending
- **Priority**: high
- **Dependencies**: P4-T2
- **Assignee**: 개발자
- **Description**: 생성 보고서의 출처 확인, 논리적 모순 탐지, 최신 정보 여부 확인
- **Acceptance Criteria**:
  - [ ] 출처 검증 로직 구현
  - [ ] 논리적 모순 탐지 로직 구현
  - [ ] 신뢰도 점수 산출 (0~1)

### P4-T5: 오류 처리

- **Status**: pending
- **Priority**: medium
- **Dependencies**: P4-T4
- **Assignee**: 개발자
- **Description**: 검색 결과 부족 시 쿼리 변경, API 타임아웃 재시도, 생성 실패 대체 템플릿
- **Acceptance Criteria**:
  - [ ] 검색 결과 부족 시 자동 쿼리 변경 (2회)
  - [ ] API 타임아웃 재시도 로직 (최대 3회)
  - [ ] 생성 실패 시 대체 템플릿 사용

### P4-T6: 엔드-투-엔드 테스트

- **Status**: pending
- **Priority**: high
- **Dependencies**: P4-T5
- **Assignee**: 개발자
- **Description**: 3개 시나리오: 개발자(Python라이브러리), 목사님(성경적 기초), 대학생(금융취업) 각 5분 이내
- **Acceptance Criteria**:
  - [ ] 시나리오 1 (개발자): Python 데이터 라이브러리 질문 → 5분 내 보고서
  - [ ] 시나리오 2 (목사님): 성경적 기초 질문 → 신학 자료 종합
  - [ ] 시나리오 3 (대학생): 금융 취업 질문 → 면접/뉴스 통합

### P4-T7: Phase D 완료 체크리스트

- **Status**: pending
- **Priority**: high
- **Dependencies**: P4-T6
- **Assignee**: 개발자
- **Description**: 분석 API 작동, 응답 시간 < 5분(95%), 사용자 만족도 4/5 이상
- **Acceptance Criteria**:
  - [ ] 분석 API 작동 확인 (10회 이상 테스트)
  - [ ] 평균 응답 시간 < 5분 (95% 이상)
  - [ ] 사용자 만족도 평가 (자체 평가 4/5 이상)

---

## P5: Phase E — Notion 공유 레이어 (선택)

**기간**: 2026-05-24 ~ 2026-05-30 (1주)
**담당**: 개발자
**우선순위**: low

### P5-T1: Notion API 연동 설정

- **Status**: pending
- **Priority**: low
- **Dependencies**: P4-T7
- **Assignee**: 개발자
- **Description**: Notion Integration 생성, API 키 설정
- **Acceptance Criteria**:
  - [ ] Notion Integration 생성 완료
  - [ ] API 키 환경 변수 설정 (.env)
  - [ ] API 연결 테스트 완료

### P5-T2: Notion Database 템플릿

- **Status**: pending
- **Priority**: low
- **Dependencies**: P5-T1
- **Assignee**: 개발자
- **Description**: 역할별(목사님/대학생/웹디자이너/사무원) Notion Database 구조 설계
- **Acceptance Criteria**:
  - [ ] 4개 Database 구조 설계 (역할별)
  - [ ] 각 Database에 5개 이상 속성 정의
  - [ ] 샘플 데이터 5개 입력

### P5-T3: Obsidian → Notion 동기화

- **Status**: pending
- **Priority**: low
- **Dependencies**: P5-T2
- **Assignee**: 개발자
- **Description**: 02-permanent 노트를 Notion에 자동 동기화 스크립트 (scripts/sync-notion.py)
- **Acceptance Criteria**:
  - [ ] `scripts/sync-notion.py` 작성
  - [ ] 샘플 노트 5개 동기화 테스트
  - [ ] 양방향 동기화 확인

### P5-T4: 역할별 권한 설정

- **Status**: pending
- **Priority**: low
- **Dependencies**: P5-T3
- **Assignee**: 개발자
- **Description**: 각 팀원 역할에 맞는 Notion 페이지 접근 권한 설정
- **Acceptance Criteria**:
  - [ ] Notion 공유 설정 (4개 팀원)
  - [ ] 역할별 접근 권한 제한 (읽기/쓰기)
  - [ ] 권한 설정 테스트 완료

### P5-T5: Phase E 완료 체크리스트

- **Status**: pending
- **Priority**: low
- **Dependencies**: P5-T4
- **Assignee**: 개발자
- **Description**: 동기화 작동 확인, 팀원 1명 Notion 접근 테스트
- **Acceptance Criteria**:
  - [ ] 자동 동기화 작동 확인 (테스트)
  - [ ] 팀원 1명 접근 테스트 완료
  - [ ] Notion → Obsidian 역동기화 가능 여부 확인

---

## P6: Phase F — Quartz 외부 공개 (선택, 낮은 우선)

**기간**: 2026-05-31 ~ 2026-06-06 (1주)
**담당**: 개발자
**우선순위**: low

### P6-T1: Quartz 설치 및 설정

- **Status**: pending
- **Priority**: low
- **Dependencies**: P4-T7
- **Assignee**: 개발자
- **Description**: Quartz v4 설치. 02-permanent 노트를 소스로 설정
- **Acceptance Criteria**:
  - [ ] Quartz v4 설치 완료
  - [ ] 02-permanent를 content 폴더로 설정
  - [ ] 로컬 빌드 성공 (http://localhost:3000)

### P6-T2: GitHub Pages 배포

- **Status**: pending
- **Priority**: low
- **Dependencies**: P6-T1
- **Assignee**: 개발자
- **Description**: Quartz → GitHub Pages 자동 배포 워크플로우 (.github/workflows/)
- **Acceptance Criteria**:
  - [ ] GitHub Actions 워크플로우 설정 (.github/workflows/deploy.yml)
  - [ ] 첫 배포 성공 (GitHub Pages URL 확인)
  - [ ] 자동 배포 트리거 설정 (push on main)

### P6-T3: SEO 최적화

- **Status**: pending
- **Priority**: low
- **Dependencies**: P6-T2
- **Assignee**: 개발자
- **Description**: 메타 태그, sitemap, robots.txt 설정
- **Acceptance Criteria**:
  - [ ] 메타 태그 설정 (title, description, og:*)
  - [ ] sitemap.xml 자동 생성 확인
  - [ ] robots.txt 작성

### P6-T4: Phase F 완료 체크리스트

- **Status**: pending
- **Priority**: low
- **Dependencies**: P6-T3
- **Assignee**: 개발자
- **Description**: 사이트 접근 확인, 노트 공개 여부 검증
- **Acceptance Criteria**:
  - [ ] 공개 URL에서 사이트 접근 가능
  - [ ] 최소 5개 노트 공개 표시
  - [ ] Google Search Console 등록 확인

---

## 의존성 그래프

```
P0-T1 (Git) → P0-T3, P0-T4
P0-T2 (Docker) → P2-T1, P2-T2, P3-T1
P0-T3, P0-T4 ─┐
              ├→ P1-T1 (Vault) → P1-T2 (Frontmatter)
              └─→ P1-T8, P1-T9

P1-T2 → P1-T3, P1-T4, P1-T5, P1-T6, P1-T7 (병렬) → P1-T10 → P1-T11
                  ↓
                P2-T9 (Claude 연동)

P2-T1, P2-T2 (병렬) → P2-T4 (병렬로 P2-T3과)
              ↓
P2-T1 → P2-T5, P2-T6 (병렬) ─┐
                              ├→ P2-T7 → P2-T8 → P2-T9 → P2-T10 → P2-T11 → P2-T12 → P2-T13 → P2-T14
P2-T4 ────────────────────────┘

P2-T14 → P3-T2 (임베딩) → P3-T3 (검색) → P3-T6 (자동연결) → P3-T7 (링크) → P3-T8 → P3-T9 → P3-T10 → P3-T11
P3-T1 → P3-T2
P3-T4 → P3-T5 → P3-T6

P3-T2 → P4-T1 (분석) → P4-T2 → P4-T3 (병렬) → P4-T4 → P4-T5 → P4-T6 → P4-T7
        P4-T3 (보고서 템플릿)

P4-T7 → P5-T1 (Notion, 선택) → P5-T2 → P5-T3 → P5-T4 → P5-T5
P4-T7 → P6-T1 (Quartz, 선택) → P6-T2 → P6-T3 → P6-T4
```

---

## 실행 순서 (Gantt 차트)

```
                        4월              5월              6월
                   10  17  24  01  08  15  22  29  05
P0 (준비)           ██ (즉시)
P1 (Phase A)        ████ (병렬 준비, 우선)
P2 (Phase B)          ████████ (★★ MVP, A와 병렬)
P3 (Phase C)              ████ (B 완료 후)
P4 (Phase D)                ████ (C와 병렬)
P5 (Phase E, 선택)           ██ (D 완료 후)
P6 (Phase F, 선택)            ██ (D 완료 후)

주: 각 칸은 1주(7일)를 의미
★★ Phase B는 Phase A 완료 후 본격, 병렬 작업 권장
```

---

## 작업 흐름 (Workflow)

### 1단계: P0 설정 (1주)
- 모든 팀원이 Git 저장소, Docker, .env 설정 확인
- 선행 조건: P0-T1 ~ P0-T4 모두 완료

### 2단계: P1 + P2 동시 진행 (3주)
- **P1 (Phase A)**: 개발자가 Obsidian Vault 구조 + Claude 스킬 정의 (2주)
- **P2 (Phase B)**: P1-T4 완료 후, n8n 자동 수집 구축 (2주)
- **병렬 가능**: P1과 P2는 겹칠 수 있음 (P1-T4 완료가 P2의 조건)

### 3단계: P3 + P4 (4주, 병렬 가능)
- **P3 (Phase C)**: P2 완료 후, 지식 연결 (2주)
- **P4 (Phase D)**: P3의 벡터 검색 기반, 분석 기능 (2주, P3과 병렬)

### 4단계: P5, P6 (선택, 2주)
- **P5 (Phase E)**: Notion 공유 (1주, 선택)
- **P6 (Phase F)**: Quartz 공개 (1주, 선택)

---

## 성공 지표 (Key Metrics)

### Phase별 성공 기준

| Phase | 지표 | 목표 | 측정 방법 |
|-------|------|------|---------|
| P0 | 설정 완료율 | 100% | 체크리스트 |
| P1 | 스킬 작동률 | 100% (5회/스킬) | 테스트 기록 |
| P2 | 실행 성공률 | 99% (3주 기록) | n8n 로그 |
| P2 | 주간 노트 생성 | 5개 이상 | Vault 직접 확인 |
| P3 | 연결 정확도 | > 80% | 샘플 평가 |
| P4 | 응답 시간 | < 5분 (95%) | 실행 시간 측정 |
| P4 | 사용자 만족도 | 4/5 이상 | 자체 평가 |
| P5 | 동기화 작동 | 100% | 테스트 |
| P6 | 배포 성공 | 100% | GitHub Pages 접근 |

### 최종 목표 (6개월 후)

- ✅ **매주 새 정보 자동 수집**: Obsidian 노트 주 5개 이상 생성
- ✅ **한 줄 질문 분석**: 5분 내 근거 있는 보고서 생성
- ✅ **노트 연결**: 100개 이상 노트 축적, 자동 연결 정확도 80% 이상
- ✅ **사용자 만족도**: 4/5 이상

---

## 노트

- **specialist 역할**: 각 Phase의 태스크는 개발자가 구현. specialist는 테스트 및 검증 담당 (필요시)
- **병렬 실행**: 명시된 "병렬 가능" 태스크는 동시 진행 권장 (효율성 증대)
- **Phase 병합**: 각 Phase 완료 후 orchestrator가 브랜치 병합 및 통합 테스트 수행
- **MVP 우선**: Phase B (n8n 자동 수집)가 가장 중요. Phase B 완료 시 "작동하는" 시스템 완성
- **선택 사항**: Phase E, F는 MVP 완성 후 추가 기능. 우선순위 낮음.

---

**문서 버전**: 1.0  
**생성일**: 2026-04-10  
**상태**: Draft (Ready for Review)
