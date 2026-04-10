# /permanent: 영구 노트 생성

문헌 노트들을 종합하여 내 언어로 재작성된 영구 노트를 생성한다.
세컨드브레인의 핵심 자산 — Notion/Quartz로 공유되는 지식.

---

## 활성화 트리거

- `/permanent` 명령 입력 시
- 사용자가 "이 노트들 영구 노트로 만들어줘" 요청 시

---

## 입력 형식

```
/permanent [도메인]
기반 노트: [[노트1]], [[노트2]], ...
주제: {영구 노트로 만들 핵심 주제}
```

---

## 처리 과정

1. 기반 문헌 노트들 읽기
2. 공통 주제 식별
3. **내 언어로 재작성** (원문 의존 없이 독립적으로 이해 가능하게)
4. 인덱스 코드 부여:
   - 도메인별 현재 최대 번호 확인
   - christian → A{N}, academic → B{N}, economy → C{N}, general → Z{N}
5. Frontmatter 생성 (type: permanent)
6. 파일명: `{인덱스코드}-{slug}.md`
7. `02-permanent/` 폴더에 저장

---

## 출력 형식

```markdown
---
type: permanent
created: {ISO8601}
modified: {ISO8601}
domain: {christian|academic|economy|general}
tags: [{태그 목록}]
status: draft

index_code: {A|B|C|Z}{번호}
sources: [{기반 문헌 노트 링크}]
related: []
---

# {핵심 주제 제목}

{핵심 아이디어를 내 언어로 2~4단락 설명}

## 핵심 주장

{1~3개 핵심 명제}

## 연결 아이디어

- [[관련 영구 노트]] — {관계 설명}

## 참고 문헌

- [[문헌 노트 1]]
- [[문헌 노트 2]]
```

---

## 규칙

- 원문 복붙 금지 — 반드시 내 언어로 재작성
- 하나의 영구 노트는 하나의 핵심 명제를 중심으로
- 인덱스 코드는 한번 부여 후 변경 없음
- 파일 저장 경로: `{OBSIDIAN_VAULT_PATH}/02-permanent/`
