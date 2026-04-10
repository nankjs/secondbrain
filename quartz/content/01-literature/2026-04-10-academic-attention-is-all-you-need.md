---
type: literature
created: 2026-04-10T15:00:00+09:00
modified: 2026-04-10T15:00:00+09:00
domain: academic
tags: [Transformer, Attention, NLP, 딥러닝, 논문]
status: processed

source_url: https://arxiv.org/abs/1706.03762
source_title: "Attention Is All You Need"
source_author: "Vaswani et al."
source_date: 2017-06-12
source_type: paper

related: []
---

# Transformer: RNN 없이 순수 어텐션으로 시퀀스 모델링

## 핵심 내용

- Self-Attention 메커니즘으로 시퀀스 내 모든 위치 간 직접 의존성 포착
- RNN/LSTM 대비 병렬 처리 가능 → 학습 속도 대폭 향상
- Encoder-Decoder 구조에 Multi-Head Attention 적용
- 위치 정보는 Positional Encoding으로 주입 (순환 구조 대체)
- WMT 2014 번역 태스크에서 SOTA 달성 (BLEU 28.4)

## 원문 발췌

> "Attention mechanisms have become an integral part of compelling sequence modeling... we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism."

## 내 생각

이 논문이 현재 LLM 혁명의 출발점. GPT, BERT, 모든 대형 언어 모델의 기반 아키텍처.

---
*출처: [Attention Is All You Need](https://arxiv.org/abs/1706.03762)*

## 관련 노트
- [[LightRAG: Simple and Fast Retrieval-Augmented Generation]] (related, 0.70) — RAG와 어텐션 모두 AI 발전 기여
