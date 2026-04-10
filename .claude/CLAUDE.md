# 세컨드브레인 프로젝트 Claude Code 설정

## 프로젝트 개요

**아바타 프로젝트 / 세컨드브레인** — 개인 지식 관리 시스템
- 자동 수집 → 지식 연결 → 즉시 분석
- Obsidian Vault: `C:/Users/kjswi/Documents/googleDrive/ObsiVault/`

## Obsidian Vault 경로

```
OBSIDIAN_VAULT_PATH=C:/Users/kjswi/Documents/googleDrive/ObsiVault
```

모든 스킬은 이 경로를 기준으로 파일을 저장한다.

## 프로젝트 스킬

이 프로젝트에서 사용 가능한 스킬 (`C:/KJS/AVARTA/secondBrain/.claude/skills/`):

| 스킬 | 설명 |
|------|------|
| `/fleeting` | 원문 → 떠돌이 노트 (00-fleeting/) |
| `/literature` | 원문 → 문헌 노트 (01-literature/) — n8n 자동화 연동 |
| `/permanent` | 문헌 노트 → 영구 노트 (02-permanent/) |
| `/lint` | Frontmatter 검증 및 정규화 |
| `/index` | 인덱스 페이지 자동 생성 (06-index/) |

## 구현 현황

| Phase | 상태 | 내용 |
|-------|------|------|
| P0 | ✅ 완료 | Git, Docker, 폴더 구조 |
| P1 | 🔄 진행 중 | Obsidian Vault + 스킬 정의 |
| P2 | ⏳ 대기 | n8n 수집 파이프라인 |
| P3 | ⏳ 대기 | LightRAG 지식 연결 |
| P4 | ⏳ 대기 | 즉시 분석 |
| P5 | ⏳ 선택 | Notion 공유 |
| P6 | ⏳ 선택 | Quartz 공개 |

## 태스크 파일

`C:/KJS/AVARTA/secondBrain/Docs/planning/06-tasks.md` 참조

## 주요 규칙

- `Docs/draft/` 폴더는 읽기 전용 (원본 연구 자료)
- `.env` 파일은 절대 커밋 금지 (`.env.example` 사용)
- 스킬 호출 시 Vault 경로는 항상 절대경로 사용
