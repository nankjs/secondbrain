---
title: "2. LLM 자동 지식 연결 — 세컨드브레인 창발 아키텍처 연구"
source: "https://www.notion.so/33d2f5d38f22811d902efe7ec3ba7a73"
date: "2026-04-10"
type: draft
project: 아바타 프로젝트 / 세컨브레인 구축 기본안
---

# LLM 자동 지식 연결 — 세컨드브레인 창발 아키텍처 연구

> **핵심 질문**: 메모와 수집된 자료들을 LLM이 자동으로 연결할 때, 어떤 기술적 설계가 창발적 아이디어 생산을 극대화하는가?

---

## 1. 영상 요약

**시청**: [YouTube — 바이브랩스 | 제텔카스텐 + Karpathy + Claude Code 스킬 통합](https://youtu.be/5JpnmbE039E)
**원본 소스**: [안드레이 카르파티: 개인용 지식 기반 구축](https://www.notion.so/42d2f5d38f2282fd9b7981ec329296a2) (바이브랩스 노션)

### 핵심 내러티브

메모는 열심히 쌓지만 지식으로 전환되지 않는다는 문제의식에서 시작. **두 시대의 천재**를 합친다.

**왼쪽 — 니클라스 루만 (Niklas Luhmann)**
- 독일 사회학자, 평생 9만 장의 종이 카드 작성
- 논문 70편 + 책 50권
- 비결: **제텔카스텐** — 수집 → 분류 → 연결 → 축적

**오른쪽 — Andrej Karpathy**
- OpenAI 공동 창립자, Tesla AI 디렉터
- *"요즘 코딩보다 지식 정리에 토큰을 더 쓴다"*
- raw/ 폴더에 자료 투입 → LLM이 자동으로 위키 생성

**영상 통합 아이디어**: 두 방법론을 **Claude Code 커스텀 스킬 1장**으로 자동화

---

## 2. Karpathy 원문 (2026.04.03 X 게시글)

> *최근 제가 매우 유용하다고 느끼는 점: LLM을 활용해 연구 관심 분야의 다양한 주제에 대한 개인 지식 기반을 구축하는 것입니다. 최근 제 토큰 처리량의 상당 부분이 코드 조작보다는 지식 조작에 더 많이 쓰이고 있습니다.*

### Karpathy 6단계 워크플로우

| 단계 | 입력 | 처리 | 출력 |
|------|------|------|------|
| 수집 | 아티클·논문·레포·이미지 | Obsidian Web Clipper + 핫키 | `raw/` 디렉토리 |
| 컴파일 | `raw/` 원본 자료 | LLM이 점진적 위키 빌드 | `.md` 위키 (요약+백링크+개념 분류) |
| IDE | 위키+원시데이터+시각화 | Obsidian 프론트엔드 | 통합 뷰 (Marp 슬라이드, 차트) |
| Q&A | 복잡한 질문 | LLM 에이전트 + 자동 인덱스 | .md, 슬라이드, 이미지 → 위키 재파일링 |
| 린팅 | 전체 위키 | LLM 상태 점검 + 웹 검색 | 수정, 보완, 새 연관성 발굴 |
| 확장 | 축적된 지식 베이스 | 커스텀 검색 엔진 + 파인튜닝 | 가중치 내재화된 전문 지식 |

> **핵심**: LLM이 위키의 모든 데이터를 직접 쓰고 유지합니다. 사람은 거의 건드리지 않습니다.

---

## 3. 기존 Karpathy 방식의 문제점

Karpathy 위키 = 문서 100개, 40만 단어. LLM이 **매번 전체를 읽어야** 하는 구조:

| 작업 | 필요 토큰 |
|------|---------|
| 컴파일 (위키 생성) | 전체 읽기 |
| 연결 문서 탐색 | 전체 읽기 |
| 린팅 (오류 감지) | 전체 읽기 |
| Q&A | 전체 읽기 |

> Karpathy는 OpenAI 공동 창립자라 토큰이 사실상 무제한. **Claude Code 프로 ($20/월)는 하루에 여러 번 한도**에 걸림.

### 파일 감지 메커니즘 (LLM 혼자서는 불가능)

LLM 자체는 파일 시스템을 모니터링하지 못한다. 두 가지 방식으로 추정:
- **인덱스 파일 diff** — `index.md`의 처리 완료 목록 vs `raw/`의 실제 파일 목록 비교 → 미처리 파일 추출
- **셸 명령 전처리** — `find raw/ -newer wiki/.last_compiled` 또는 `git diff --name-only`로 변경 파일 필터링 후 LLM에 전달

> Karpathy가 *"스크립트를 엮어 만든 임시방편적인 솔루션"*이라 표현한 것이 바로 이 파이프라인이다.

→ 바이브랩스의 해법: **토큰을 10분의 1로 줄이는 3전략**

---

## 4. 토큰 절약 3전략 (핵심 시스템 설계)

### 전략 1: Inbox Zero — 처리된 raw 파일 숨기기

```
처리 전: raw/분리별이.md
처리 후: raw/archive/분리별이.md  (삭제 아님, 숨기기)
→ raw/ 폴더는 항상 비어 있음 = 충에 있는 것은 100% 새것
```

LLM이 "이거 새것인가 이미 처리한 것인가" 판단 불필요

### 전략 2: 프론트 메터만 읽기 — 40만 단어 → 수백 줄

각 메모마다 YAML frontmatter 추가:

```yaml
---
title: "AI와 창의성"
tags: [AI, 인지과학]
id: "B-2"
summary: "AI는 직관적 연상을 모사하지 못하지만 대역시냅시로 대안적 사고를 보완한다"
links: [A-3, C-1]
---
```

LLM이 메모 200개를 분석할 때 **본문 읽기 없이** 프론트 메터만으로 연관성 판단 가능

### 전략 3: 원본 보존 + 링크로 돌아가기

임시 메모 → 연구 연결 시 원본 링크 살려 둠 → 나중에 원래 맥락 확인 가능

---

## 5. 제텔카스텐 3유형 ↔ Karpathy ↔ Notion 대응표

| 제텔카스텐 | Karpathy | 세컨드브레인 (Notion) |
|----------|---------|-------------------|
| 임시메모 (Fleeting) | `raw/` 디렉토리 | In Notes DB |
| 문헌메모 (Literature) | raw/ 내 요약+해석 | In Notes DB 분석 영역 |
| 영구메모 (Permanent) | 컴파일된 위키 .md | Thinker Notes DB |

**핵심 차이**: 루만은 임시메모를 처리 후 **폐기**했고, Karpathy는 `raw/`를 **영구 보존**한다.
→ 디지털 시대의 해법: **Archive 플래그** — 삭제하지 않되, 활성 탐색 공간에서 제외

**통합 핵심 공식**:
> 임시메모 → 처리 완료 → Archive 플래그 → raw/는 늘 비어있음 → 영구메모에 아이디어 집약 + 임시메모 레퍼런스 보유 → 프론트매터(DB 프로퍼티)에 요약 캐싱 → LLM 토큰 절약

---

## 6. Claude Code 스킬 아키텍처 (영상 실제 시스템)

**스킬 위치**: `.claude/sys/스킬명.md` — 코딩 없이 일반 언어로 정의하는 AI 비서 업무 매뉴얼

### 주요 스킬 목록

| 스킬 | 역할 | 인간/AI |
|------|------|--------|
| `/fleeting` | 임시 아이디어 기록, 원자성 유지 | 인간 입력 |
| `/literature` | 출처 있는 문헌 노트 생성 | 인간 입력 |
| `/permanent` | 문헌+임시 노트를 연결해 새로운 연구 노트 생성 | **인간이 자기 말로** 쓰는 영역 |
| `/batch` | 여러 메모 병렬 처리 | AI 자동화 |
| `/lint` | 고아 노트 탐지 + 끊긴 링크 수정 | AI 자동화 |
| `/index` | 클러스터별 인덱스 + 관계도 생성 | AI 자동화 |
| `/query` | 볼트 전체 Q&A 결과 MD 파일링 | AI 자동화 |
| `/loop` | 파일 감시 + 자동 컴파일 루프 | AI 자동화 |

### 콤보 스킬 흐름 (데모 기준)

```
사용자: raw/ 폴더에 메모 투입
    ↓
/fleeting 또는 /literature 스킬 실행
    ↓ [3단계 딥 리딩]
    - 표면 읽기
    - 논지 구조 파악
    - 기존 지식 체계에서 위치 판단
    ↓
고유 인덱스 코드 부여 (B-2, C-1A ...)
    + 기존 노트와 의미 연결 자동 탐색
    ↓
/permanent: 두 노트를 연결한 새 연구 노트 생성
```

### 루만에서 차용한 세 가지

1. **원자성**: 메모 1개 = 아이디어 1개, 주제 혼잡 금지
2. **인덱스 코드**: 각 메모에 고유 주소 (`4A`, `C-1B`...) → 정확한 위치에 삽입 가능
3. **백링크**: 메모끼리 서로 참조

---

## 7. 현실적 시스템 구조

```
수집 자동화 그룹     인간의 사고 그룹     LLM 자동화 그룹
──────────────    ────────────    ──────────────────
fleeting        permanent       lint
literature      (루만의 철학:    index
                자기 말로 쓰기)  query
                               loop
```

> **루만의 철학 보존**: *"이해한 것은 자기 말로 쓰지 않으면 이해한 게 아니다"*
> → permanent 스킬은 인간이 직접 쓰는 영역을 반드시 지킴

---

## 8. "RAG 없이 충분하다"의 조건 붕괴 분석

Karpathy가 "RAG 없이 충분하다"고 말한 전제 조건은 사실 **취약하다**.

**작동하는 이유 단 두 가지**:
1. **규모가 작다** — ~100개 문서, ~40만 단어. 책 2~3권 분량. 컨텍스트 윈도우(100K~200K 토큰)로 커버 가능
2. **LLM이 전체를 "읽을 수 있다"** — 인덱스+요약을 통한 사실상 브루트포스 독해

**조건이 깨지는 순간 시스템이 무너진다**:

**① 스케일 문제**: 메모 1,000개, 10,000개가 되면 인덱스 파일 자체가 수십만 단어 → LLM이 인덱스 읽는 것만으로 컨텍스트 소진 → "인덱스의 인덱스"가 필요 → **벡터 DB의 계층적 인덱싱을 수동으로 재발명하는 꼴**

**② 검색 정밀도**: LLM 추론으로 관련 문서 찾기는 작은 규모에서 "충분히 좋다"일 뿐 "정확하다"가 아님. 시맨틱 유사도 검색은 벡터 임베딩이 수학적으로 수행하는 것 → **망치로 나사를 박는 격**

**③ 제텔카스텐 연결 속도 저하**: LLM이 문서 간 연결 수행 시 매번 관련 문서를 읽어야 함. 문서 100개는 괜찮지만 1,000개가 되면 연결 후보 탐색만으로 토큰 비용 기하급수적 증가. 그래프 DB + 임베딩 기반이라면 연결 후보 탐색은 밀리초 단위

> **결론**: Karpathy의 진짜 공헌은 "RAG가 필요 없다"가 아니다. **"지식 베이스의 설계 주체가 사람에서 LLM으로 넘어갔다"**는 것이 핵심이고, 검색 인프라는 별개의 문제다.

---

## 9. Notion 자체가 이미 벡터 RAG로 작동한다

Notion 공식 엔지니어링 블로그: *"Two years of vector search at Notion: 10x scale, 1/10th cost"*

Notion AI가 워크스페이스를 검색할 때 단순 키워드 매칭이 아닌 **시맨틱 벡터 검색** 작동.

**Karpathy 방식 vs Notion 방식**:

| | Karpathy | Notion |
|-|---------|--------|
| 검색 방식 | LLM이 인덱스 직접 읽고 추론 (브루트포스) | 임베딩 → 벡터 검색 → LLM 컨텍스트 주입 (RAG) |
| 스케일 한계 | ~40만 단어 | 수억 블록 |
| 투명성 | .md 파일 100% 검사 가능 | 블랙박스 |
| 비용 | 토큰 소진 | 구독료 포함 |

> Notion 기반 세컨드브레인은 이미 벡터 검색 인프라 위에서 돌아가고 있다는 뜻.

---

## 10. 기술적 완성도를 높이는 심화 방향

### 10-1. A-MEM — Zettelkasten 기반 LLM 에이전트 메모리

> arXiv:2502.12110 (2025)

```
새 메모 입력
   ↓
LLM이 기존 메모 중 연관 메모 자동 탐색
   ↓
링크 생성 시 "왜 연결되는가" 주석 자동 생성
   ↓
동적 인덱싱 → 시간이 지날수록 연결망 밀도 증가
```

**창발 메커니즘**: 링크 생성 시 의미 주석을 함께 저장 → 나중에 이 주석이 새 아이디어의 씨앗이 됨

참고: [arXiv:2502.12110](https://arxiv.org/abs/2502.12110)

### 10-2. LightRAG — 소규모에서 대규모로 확장하는 그래프 RAG

> EMNLP 2025, GitHub 30,000+ 스타

| | Claude Code 스킬 (영상 방식) | LightRAG 추가 |
|-|--------------------------|-------------|
| 규모 | ~수십백 노트 | 수만 노트로 확장 |
| 연결 방식 | 프론트 메터 키워드 매칭 | 그래프 관계 순회 |
| 실시간 업데이트 | 파일 감시 | 증분 그래프 업데이트 |
| 주요 장점 | 토큰 절약 | 창발적 다중 홉 추론 |

참고: [LightRAG GitHub](https://github.com/HKUDS/LightRAG)

### 10-3. Zettelkasten MCP — Claude 직접 통합

> entanglr/zettelkasten-mcp — Claude와 직접 연동되는 MCP 서버

| | 스킬 (.md 파일) | Zettelkasten MCP |
|-|--------------|----------------|
| 링크 타입 | 제한적 | supports/contradicts/extends/inspired-by |
| 저장소 | 마크다운 파일 | SQLite + ChromaDB 하이브리드 |
| 시맨틱 검색 | 키워드 기반 | 벡터 유사도 |

참고: [zettelkasten-mcp GitHub](https://github.com/entanglr/zettelkasten-mcp)

### 10-4. Obsidian + Claude Code 직접 통합 도구

- [Obsidian-CLI-skill](https://github.com/pablo-mano/Obsidian-CLI-skill) — Obsidian용 Claude Code 스킬
- [claudian](https://github.com/YishenTu/claudian) — Obsidian 플러그인으로 Claude Code 내장
- [claude-code-obsidian](https://github.com/az9713/claude-code-obsidian) — 스킬 + 볼트 설정

---

## 11. 창발적 아이디어 생산 메커니즘

노트 수가 많아질수록 강력해지는 공식:

```
노트 N개 → 가능한 연결 수 N²/2 (2중 조합)
노트 50개  → 가능한 연결 1,225개
노트 200개 → 가능한 연결 19,900개
```

### 창발의 4가지 조건

1. **도메인 경계 타파**: 물리학 노트와 신학 노트와 경제 노트가 하나의 그래프에 존재. LLM이 "가장 뜻밖의 연결" 주기적 보고
2. **주석이 있는 링크**: 단순 `[[A]] → [[B]]` 아닌 "왜 연결되는가"가 핵심이다. 이 주석이 이후 새 아이디어 합성의 씨앗
3. **질문 노트 보존**: 답하지 못한 질문도 노트로 저장. LLM이 새 자료 수집 시 기존 질문과 자동 대조 → "이 논문이 저 질문에 답하는가?"
4. **주기적 재연결**: Spaced Repetition 원리 적용. 오래된 노트를 LLM이 새 자료와 재연결 시도 → 시간적 거리가 창발의 또 다른 축

---

## 12. 통합 아키텍처 다이어그램

```
[ 수집 ] raw/ 폴더 또는 Obsidian Web Clipper
       ↓
[ 원자화 ] /fleeting 또는 /literature 스킬
         • 3단계 딥리딩 (표면·논지·위치)
         • frontmatter 생성 (인덱스 코드 + 태그 + 한줄 요약)
       ↓
[ 연결 ] /permanent 스킬
         • frontmatter만 읽어 연관 노트 탐색
         • "왜 연결되는가" 주석 자동 생성
         • 인간이 자기 말로 정제하면 완성
       ↓
[ 유지보수 ] /lint + /index + /loop
         • 고아 노트 탐지 → 자동 수정
         • 클러스터 인덱스 갱신
         • 파일 감시 루프 (진정한 지식 공장화)
       ↓
[ 시각화 ] Obsidian 그래프 뷰 / 클러스터 맵
```

---

## 13. 심화 참고 자료

| 분류 | 자료 | 핵심 기여 |
|------|------|---------|
| 영상 소스 | [YouTube 링크](https://youtu.be/5JpnmbE039E) | 바이브랩스, 실제 데모 포함 |
| 원본 노션 | [안드레이 카르파티: 개인용 지식 기반 구축](https://www.notion.so/42d2f5d38f2282fd9b7981ec329296a2) | 바이브랩스 직접 작성 분석 + 커스텀 프롬프트 |
| Karpathy 원문 | [llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | 영감의 원천 |
| Karpathy X | [원문 트윗](https://x.com/karpathy/status/2039805659525644595) | 2026.04.03 게시 |
| VentureBeat | [RAG 우회 아키텍처](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an) | "RAG를 우회하는 LLM 지식 베이스 아키텍처" |
| 에이전트 메모리 | [A-MEM arXiv:2502.12110](https://arxiv.org/abs/2502.12110) | Zettelkasten+LLM 메모리 |
| 그래프 RAG | [LightRAG GitHub](https://github.com/HKUDS/LightRAG) | EMNLP 2025, 대규모 확장용 |
| MCP 통합 | [zettelkasten-mcp](https://github.com/entanglr/zettelkasten-mcp) | Claude 직접 연동 |
| Notion 벡터 검색 | [Two years of vector search at Notion](https://www.notion.com/ko/blog/two-years-of-vector-search-at-notion) | Notion RAG 아키텍처 공식 블로그 |

---

## 14. 구현 로드맵

- [ ] **Phase 1** — Obsidian 볼트에 `.claude/sys/` 폴더 생성 + fleeting/literature/permanent 스킬 3개 작성
- [ ] **Phase 2** — frontmatter 템플릿 확정 (인덱스 코드 체계 설계)
- [ ] **Phase 3** — /lint + /index 스킬 추가 → 일주일 1회 자동 실행
- [ ] **Phase 4** — 노트 100개 돌파 후 LightRAG Docker 도입 검토
- [ ] **Phase 5** — A-MEM 방식으로 링크 주석 자동 생성 기능 보강
- [ ] **Phase 6** — /query 스킬로 주간 스펙션 + Notion 자동 게시

---

*작성: 2026-04-10 | 영상: https://youtu.be/5JpnmbE039E (바이브랩스) | 원본 소스: https://www.notion.so/42d2f5d38f2282fd9b7981ec329296a2*
