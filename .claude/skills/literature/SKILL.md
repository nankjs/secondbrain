# /literature: 문헌 노트 생성 (가장 중요)

원문(논문, 기사, 영상 등)을 원자화하여 문헌 노트로 변환한다.
n8n 자동화 파이프라인의 핵심 스킬.

---

## 활성화 트리거

- `/literature` 명령 입력 시
- n8n 워크플로우에서 Claude API 호출 시 (자동)
- "이 링크 정리해줘", "이 논문 노트로 만들어줘" 요청 시

---

## 입력 형식

```
/literature [도메인]
URL: {원문 URL}
또는 직접 텍스트 붙여넣기
```

---

## 처리 과정

1. 원문 읽기 (URL 제공 시 내용 확인, 텍스트 제공 시 그대로 처리)
2. **원자화**: 하나의 핵심 아이디어 식별 (긴 글은 여러 노트로 분리 가능)
3. 핵심 내용 3~5개 포인트 추출
4. 도메인 자동 분류 (명시 시 우선)
5. 태그 추출 (최대 8개)
6. Frontmatter 생성 (type: literature)
7. 파일명: `{YYYY-MM-DD}-{domain}-{slug}.md`
8. `01-literature/` 폴더에 저장

---

## 출력 형식

```markdown
---
type: literature
created: {ISO8601}
modified: {ISO8601}
domain: {christian|academic|economy|general}
tags: [{태그 목록}]
status: inbox

source_url: {원문 URL}
source_title: "{원문 제목}"
source_author: "{저자}"
source_date: {YYYY-MM-DD}
source_type: article | paper | video | podcast | book

related: []
---

# {핵심 아이디어 제목}

## 핵심 내용

- {포인트 1}
- {포인트 2}
- {포인트 3}

## 원문 발췌

> "{중요한 인용구}"

## 내 생각

{선택: 짧은 메모 또는 비워둠}

---
*출처: [{source_title}]({source_url})*
```

---

## 원자화 원칙

- **하나의 노트 = 하나의 핵심 아이디어**
- 하나의 긴 기사에서 3개의 독립적인 아이디어가 있다면 → 3개의 노트 생성
- 아이디어 간 중복 없음
- 다른 노트에서 이해 가능한 독립적인 내용

---

## 규칙

- source_url은 반드시 포함 (URL 없을 시 "직접 입력" 명시)
- 요약은 원문의 언어로 (한국어 원문 → 한국어, 영어 원문 → 한국어 번역 요약)
- 파일 저장 경로: `{OBSIDIAN_VAULT_PATH}/01-literature/`

---

## n8n 연동 형식 (자동화)

n8n에서 Claude API 호출 시:
```json
{
  "skill": "literature",
  "domain": "academic",
  "source_url": "https://arxiv.org/abs/...",
  "source_title": "논문 제목",
  "source_content": "논문 전문 또는 요약"
}
```

응답:
```json
{
  "filename": "2026-04-10-academic-lightrag-graph-rag.md",
  "content": "---\n...\n---\n# ...",
  "domain": "academic",
  "tags": ["LightRAG", "GraphRAG", "VectorDB"]
}
```
