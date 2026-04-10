# /analyze: 즉시 분석 온디맨드

사용자 질문을 받아 Vault 지식베이스에서 관련 내용을 검색하고,
구조화된 마크다운 보고서를 5분 이내에 생성한다.

---

## 활성화 트리거

- `/analyze` 명령 입력 시

---

## 입력 형식

```
/analyze
질문: [분석할 주제나 질문]
도메인: [academic|christian|economy|all] (선택, 기본 all)
깊이: [quick|standard|deep] (선택, 기본 standard)
```

### 예시

```
/analyze
질문: RAG와 전통적인 검색의 차이점은?

/analyze
질문: 인덱스 펀드 투자 전략
도메인: economy

/analyze
질문: 제텔카스텐과 AI 지식 관리의 결합 가능성
깊이: deep
```

---

## 처리 과정

### 1단계: 쿼리 분해
- 질문에서 핵심 키워드 추출 (3~5개)
- 도메인 필터 결정
- 검색 전략 선택 (hybrid/global/naive)

### 2단계: LightRAG 검색
```
scripts/vector-search.py "{질문}" --mode hybrid
```
- Top-K = 30 (standard), 50 (deep)
- 임계값: 0.7 이상 결과만 사용

### 3단계: 보고서 생성
검색된 컨텍스트를 바탕으로 Claude가 다음 템플릿으로 보고서 작성:

```markdown
# [질문 제목]

**분석일**: YYYY-MM-DD
**도메인**: academic|christian|economy|all
**출처 노트**: N개

---

## 핵심 답변

[2~3문장 핵심 요약]

## 상세 분석

### [소주제 1]
[상세 내용]

### [소주제 2]
[상세 내용]

## 연결된 아이디어

- [[노트1]]: [연결 이유]
- [[노트2]]: [연결 이유]

## 추가 탐색 권장

- [질문1]: 더 탐구할 방향
- [질문2]: 관련 주제

---
*이 보고서는 Vault의 N개 노트에서 생성되었습니다.*
```

### 4단계: 저장 (선택)
- `ObsiVault/03-resources/analysis/YYYY-MM-DD-{slug}.md`에 저장 가능
- 사용자 확인 후 저장

---

## 깊이별 설정

| 깊이 | Top-K | 검색 모드 | 소요 시간 |
|------|-------|----------|---------|
| quick | 10 | naive | ~1분 |
| standard | 30 | hybrid | ~2분 |
| deep | 50 | global | ~5분 |

---

## 규칙

- LightRAG 미실행 시: `docker compose up -d lightrag` 안내
- 검색 결과 0건 시: Vault에 관련 노트 없음 안내 + 노트 추가 권장
- 출처 노트를 항상 명시 ([[노트명]] 형식)
- 추측이나 외부 지식 최소화, Vault 내용 우선
- 보고서 저장 전 사용자 확인
