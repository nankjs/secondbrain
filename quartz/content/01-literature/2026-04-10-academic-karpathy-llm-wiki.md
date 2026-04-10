---
type: literature
created: 2026-04-10T15:40:00+09:00
modified: 2026-04-10T15:40:00+09:00
domain: academic
tags: [Karpathy, LLM, 지식관리, WikiMethod, 세컨드브레인]
status: processed

source_url: https://karpathy.github.io/2023/
source_title: "Andrej Karpathy's LLM-based Knowledge Wiki Method"
source_author: "Andrej Karpathy"
source_date: 2023-01-01
source_type: article

related: []
---

# Karpathy의 LLM 위키 방법론: raw/ 폴더 → LLM이 위키 자동 빌드

## 핵심 내용

- raw/ 폴더에 원문 그대로 저장 (가공 없음)
- LLM이 주기적으로 raw/ 를 읽고 위키 페이지 자동 생성
- 사람이 직접 정리하는 시간 0 → 수집만 하면 됨
- 위키 페이지는 raw/ 에 대한 링크 유지 (원본 추적 가능)
- 토큰 절약: 본문 대신 요약 + 원본 링크로 컨텍스트 유지

## 원문 발췌

> "The key insight: don't organize as you go. Dump everything raw, let the LLM do the synthesis later."

## 내 생각

우리 프로젝트의 00-fleeting/ = raw/, /literature 스킬 = LLM 위키 빌더. 개념 일치.

---
*출처: [Karpathy Blog](https://karpathy.github.io/2023/)*

## 관련 노트
- [[제텔카스텐 방법론의 신학적 적용]] (related, 0.70) — 지식관리 관점에서 유사성 존재
