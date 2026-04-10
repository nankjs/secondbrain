"""
Obsidian Vault 저장 스크립트 (P2-T10)
n8n에서 Claude가 생성한 마크다운 노트를 Vault에 저장

사용법:
  python scripts/save-to-vault.py --file /path/to/note.md
  python scripts/save-to-vault.py --content "---\n..." --domain academic --date 2026-04-10
"""

import argparse
import os
import re
import sys
from datetime import datetime

VAULT = os.environ.get(
    "OBSIDIAN_VAULT_PATH",
    "C:/Users/kjswi/Documents/googleDrive/ObsiVault"
)

DOMAIN_FOLDER_MAP = {
    "christian":  "01-literature",
    "academic":   "01-literature",
    "economy":    "01-literature",
    "general":    "01-literature",
    "fleeting":   "00-fleeting",
    "permanent":  "02-permanent",
}


def extract_frontmatter_value(content: str, key: str) -> str:
    """frontmatter에서 특정 키 값 추출"""
    pattern = rf"^{key}:\s*(.+)$"
    match = re.search(pattern, content, re.MULTILINE)
    return match.group(1).strip().strip('"') if match else ""


def make_filename(content: str, domain: str, date: str) -> str:
    """노트 내용에서 파일명 생성"""
    # 제목 추출 (첫 번째 # 헤더)
    title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = "untitled"

    # 파일명 안전화: 특수문자 제거, 공백→하이픈
    slug = re.sub(r"[^\w\s가-힣]", "", title)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = slug[:50]  # 최대 50자

    return f"{date}-{domain}-{slug}.md"


def save_note(content: str, domain: str, date: str) -> str:
    """노트를 적절한 폴더에 저장. 저장된 경로 반환."""
    folder_name = DOMAIN_FOLDER_MAP.get(domain, "01-literature")
    folder_path = os.path.join(VAULT, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    filename = make_filename(content, domain, date)
    filepath = os.path.join(folder_path, filename)

    # 중복 파일명 처리
    if os.path.exists(filepath):
        base, ext = os.path.splitext(filepath)
        counter = 1
        while os.path.exists(f"{base}-{counter}{ext}"):
            counter += 1
        filepath = f"{base}-{counter}{ext}"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def main():
    parser = argparse.ArgumentParser(description="Obsidian Vault에 노트 저장")
    parser.add_argument("--file", help="저장할 마크다운 파일 경로")
    parser.add_argument("--content", help="저장할 마크다운 내용 (직접 입력)")
    parser.add_argument("--domain", default="general", help="도메인 (christian/academic/economy/general)")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="날짜 (YYYY-MM-DD)")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            content = f.read()
    elif args.content:
        content = args.content.replace("\\n", "\n")
    else:
        # stdin에서 읽기
        content = sys.stdin.read()

    if not content.strip():
        print("오류: 저장할 내용이 없습니다", file=sys.stderr)
        sys.exit(1)

    # frontmatter에서 domain 자동 감지
    fm_domain = extract_frontmatter_value(content, "domain")
    if fm_domain:
        args.domain = fm_domain

    saved_path = save_note(content, args.domain, args.date)
    print(f"저장 완료: {saved_path}")
    return saved_path


if __name__ == "__main__":
    main()
