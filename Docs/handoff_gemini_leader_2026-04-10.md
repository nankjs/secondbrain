---
title: Gemini 리더 업무인계서
date: 2026-04-10
from: Claude (클랩스 리더)
to: Gemini (후임 리더)
project: 세컨드브레인 구축 (아바타 프로젝트)
---

# Gemini 리더 업무인계서

> 너는 이제 이 프로젝트의 리더야. Claude가 토큰 부족으로 자리를 넘긴다.
> 이 문서를 완전히 숙지한 후 대기 상태로 전환해. 사용자의 다음 지시를 기다려.

---

## 1. 반드시 읽어야 할 파일 목록

아래 순서대로 읽어라. 읽기 전에 작업 시작 금지.

| 순서 | 파일 경로 | 목적 |
|------|---------|------|
| 1 | `C:/KJS/AVARTA/secondBrain/Docs/draft/04_오픈소스_스택과_아키텍처_재검토_v2.md` | 현재 채택된 최신 아키텍처 (가장 중요) |
| 2 | `C:/KJS/AVARTA/secondBrain/Docs/draft/02_LLM_자동_지식_연결_세컨드브레인_창발_아키텍처_연구.md` | 설계 근거 (Karpathy + 제텔카스텐 분석) |
| 3 | `C:/KJS/AVARTA/secondBrain/Docs/TASKS.md` | 전체 작업 계획 및 진행 순서 |
| 4 | `C:/KJS/AVARTA/secondBrain/Docs/draft/session_transcript_2026-04-10.md` | 이전 세션 전체 대화 기록 (리더 훈련 과정 포함) |

**현재 Claude 세션 트랜스크립트 경로**:
```
C:/Users/kjswi/.claude/projects/C--KJS-AVARTA-secondBrain/74914451-3c98-4a9f-b329-fdeb4ce6b92b.jsonl
```
이 JSONL 파일은 현재 세션(Claude가 파일들을 검토하고 TASKS.md를 작성한 과정)을 담고 있다. 필요시 참조해라.

---

## 2. 프로젝트 핵심 요약

**무엇을 만드는가**: 개인 지식 관리 시스템 (세컨드브레인)
- 6개 도메인에서 자료를 자동 수집
- LLM이 수집 자료를 원자적 노트로 변환
- 노트들을 자동으로 연결하여 창발적 아이디어 생산

**현재 상태**: 초안(draft) 4개 문서가 작성된 상태. 개발문서 작성 단계 진입 전.

**다음 해야 할 일**: TASKS.md의 T00부터 순서대로 개발문서 작성
- T00: `/socrates` 스킬 정의 → 가장 먼저
- T01: PRD → T02: TRD → T03: 아키텍처 → ...

---

## 3. 리더로서 행동 원칙

### 네가 해야 할 것
- 사용자의 지시를 받아 개발문서 작성을 **주도**한다
- 각 문서 작성 전 `/socrates` 방식으로 요구사항을 질문하고 정제한다
- draft 초안 문서들을 출발점으로 삼되, 맹목적으로 따르지 않는다
- 완성된 문서는 `C:/KJS/AVARTA/secondBrain/Docs/planning/` 폴더에 저장한다
- 각 Phase 완료 후 사용자에게 보고하고 다음 지시를 기다린다

### 네가 하지 말아야 할 것
- TASKS.md에 없는 작업을 임의로 시작하지 마라
- 사용자 승인 없이 Phase를 건너뛰지 마라
- `Docs/draft/` 폴더의 파일을 수정하지 마라 (읽기 전용)
- `C:/Users/kjswi/.claude/` 경로를 탐색하거나 수정하지 마라

---

## 4. /socrates 스킬 개념

이 스킬은 아직 파일로 존재하지 않는다. **T00 작업이 이 스킬을 만드는 것**이다.

개념:
- 사용자가 `/socrates [문서명]`을 호출하면 시작
- LLM이 해당 문서에 필요한 핵심 질문 5~7개를 순서대로 제시
- 사용자 답변 → LLM 요약·정제 → 문서 섹션 구성
- 모든 질문 완료 → 문서 초안 생성
- 소크라테스식: 답변이 불명확하면 재질문

스킬 파일 저장 위치: `C:/KJS/AVARTA/secondBrain/.claude/skills/socrates.md`

---

## 5. 디렉토리 구조 (목표 상태)

```
C:/KJS/AVARTA/secondBrain/
├── Docs/
│   ├── draft/          ← 읽기 전용 초안 (건드리지 마)
│   ├── planning/       ← 완성된 개발문서들 (여기에 저장)
│   └── TASKS.md        ← 작업 계획 (완료 시 상태 업데이트)
├── .claude/
│   └── skills/         ← Claude Code 스킬 파일들 (T05~T11)
└── .gemini/            ← Gemini 설정
```

---

## 6. 보고 형식

작업 시작 전 다음 형식으로 확인 보고해라:

```
[Gemini → 사용자]
인계서 숙지 완료.

이해한 내용:
- 프로젝트: 세컨드브레인 구축 (아바타 프로젝트)
- 현재 상태: draft 4개 완료, 개발문서 작성 시작 전
- 다음 작업: T00 - /socrates 스킬 정의

질문: [있다면 기재, 없으면 "없음"]

사용자의 다음 지시를 기다립니다.
```

---

*인계: Claude → Gemini | 2026-04-10*
