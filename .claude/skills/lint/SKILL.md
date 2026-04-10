# /lint: Frontmatter 검증 및 정규화

Obsidian Vault 내 노트의 Frontmatter를 검증하고 수정 제안을 제공한다.

---

## 활성화 트리거

- `/lint` 명령 입력 시
- `/lint {파일경로}` — 특정 파일 검증
- `/lint all` — Vault 전체 검증

---

## 입력 형식

```
/lint                    # Vault 전체 검증
/lint 01-literature/    # 특정 폴더 검증
/lint {filename}.md     # 특정 파일 검증
```

---

## 검증 항목

| 항목 | 규칙 | 오류 코드 |
|------|------|---------|
| type | fleeting\|literature\|permanent\|project 중 하나 | E001 |
| created | ISO 8601 형식 (YYYY-MM-DDTHH:MM:SS+09:00) | E002 |
| domain | christian\|academic\|economy\|general 중 하나 | E003 |
| source_url | literature 타입이면 필수 | E004 |
| index_code | permanent 타입이면 필수, 형식: [A-Z][0-9]+ | E005 |
| 파일명 | 규칙 준수 여부 ({date}-{domain}-{slug}.md) | W001 |
| 태그 | 비어있으면 경고 | W002 |

---

## 출력 형식

```
/lint 검증 결과 — 2026-04-10

검증 파일: 42개
  ✅ 정상: 38개
  ❌ 오류: 3개
  ⚠️ 경고: 1개

─── 오류 목록 ───────────────────────────
[E001] 01-literature/2026-04-09-economy-spy.md
  → type 필드 누락. 추가 권장: type: literature

[E004] 01-literature/2026-04-10-academic-ml.md
  → source_url 누락 (literature 타입 필수)

[E005] 02-permanent/B01-zettelkasten.md
  → index_code 형식 오류. 현재: "B01", 권장: "B1"

─── 경고 목록 ───────────────────────────
[W002] 00-fleeting/2026-04-10-fleeting-idea.md
  → tags 비어있음

─── 자동 수정 가능 항목 ───────────────────
수정하시겠습니까? (y/n)
  - created 날짜 형식 정규화 (5개 파일)
```

---

## 규칙

- 오류(E)는 반드시 수정 필요
- 경고(W)는 권장 사항
- 자동 수정 가능한 항목은 사용자 확인 후 수정
- 수정 내역은 로그로 기록
