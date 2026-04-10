"""
Obsidian Vault 노트 → LightRAG 임베딩 (P3-T2)
기존 노트를 LightRAG에 일괄 인덱싱

사용법:
  python scripts/embed-vault.py                 # 전체 임베딩
  python scripts/embed-vault.py --folder 01-literature  # 특정 폴더만
  python scripts/embed-vault.py --dry-run       # 실제 전송 없이 목록만 확인
"""

import argparse
import json
import os
import time
import urllib.request
import urllib.error
from pathlib import Path

LIGHTRAG_API = "http://localhost:9621"
VAULT_PATH = os.environ.get(
    "OBSIDIAN_VAULT_PATH",
    "C:/Users/kjswi/Documents/googleDrive/ObsiVault"
)

# 임베딩할 폴더 목록
EMBED_FOLDERS = ["00-fleeting", "01-literature", "02-permanent"]


def check_lightrag() -> bool:
    """LightRAG 서버 상태 확인"""
    try:
        with urllib.request.urlopen(f"{LIGHTRAG_API}/health", timeout=5) as r:
            data = json.loads(r.read())
            return data.get("status") == "healthy"
    except Exception as e:
        print(f"[FAIL] LightRAG 연결 실패: {e}")
        return False


def get_indexed_docs() -> set:
    """이미 인덱싱된 문서 목록 조회"""
    try:
        req = urllib.request.Request(f"{LIGHTRAG_API}/documents")
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            # LightRAG API 응답 형식에 따라 파싱
            if isinstance(data, list):
                return {d.get("id", d.get("file_name", "")) for d in data}
            elif isinstance(data, dict):
                docs = data.get("data", data.get("documents", []))
                return {d.get("id", d.get("file_name", "")) for d in docs}
    except Exception:
        pass
    return set()


def read_note(file_path: Path) -> str:
    """마크다운 노트 읽기"""
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  [WARN] 읽기 실패 {file_path.name}: {e}")
        return ""


def embed_document(content: str, filename: str) -> bool:
    """LightRAG에 문서 인덱싱"""
    payload = json.dumps({
        "text": content,
        "description": filename,
        "metadata": {"source": filename}
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{LIGHTRAG_API}/documents/text",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            resp = json.loads(r.read())
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  [FAIL] HTTP {e.code}: {body[:200]}")
        return False
    except Exception as e:
        print(f"  [FAIL] 인덱싱 오류: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Vault 노트 LightRAG 임베딩")
    parser.add_argument("--folder", help="특정 폴더만 (예: 01-literature)")
    parser.add_argument("--dry-run", action="store_true", help="목록만 출력")
    args = parser.parse_args()

    if not args.dry_run and not check_lightrag():
        print("[FAIL] LightRAG가 실행 중이지 않습니다. docker compose up -d lightrag")
        return

    vault = Path(VAULT_PATH)
    folders = [args.folder] if args.folder else EMBED_FOLDERS

    total = success = skip = 0

    for folder_name in folders:
        folder = vault / folder_name
        if not folder.exists():
            continue

        md_files = [f for f in folder.glob("*.md") if f.name != "README.md"]
        if not md_files:
            continue

        print(f"\n[{folder_name}] {len(md_files)}개 노트")

        for md_file in sorted(md_files):
            total += 1
            content = read_note(md_file)
            if not content or len(content) < 50:
                print(f"  [SKIP] {md_file.name} (내용 없음)")
                skip += 1
                continue

            if args.dry_run:
                print(f"  [DRY] {md_file.name} ({len(content)} chars)")
                success += 1
                continue

            print(f"  [EMBED] {md_file.name}...", end=" ")
            ok = embed_document(content, md_file.name)
            if ok:
                print("OK")
                success += 1
            else:
                print("FAIL")
            # API 부하 방지 딜레이
            time.sleep(0.5)

    print(f"\n완료: {success}/{total} 성공, {skip} 건너뜀")


if __name__ == "__main__":
    main()
