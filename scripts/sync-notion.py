"""
Obsidian Vault -> Notion 동기화 (P5-T3)

핵심 해결책:
  - json.dumps(ensure_ascii=False)로 유니코드 서로게이트 문제 방지
  - 100블록 단위 청킹으로 Notion API 제한 우회
  - curl 대신 Python urllib로 완전한 인코딩 제어

사용법:
  python scripts/sync-notion.py --setup              # DB 생성 (최초 1회)
  python scripts/sync-notion.py                      # 전체 동기화
  python scripts/sync-notion.py --folder 01-literature  # 특정 폴더만
  python scripts/sync-notion.py --dry-run            # 목록만 출력
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

VAULT_PATH = os.environ.get(
    "OBSIDIAN_VAULT_PATH",
    "C:/Users/kjswi/Documents/googleDrive/ObsiVault"
)
NOTION_TOKEN = os.environ.get("NOTION_API_KEY", os.environ.get("NOTION_TOKEN", ""))
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "")

# 아바타 프로젝트 페이지 ID (세컨드브레인 DB의 부모)
PARENT_PAGE_ID = "33d2f5d3-8f22-80b4-8392-d7541c309957"

# 동기화 대상 폴더
SYNC_FOLDERS = ["01-literature", "02-permanent"]

# Notion API 블록 청킹 제한
CHUNK_SIZE = 90  # 여유있게 100 이하로 설정


def notion_request(method: str, endpoint: str, body: dict = None) -> dict:
    """Notion API 요청 — ensure_ascii=False로 서로게이트 문제 방지"""
    url = f"{NOTION_API}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

    data = None
    if body is not None:
        # ensure_ascii=False: 한국어/이모지를 UTF-8로 직접 인코딩
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        print(f"  [HTTP {e.code}] {body_text[:300]}", file=sys.stderr)
        return {"error": e.code, "message": body_text}
    except Exception as e:
        print(f"  [ERR] {e}", file=sys.stderr)
        return {"error": str(e)}


def create_database(parent_page_id: str) -> str:
    """세컨드브레인 Notion Database 생성"""
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "SecondBrain Vault"}}],
        "properties": {
            "Name": {"title": {}},
            "Folder": {
                "select": {
                    "options": [
                        {"name": "00-fleeting", "color": "gray"},
                        {"name": "01-literature", "color": "blue"},
                        {"name": "02-permanent", "color": "green"},
                    ]
                }
            },
            "Tags": {"multi_select": {}},
            "Source": {"url": {}},
            "Created": {"date": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "synced", "color": "green"},
                        {"name": "pending", "color": "yellow"},
                    ]
                }
            },
        },
    }

    result = notion_request("POST", "databases", payload)
    if "id" in result:
        db_id = result["id"]
        print(f"[OK] Database 생성: {db_id}")
        print(f"     .env에 추가: NOTION_DATABASE_ID={db_id}")
        return db_id
    else:
        print(f"[FAIL] Database 생성 실패: {result.get('message','')[:200]}")
        return ""


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """마크다운 Frontmatter 파싱, (meta, body) 반환"""
    meta = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2].strip()
            for line in fm_text.strip().splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip().strip('"')
    return meta, body


def md_line_to_blocks(line: str) -> list[dict]:
    """마크다운 한 줄을 Notion 블록으로 변환"""
    # 제목
    if line.startswith("### "):
        return [{"object": "block", "type": "heading_3",
                 "heading_3": {"rich_text": [{"type": "text", "text": {"content": line[4:]}}]}}]
    if line.startswith("## "):
        return [{"object": "block", "type": "heading_2",
                 "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:]}}]}}]
    if line.startswith("# "):
        return [{"object": "block", "type": "heading_1",
                 "heading_1": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}}]

    # 불릿 리스트
    if line.startswith("- ") or line.startswith("* "):
        return [{"object": "block", "type": "bulleted_list_item",
                 "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}}]

    # 번호 리스트
    m = re.match(r"^\d+\. (.+)", line)
    if m:
        return [{"object": "block", "type": "numbered_list_item",
                 "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": m.group(1)}}]}}]

    # 코드 블록 (단순 처리: 인라인 코드 제거)
    if line.startswith("```"):
        return []  # 코드 펜스는 건너뜀

    # 빈 줄 → 단락 구분
    if not line.strip():
        return [{"object": "block", "type": "paragraph",
                 "paragraph": {"rich_text": []}}]

    # 일반 단락 (2000자 제한 적용)
    text = line[:2000]
    return [{"object": "block", "type": "paragraph",
             "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}]


def md_to_blocks(body: str) -> list[dict]:
    """마크다운 본문 전체를 Notion 블록 리스트로 변환"""
    blocks = []
    in_code = False
    code_lines = []

    for line in body.splitlines():
        if line.startswith("```"):
            if in_code:
                # 코드 블록 닫기
                code_content = "\n".join(code_lines)[:2000]
                blocks.append({
                    "object": "block", "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": code_content}}],
                        "language": "plain text"
                    }
                })
                code_lines = []
                in_code = False
            else:
                in_code = True
        elif in_code:
            code_lines.append(line)
        else:
            blocks.extend(md_line_to_blocks(line))

    return blocks


def append_blocks_chunked(page_id: str, blocks: list[dict]) -> bool:
    """블록을 CHUNK_SIZE 단위로 분할 업로드"""
    for i in range(0, len(blocks), CHUNK_SIZE):
        chunk = blocks[i: i + CHUNK_SIZE]
        result = notion_request(
            "PATCH",
            f"blocks/{page_id}/children",
            {"children": chunk}
        )
        if "error" in result:
            return False
        # API 부하 방지
        time.sleep(0.3)
    return True


def get_existing_pages(database_id: str) -> dict:
    """DB에서 기존 동기화된 페이지 목록 조회 {파일명: page_id}"""
    existing = {}
    payload = {"page_size": 100}
    result = notion_request("POST", f"databases/{database_id}/query", payload)

    for page in result.get("results", []):
        name_prop = page.get("properties", {}).get("Name", {})
        titles = name_prop.get("title", [])
        if titles:
            filename = titles[0].get("plain_text", "")
            existing[filename] = page["id"]
    return existing


def sync_note(file_path: Path, folder_name: str, database_id: str,
              existing: dict, dry_run: bool) -> bool:
    """단일 노트를 Notion에 동기화"""
    content = file_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(content)

    title = meta.get("title", file_path.stem)
    tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    source = meta.get("source", meta.get("url", ""))
    created = meta.get("date", "")

    if dry_run:
        print(f"  [DRY] {file_path.name} → '{title}' ({len(body)} chars)")
        return True

    # 이미 존재하면 스킵 (업데이트 미구현)
    if file_path.name in existing:
        print(f"  [SKIP] {file_path.name} (이미 동기화됨)")
        return True

    # 페이지 속성 구성
    properties = {
        "Name": {"title": [{"type": "text", "text": {"content": title}}]},
        "Folder": {"select": {"name": folder_name}},
        "Status": {"select": {"name": "synced"}},
    }
    if tags:
        properties["Tags"] = {"multi_select": [{"name": t[:100]} for t in tags[:10]]}
    if source:
        properties["Source"] = {"url": source}
    if created:
        try:
            # YYYY-MM-DD 형식 검증
            if re.match(r"\d{4}-\d{2}-\d{2}", created):
                properties["Created"] = {"date": {"start": created[:10]}}
        except Exception:
            pass

    # 1단계: 페이지 생성 (내용 없이)
    page_payload = {
        "parent": {"database_id": database_id},
        "properties": properties,
    }
    result = notion_request("POST", "pages", page_payload)
    if "id" not in result:
        print(f"  [FAIL] 페이지 생성 실패: {result.get('message','')[:150]}")
        return False

    page_id = result["id"]

    # 2단계: 본문 블록을 청킹하여 추가
    blocks = md_to_blocks(body)
    if blocks:
        ok = append_blocks_chunked(page_id, blocks)
        if not ok:
            print(f"  [WARN] {file_path.name} 블록 추가 부분 실패")
            return False

    print(f"  [OK] {file_path.name} → '{title}' ({len(blocks)} blocks)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Obsidian -> Notion 동기화")
    parser.add_argument("--setup", action="store_true", help="Notion DB 최초 생성")
    parser.add_argument("--folder", help="특정 폴더만 (예: 01-literature)")
    parser.add_argument("--dry-run", action="store_true", help="목록만 출력")
    args = parser.parse_args()

    if not NOTION_TOKEN:
        print("[FAIL] NOTION_TOKEN 환경변수가 없습니다. .env 확인")
        sys.exit(1)

    # DB 생성 모드
    if args.setup:
        db_id = create_database(PARENT_PAGE_ID)
        if db_id:
            # .env에 자동 업데이트
            env_path = Path(".env")
            if env_path.exists():
                env_text = env_path.read_text(encoding="utf-8")
                if "NOTION_DATABASE_ID=" in env_text:
                    env_text = re.sub(
                        r"NOTION_DATABASE_ID=.*",
                        f"NOTION_DATABASE_ID={db_id}",
                        env_text
                    )
                else:
                    env_text += f"\nNOTION_DATABASE_ID={db_id}\n"
                env_path.write_text(env_text, encoding="utf-8")
                print(f"[OK] .env 업데이트 완료")
        return

    # 동기화 모드
    database_id = NOTION_DATABASE_ID
    if not database_id:
        print("[FAIL] NOTION_DATABASE_ID가 없습니다. 먼저 --setup 실행")
        sys.exit(1)

    vault = Path(VAULT_PATH)
    folders = [args.folder] if args.folder else SYNC_FOLDERS

    # 기존 동기화 페이지 목록
    existing = {} if args.dry_run else get_existing_pages(database_id)

    total = success = skip = fail = 0

    for folder_name in folders:
        folder = vault / folder_name
        if not folder.exists():
            print(f"[SKIP] 폴더 없음: {folder}")
            continue

        md_files = [f for f in folder.glob("*.md") if f.name != "README.md"]
        if not md_files:
            print(f"[{folder_name}] 노트 없음")
            continue

        print(f"\n[{folder_name}] {len(md_files)}개 노트")

        for md_file in sorted(md_files):
            total += 1
            ok = sync_note(md_file, folder_name, database_id, existing, args.dry_run)
            if ok:
                success += 1
            else:
                fail += 1
            time.sleep(0.5)

    print(f"\n완료: {success}/{total} 성공, {fail} 실패")


if __name__ == "__main__":
    main()
