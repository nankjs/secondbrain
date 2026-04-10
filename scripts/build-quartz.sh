#!/usr/bin/env bash
# Vault 노트 → Quartz 빌드 스크립트
# 사용법:
#   bash scripts/build-quartz.sh          # 빌드만
#   bash scripts/build-quartz.sh --serve  # 빌드 후 로컬 서버 (포트 3333)

set -e

VAULT="${OBSIDIAN_VAULT_PATH:-C:/Users/kjswi/Documents/googleDrive/ObsiVault}"
QUARTZ_ROOT="$(dirname "$0")/../quartz"
CONTENT="$QUARTZ_ROOT/content"
QUARTZ_CLI="$QUARTZ_ROOT/quartz/bootstrap-cli.mjs"

echo "[1/3] Vault 노트 복사..."
for folder in "01-literature" "02-permanent"; do
  mkdir -p "$CONTENT/$folder"
  cp "$VAULT/$folder"/*.md "$CONTENT/$folder/" 2>/dev/null && echo "  $folder 복사 완료" || true
done

echo "[2/3] Quartz 빌드..."
if [ "$1" = "--serve" ]; then
  node "$QUARTZ_CLI" build --serve --port 3333
else
  node "$QUARTZ_CLI" build
  echo "[3/3] 완료: $QUARTZ_ROOT/public/"
fi
