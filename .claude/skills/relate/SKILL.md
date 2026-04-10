# /relate: 노트 관계 분석

두 노트 간의 의미적 관계를 분석하여 타입, 강도, 설명을 반환한다.
Phase C 지식 연결의 핵심 스킬.

---

## 관계 타입 정의

| 타입 | 설명 | 예시 |
|------|------|------|
| `context` | A는 B의 배경/맥락 | "인터넷 역사"는 "TCP/IP 프로토콜"의 배경 |
| `extend` | A가 B의 개념을 확장/심화 | "Transformer v2"는 "Attention Is All You Need"를 확장 |
| `contradict` | A와 B가 상충하거나 반론 관계 | "인덱스 투자 지지"는 "액티브 투자 지지"와 모순 |
| `related` | 주제적으로 관련 있음 | "Pandas 성능"과 "데이터 처리 라이브러리" 비교 |
| `supports` | A가 B의 주장을 뒷받침 | "버핏 인터뷰"는 "장기 투자 원칙"을 지지 |
| `inspired` | A가 B에서 영감을 받음 | "LightRAG"는 "GraphRAG"에서 영감 |

---

## 활성화 트리거

- `/relate` 명령 입력 시
- `scripts/auto-linking.py` 자동화에서 호출 시

---

## 입력 형식

```
/relate
노트A: [[노트A-제목]]
노트B: [[노트B-제목]]
```

또는 자동화에서 JSON:
```json
{
  "note_a": {"title": "...", "content": "..."},
  "note_b": {"title": "...", "content": "..."}
}
```

---

## 처리 과정

1. 두 노트의 제목 + 핵심 내용(최대 500자) 읽기
2. 관계 분석:
   - 주제 중첩도 파악
   - 논리적 관계 (지지/반론/확장/배경)
   - 시간적/인과 관계
3. 가장 적합한 관계 타입 1개 선택
4. 강도 산정 (0.0~1.0):
   - 0.9+: 직접적으로 같은 주제
   - 0.7~0.9: 강한 주제 연관
   - 0.5~0.7: 간접 연관
   - 0.5 미만: 관계 없음 (연결 안 함)

---

## 출력 형식

```json
{
  "relation_type": "context|extend|contradict|related|supports|inspired",
  "strength": 0.85,
  "description": "한 줄 관계 설명 (한국어, 최대 50자)",
  "bidirectional": true
}
```

### 임계값 규칙
- `strength >= 0.7` → Obsidian 링크 생성
- `strength < 0.5` → 무시 (연결 안 함)
- `0.5 <= strength < 0.7` → 약한 연결 (태그만 추가)

---

## 예시

**입력**:
```
노트A: "Transformer: RNN 없이 순수 어텐션으로 시퀀스 모델링"
노트B: "LightRAG: 그래프+벡터 하이브리드 검색"
```

**출력**:
```json
{
  "relation_type": "inspired",
  "strength": 0.75,
  "description": "LightRAG의 그래프 어텐션은 Transformer 아키텍처에서 영감",
  "bidirectional": false
}
```

---

## 규칙

- 양방향 관계는 `bidirectional: true` (A→B, B→A 모두 링크)
- 단방향 관계는 `bidirectional: false` (A→B만 링크)
- `contradict`는 항상 양방향
- `context`는 단방향 (B→A는 다른 타입으로 재분류)
