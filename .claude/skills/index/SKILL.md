# /index: 인덱스 페이지 자동 생성

Vault 전체를 스캔하여 도메인별, 태그별, 날짜별 인덱스 페이지를 생성한다.

---

## 활성화 트리거

- `/index` 명령 입력 시
- 주기적 자동 실행 (n8n 수집 완료 후)

---

## 입력 형식

```
/index              # 전체 인덱스 재생성
/index domain       # 도메인별 인덱스만
/index tags         # 태그별 인덱스만
/index date         # 날짜별 인덱스만
```

---

## 처리 과정

1. Vault 전체 .md 파일 스캔
2. Frontmatter 파싱 (type, domain, tags, created, index_code)
3. 분류 및 집계
4. 인덱스 파일 생성/업데이트 (`06-index/` 폴더)

---

## 생성 파일 목록

### index-by-domain.md
```markdown
# 도메인별 인덱스

최종 업데이트: 2026-04-10

## 기독교 (Christian) — 12개
### 영구 노트 (3개)
- [[A1-하나님의-사랑]] — 가족 관계의 성경적 기초
- [[A2-기도의-본질]] — 기도란 무엇인가

### 문헌 노트 (9개)
- [[2026-04-10-christian-sermon-family]] — 가족 설교
...

## 학술 (Academic) — 28개
...
```

### index-by-tag.md
```markdown
# 태그별 인덱스

## AI (15개)
- [[2026-04-10-academic-lightrag-graph-rag]] (literature)
- [[B1-transformer-attention]] (permanent)
...
```

### index-by-date.md
```markdown
# 최신 노트 (날짜별)

## 2026-04-10 (오늘, 5개)
- [[2026-04-10-academic-arxiv-ml]] (literature)
- [[2026-04-10-economy-spy-weekly]] (literature)
...
```

---

## 통계 출력

```
/index 완료 — 2026-04-10

Vault 통계:
  전체 노트: 42개
  - fleeting: 5개
  - literature: 32개
  - permanent: 5개
  - project: 0개

도메인별:
  - christian: 8개
  - academic: 18개
  - economy: 14개
  - general: 2개

생성된 인덱스:
  06-index/index-by-domain.md ✅
  06-index/index-by-tag.md ✅
  06-index/index-by-date.md ✅
```

---

## 규칙

- 기존 인덱스 파일은 덮어쓰기 (매번 재생성)
- 수동으로 작성한 내용이 인덱스 파일에 있으면 경고 후 덮어쓰기
- 파일 저장 경로: `{OBSIDIAN_VAULT_PATH}/06-index/`
