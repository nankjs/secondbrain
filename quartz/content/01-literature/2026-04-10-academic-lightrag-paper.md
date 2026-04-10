---
type: literature
created: 2026-04-10T15:10:00+09:00
modified: 2026-04-10T15:10:00+09:00
domain: academic
tags: [LightRAG, GraphRAG, VectorDB, 지식그래프, RAG]
status: inbox

source_url: https://arxiv.org/abs/2410.05779
source_title: "LightRAG: Simple and Fast Retrieval-Augmented Generation"
source_author: "Guo et al."
source_date: 2024-10-08
source_type: paper

related: []
---

# LightRAG: 그래프+벡터 하이브리드 검색으로 RAG 품질 향상

## 핵심 내용

- 벡터 검색 단독보다 지식 그래프 구조 결합 시 답변 품질 향상
- 두 가지 검색 모드: 로컬(specific entity) + 글로벌(broad topic)
- 엔티티와 관계를 그래프로 저장 → 연결된 컨텍스트 함께 검색
- Chroma 등 기존 벡터 DB 대비 관계 추론 능력 우수
- EMNLP 2025 채택

## 원문 발췌

> "LightRAG incorporates graph structures into text indexing and retrieval processes, employing a dual-level retrieval system that enhances comprehensive information retrieval."

## 내 생각

세컨드브레인 Phase C의 핵심 컴포넌트. 노트 간 관계 추론에 특히 적합.

---
*출처: [LightRAG Paper](https://arxiv.org/abs/2410.05779)*

## 관련 노트
- [[Attention Is All You Need]] (related, 0.70) — RAG와 어텐션 모두 AI 발전 기여
