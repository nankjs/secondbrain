# /fleeting: 떠돌이 노트 생성

원문 텍스트나 아이디어를 빠르게 캡처하여 떠돌이 노트로 변환한다.

---

## 활성화 트리거

- `/fleeting` 명령 입력 시
- 사용자가 "이거 노트로 저장해줘" 등 빠른 캡처 요청 시

---

## 입력 형식

```
/fleeting [도메인]
[원문 텍스트 또는 아이디어]
```

- **도메인**: christian | academic | economy | general (생략 시 general)
- **원문**: 자유 형식 텍스트

---

## 처리 과정

1. 입력 텍스트에서 핵심 아이디어 추출 (1~3문장)
2. 도메인 확인 (명시되지 않으면 내용 기반 자동 분류)
3. Frontmatter 생성 (type: fleeting)
4. 파일명 생성: `{YYYY-MM-DD}-fleeting-{slug}.md`
5. `00-fleeting/` 폴더에 저장

---

## 출력 형식

```markdown
---
type: fleeting
created: {ISO8601}
modified: {ISO8601}
domain: {christian|academic|economy|general}
tags: [{자동 추출된 태그}]
status: inbox
---

# {핵심 아이디어 제목}

{원문 텍스트 또는 요약}

---
*캡처: {YYYY-MM-DD HH:MM}*
```

---

## 규칙

- 분석이나 연결은 하지 않는다 — 빠른 캡처가 목적
- 원문을 최대한 보존한다
- 파일 저장 경로: `{OBSIDIAN_VAULT_PATH}/00-fleeting/`
- 저장 후 파일 경로를 사용자에게 알린다

---

## 예시

**입력**:
```
/fleeting academic
Attention Is All You Need 논문에서 Transformer 아키텍처는 RNN 없이 순수 어텐션만으로 시퀀스 모델링을 가능하게 했다.
```

**출력 파일**: `00-fleeting/2026-04-10-fleeting-transformer-attention.md`
```markdown
---
type: fleeting
created: 2026-04-10T14:30:00+09:00
modified: 2026-04-10T14:30:00+09:00
domain: academic
tags: [Transformer, Attention, NLP, 딥러닝]
status: inbox
---

# Transformer: 순수 어텐션으로 시퀀스 모델링

Attention Is All You Need 논문에서 Transformer 아키텍처는 RNN 없이 순수 어텐션만으로 시퀀스 모델링을 가능하게 했다.

---
*캡처: 2026-04-10 14:30*
```
