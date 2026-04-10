"""
인덱스 페이지 자동 생성 스크립트 (P1-T7 /index 스킬 Python 구현)
n8n 수집 완료 후 자동 실행
"""

import os
import re
from datetime import datetime
from collections import defaultdict

VAULT = os.environ.get(
    "OBSIDIAN_VAULT_PATH",
    "C:/Users/kjswi/Documents/googleDrive/ObsiVault"
)

SKIP_FOLDERS = {"04-templates", "05-attachments", ".obsidian", "06-index"}


def parse_frontmatter(content: str) -> dict:
    fm = {}
    if not content.startswith("---"):
        return fm
    end = content.find("---", 3)
    if end < 0:
        return fm
    for line in content[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"')
    return fm


def get_title(content: str, filename: str) -> str:
    match = re.search(r"^# (.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return filename.replace(".md", "").replace("-", " ")


def scan_vault():
    notes = []
    for root, dirs, files in os.walk(VAULT):
        # 제외 폴더
        dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS and not d.startswith(".")]
        rel_root = os.path.relpath(root, VAULT)

        for fname in files:
            if not fname.endswith(".md") or fname == "README.md":
                continue
            path = os.path.join(root, fname)
            rel_path = os.path.relpath(path, VAULT).replace("\\", "/")
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue

            fm = parse_frontmatter(content)
            if not fm.get("type"):
                continue

            notes.append({
                "rel_path": rel_path,
                "wikilink": f"[[{fname[:-3]}]]",
                "title": get_title(content, fname),
                "type": fm.get("type", ""),
                "domain": fm.get("domain", "general"),
                "tags": fm.get("tags", "[]"),
                "created": fm.get("created", "")[:10],
                "status": fm.get("status", ""),
            })

    return sorted(notes, key=lambda n: n["created"], reverse=True)


def generate_domain_index(notes: list) -> str:
    by_domain = defaultdict(lambda: defaultdict(list))
    for n in notes:
        by_domain[n["domain"]][n["type"]].append(n)

    domain_labels = {
        "christian": "기독교 (Christian)",
        "academic": "학술 (Academic)",
        "economy": "경제 (Economy)",
        "general": "일반 (General)",
    }

    lines = [
        "# 도메인별 인덱스\n",
        f"> 자동 생성: {datetime.now().strftime('%Y-%m-%d %H:%M')} | /index 스킬\n",
        "---\n",
    ]

    total_by_domain = {}
    for domain in ["christian", "academic", "economy", "general"]:
        if domain not in by_domain:
            continue
        type_data = by_domain[domain]
        total = sum(len(v) for v in type_data.values())
        total_by_domain[domain] = total
        lines.append(f"## {domain_labels[domain]} — {total}개\n")

        for ntype in ["permanent", "literature", "fleeting", "project"]:
            if ntype not in type_data:
                continue
            type_notes = type_data[ntype]
            type_label = {"permanent": "영구 노트", "literature": "문헌 노트",
                          "fleeting": "떠돌이 노트", "project": "프로젝트"}[ntype]
            lines.append(f"\n### {type_label} ({len(type_notes)}개)\n")
            for n in type_notes[:20]:  # 최대 20개
                lines.append(f"- {n['wikilink']} — {n['title']}\n")

        lines.append("\n---\n")

    # 통계 테이블
    lines.append("## 통계\n\n")
    lines.append("| 도메인 | 문헌 | 떠돌이 | 영구 | 합계 |\n")
    lines.append("|--------|------|--------|------|------|\n")
    grand_total = 0
    for domain in ["christian", "academic", "economy", "general"]:
        if domain not in by_domain:
            continue
        td = by_domain[domain]
        lit = len(td.get("literature", []))
        flt = len(td.get("fleeting", []))
        prm = len(td.get("permanent", []))
        tot = lit + flt + prm
        grand_total += tot
        lines.append(f"| {domain} | {lit} | {flt} | {prm} | {tot} |\n")
    lines.append(f"| **합계** | - | - | - | **{grand_total}** |\n")

    return "".join(lines)


def generate_tag_index(notes: list) -> str:
    by_tag = defaultdict(list)
    for n in notes:
        tags_str = n["tags"]
        tags = re.findall(r"[\w가-힣]+", tags_str)
        for tag in tags:
            by_tag[tag].append(n)

    lines = [
        "# 태그별 인덱스\n",
        f"> 자동 생성: {datetime.now().strftime('%Y-%m-%d %H:%M')} | /index 스킬\n",
        "---\n",
    ]

    for tag, tag_notes in sorted(by_tag.items(), key=lambda x: -len(x[1])):
        lines.append(f"\n## {tag} ({len(tag_notes)}개)\n")
        for n in tag_notes[:10]:
            lines.append(f"- {n['wikilink']} ({n['type']})\n")

    return "".join(lines)


def generate_date_index(notes: list) -> str:
    by_date = defaultdict(list)
    for n in notes:
        date = n["created"][:10] if n["created"] else "unknown"
        by_date[date].append(n)

    lines = [
        "# 최신 노트 (날짜별)\n",
        f"> 자동 생성: {datetime.now().strftime('%Y-%m-%d %H:%M')} | /index 스킬\n",
        "---\n",
    ]

    for date in sorted(by_date.keys(), reverse=True)[:30]:
        date_notes = by_date[date]
        suffix = " (오늘)" if date == datetime.now().strftime("%Y-%m-%d") else ""
        lines.append(f"\n## {date}{suffix} ({len(date_notes)}개)\n")
        for n in date_notes:
            lines.append(f"- {n['wikilink']} — {n['title']}\n")

    return "".join(lines)


def main():
    print("인덱스 생성 중...")
    notes = scan_vault()
    print(f"  노트 {len(notes)}개 발견")

    index_dir = os.path.join(VAULT, "06-index")
    os.makedirs(index_dir, exist_ok=True)

    files = {
        "index-by-domain.md": generate_domain_index(notes),
        "index-by-tag.md": generate_tag_index(notes),
        "index-by-date.md": generate_date_index(notes),
    }

    for fname, content in files.items():
        path = os.path.join(index_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ {fname}")

    print(f"\n완료: {len(notes)}개 노트 인덱싱")


if __name__ == "__main__":
    main()
