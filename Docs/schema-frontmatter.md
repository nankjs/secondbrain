# Frontmatter 스키마 표준

모든 노트는 아래 YAML frontmatter를 사용한다. 필수 필드는 반드시 포함.

---

## 공통 필드 (모든 노트 타입)

```yaml
---
# ── 필수 ──────────────────────────────────────────
type: fleeting | literature | permanent | project
created: 2026-04-10T14:30:00+09:00
modified: 2026-04-10T14:30:00+09:00
domain: christian | academic | economy | general

# ── 선택 ──────────────────────────────────────────
tags: []          # 키워드 태그 (예: [AI, 제텔카스텐, 주식])
status: inbox | processed | archived
---
```

---

## type: fleeting (떠돌이 노트)

```yaml
---
type: fleeting
created: 2026-04-10T14:30:00+09:00
modified: 2026-04-10T14:30:00+09:00
domain: christian | academic | economy | general
tags: []
status: inbox
# 처리 후 literature 또는 permanent로 업그레이드
---
```

---

## type: literature (문헌 노트)

```yaml
---
type: literature
created: 2026-04-10T14:30:00+09:00
modified: 2026-04-10T14:30:00+09:00
domain: christian | academic | economy | general
tags: []
status: inbox | processed

# 출처 정보 (필수)
source_url: https://...
source_title: "원문 제목"
source_author: "저자"
source_date: 2026-04-10
source_type: article | paper | video | podcast | book

# 자동 연결 (Phase C 이후)
related: []       # [[관련노트1]], [[관련노트2]]
---
```

---

## type: permanent (영구 노트)

```yaml
---
type: permanent
created: 2026-04-10T14:30:00+09:00
modified: 2026-04-10T14:30:00+09:00
domain: christian | academic | economy | general
tags: []
status: draft | published

# 인덱스 코드 (A=기독교, B=학술, C=경제, Z=일반)
index_code: A01   # 예: A01 = 기독교 첫 번째 영구 노트

# 기반 문헌 (어떤 literature 노트에서 왔는가)
sources: []       # [[문헌노트1]], [[문헌노트2]]
related: []       # [[영구노트1]], [[영구노트2]]
---
```

---

## type: project (프로젝트 노트)

```yaml
---
type: project
created: 2026-04-10T14:30:00+09:00
modified: 2026-04-10T14:30:00+09:00
domain: general
tags: []
status: active | on-hold | completed

project_name: "프로젝트명"
project_phase: planning | executing | reviewing | done
---
```

---

## 도메인 코드

| 코드 | 의미 | 인덱스 접두사 |
|------|------|-------------|
| christian | 기독교/신학 | A |
| academic | 학술/논문/기술 | B |
| economy | 경제/주식/금융 | C |
| general | 기타/일반 | Z |

---

## 파일명 규칙

```
{YYYY-MM-DD}-{domain}-{slug}.md

예시:
2026-04-10-academic-lightrag-graph-rag.md
2026-04-10-christian-sermon-family.md
2026-04-10-economy-spy-weekly-2026w15.md
```

---

## 검증 기준 (/lint 스킬)

| 검사 항목 | 규칙 |
|----------|------|
| type | 4가지 중 하나 |
| created | ISO 8601 형식 |
| domain | 4가지 코드 중 하나 |
| source_url | literature 타입이면 필수 |
| index_code | permanent 타입이면 필수, 형식: [A-Z][0-9]+ |
