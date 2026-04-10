# n8n 운영 매뉴얼 (P2-T13)

## 접속 정보

| 항목 | 값 |
|------|-----|
| URL | http://localhost:15678 |
| 이메일 | admin@secondbrain.local |
| 비밀번호 | secondbrain2026!A |
| 워크플로우 ID | tpP9M1RQgIQLAlwl |

---

## 워크플로우 활성화

1. http://localhost:15678 접속 → 로그인
2. 왼쪽 메뉴 **Workflows** 클릭
3. `secondbrain-weekly-collection` 선택
4. 우측 상단 토글 **Inactive → Active** 전환
5. 다음 실행: 월요일 09:00 KST 자동 실행

---

## 수동 실행 방법

```bash
# n8n UI에서 수동 실행
# Workflow 열기 → 우측 상단 "Execute Workflow" 버튼

# 또는 REST API로 수동 트리거 (curl)
curl -s -X POST "http://localhost:15678/api/v1/workflows/tpP9M1RQgIQLAlwl/run" \
  -H "X-N8N-API-KEY: {API_KEY}" \
  -H "Content-Type: application/json"
```

---

## ArXiv 수동 실행

```bash
# 바로 ArXiv 수집 테스트
python C:/KJS/AVARTA/secondBrain/scripts/collect-arxiv.py --max 3 --days 7

# 결과를 Vault에 직접 저장
python C:/KJS/AVARTA/secondBrain/scripts/collect-arxiv.py --max 3 | \
  python C:/KJS/AVARTA/secondBrain/scripts/save-to-vault.py
```

---

## 오류 발생 시 대처

### 1. 컨테이너가 죽었을 때

```bash
cd C:/KJS/AVARTA/secondBrain
docker compose ps                        # 상태 확인
docker compose up -d                     # 재시작
docker compose logs --tail=50 n8n        # 로그 확인
```

### 2. MiniFlux RSS 수집 실패

```bash
# MiniFlux 피드 갱신 강제 실행
curl -s -X PUT -u admin:secondbrain2026 \
  http://localhost:8080/v1/feeds/1/refresh

# 모든 피드 갱신
curl -s -X PUT -u admin:secondbrain2026 \
  http://localhost:8080/v1/feeds/refresh
```

### 3. API 비용 모니터링

```bash
# Claude API 사용량 확인 (월별)
# https://console.anthropic.com/usage 에서 확인
# 주 1회 수집 시 예상 비용: ~$1~3/월 (haiku 모델 기준)
```

### 4. Obsidian Vault 저장 실패

```bash
# Vault 경로 확인
echo %OBSIDIAN_VAULT_PATH%

# 수동으로 인덱스 재생성
python C:/KJS/AVARTA/secondBrain/scripts/generate-index.py
```

---

## 컨테이너 자동 시작 설정

`restart: unless-stopped` 설정 완료 — Docker Desktop 시작 시 자동 실행.

Docker Desktop 자동 시작 설정:
- Docker Desktop → Settings → General → "Start Docker Desktop when you log in" 체크

---

## 로그 위치

| 로그 | 위치 |
|------|------|
| n8n 실행 로그 | `docker compose logs n8n` |
| MiniFlux 로그 | `docker compose logs miniflux` |
| 수집 로그 | `C:/KJS/AVARTA/secondBrain/logs/` (현재 .gitignore) |

---

## 주간 점검 체크리스트

매주 화요일 (수집 다음 날) 확인:

- [ ] n8n 실행 이력: http://localhost:15678 → Executions
- [ ] 새 노트 수: `ObsiVault/01-literature/` 파일 수 증가 확인
- [ ] 오류 여부: `docker compose logs --since=168h n8n | grep -i error`
- [ ] API 비용: Anthropic Console 확인
