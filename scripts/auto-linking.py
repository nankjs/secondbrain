"""
자동 노트 연결 스크립트 (P3-T6)
LightRAG 유사도 + /relate 스킬 로직으로 노트 간 링크 자동 생성

사용법:
  python scripts/auto-linking.py                  # 전체 Vault 연결 분석
  python scripts/auto-linking.py --dry-run        # 링크 없이 분석만
  python scripts/auto-linking.py --note "파일명"  # 특정 노트만
  python scripts/auto-linking.py --threshold 0.7  # 유사도 임계값 조정
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

LIGHTRAG_API = "http://localhost:9621"
VAULT_PATH = os.environ.get(
    "OBSIDIAN_VAULT_PATH",
    "C:/Users/kjswi/Documents/googleDrive/ObsiVault"
)

# 연결 분석할 폴더
LINK_FOLDERS = ["01-literature", "02-permanent"]

# 강도 임계값
THRESHOLD_STRONG = 0.7   # → Obsidian 링크 생성
THRESHOLD_WEAK   = 0.5   # → 태그만 추가
THRESHOLD_IGNORE = 0.5   # 미만 → 무시


def search_related(query: str, mode: str = "naive", top_k: int = 5) -> str:
    """LightRAG로 관련 내용 검색"""
    payload = json.dumps({
        "query": query,
        "mode": mode,
        "only_need_context": True,
        "top_k": top_k
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{LIGHTRAG_API}/query",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            return result.get("response", "")
    except Exception:
        return ""


def extract_title(content: str, filename: str) -> str:
    """노트에서 제목 추출"""
    # frontmatter source_title 우선
    m = re.search(r'source_title:\s*["\']?([^"\'\n]+)["\']?', content)
    if m:
        return m.group(1).strip()
    # H1 헤더
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # 파일명에서
    return filename.replace(".md", "").replace("-", " ")


def analyze_relation(note_a_title: str, note_a_content: str,
                     note_b_title: str, note_b_content: str) -> dict:
    """
    /relate 스킬 로직 구현
    두 노트 간의 관계 타입, 강도, 설명 반환
    """
    # 각 노트의 핵심 내용 (최대 500자)
    a_snippet = note_a_content[:500].replace("\n", " ")
    b_snippet = note_b_content[:500].replace("\n", " ")

    # LightRAG에 관계 분석 질의
    query = (
        f"Analyze the semantic relationship between these two notes:\n\n"
        f"Note A: '{note_a_title}'\n{a_snippet}\n\n"
        f"Note B: '{note_b_title}'\n{b_snippet}\n\n"
        f"Return JSON: {{\"relation_type\": \"context|extend|contradict|related|supports|inspired\", "
        f"\"strength\": 0.0-1.0, \"description\": \"brief description in Korean (max 50 chars)\", "
        f"\"bidirectional\": true/false}}"
    )

    payload = json.dumps({
        "query": query,
        "mode": "naive",
        "only_need_context": False,
        "response_type": "Single Paragraph"
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{LIGHTRAG_API}/query",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            response = result.get("response", "")

        # JSON 블록 추출
        json_match = re.search(r'\{[^{}]+\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception:
        pass

    # 폴백: 기본값
    return {
        "relation_type": "related",
        "strength": 0.0,
        "description": "관계 분석 실패",
        "bidirectional": False
    }


def has_link(content: str, target_title: str) -> bool:
    """노트에 이미 링크가 있는지 확인"""
    # [[파일명]] 형식
    return f"[[{target_title}" in content or target_title in content


def add_link_to_note(file_path: Path, target_title: str,
                     relation: dict, dry_run: bool = False) -> bool:
    """노트 하단에 관련 링크 섹션 추가"""
    content = file_path.read_text(encoding="utf-8")

    # 이미 링크 있으면 스킵
    if has_link(content, target_title):
        return False

    rel_type = relation["relation_type"]
    strength = relation["strength"]
    description = relation["description"]

    link_line = f"- [[{target_title}]] ({rel_type}, {strength:.2f}) — {description}"

    # 기존 관련 링크 섹션 있으면 추가
    if "## 관련 노트" in content:
        new_content = content.rstrip() + f"\n{link_line}\n"
    else:
        new_content = content.rstrip() + f"\n\n## 관련 노트\n{link_line}\n"

    if not dry_run:
        file_path.write_text(new_content, encoding="utf-8")

    return True


def collect_notes(folder: str) -> list[tuple[Path, str, str]]:
    """폴더에서 노트 수집: (path, title, content)"""
    vault = Path(VAULT_PATH)
    folder_path = vault / folder
    if not folder_path.exists():
        return []

    notes = []
    for md_file in sorted(folder_path.glob("*.md")):
        if md_file.name == "README.md":
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            title = extract_title(content, md_file.name)
            notes.append((md_file, title, content))
        except Exception:
            pass
    return notes


def main():
    parser = argparse.ArgumentParser(description="노트 자동 연결")
    parser.add_argument("--dry-run", action="store_true", help="분석만, 파일 수정 없음")
    parser.add_argument("--note", help="특정 노트 파일명")
    parser.add_argument("--threshold", type=float, default=THRESHOLD_STRONG,
                        help=f"링크 생성 임계값 (기본: {THRESHOLD_STRONG})")
    parser.add_argument("--folder", help="특정 폴더만 (예: 01-literature)")
    args = parser.parse_args()

    # LightRAG 상태 확인
    try:
        with urllib.request.urlopen(f"{LIGHTRAG_API}/health", timeout=5) as r:
            health = json.loads(r.read())
            if health.get("status") != "healthy":
                print("[FAIL] LightRAG가 준비되지 않았습니다.")
                sys.exit(1)
    except Exception as e:
        print(f"[FAIL] LightRAG 연결 실패: {e}")
        sys.exit(1)

    folders = [args.folder] if args.folder else LINK_FOLDERS
    all_notes: list[tuple[Path, str, str]] = []
    for folder in folders:
        all_notes.extend(collect_notes(folder))

    print(f"총 {len(all_notes)}개 노트 분석 시작")
    if args.dry_run:
        print("[DRY RUN] 파일 수정 없음")

    # 특정 노트 필터
    if args.note:
        all_notes = [(p, t, c) for p, t, c in all_notes if args.note in p.name]
        print(f"필터: {args.note} → {len(all_notes)}개")

    linked = 0
    skipped = 0
    pairs_analyzed = 0

    # 모든 노트 쌍 분석 (N*(N-1)/2)
    for i, (path_a, title_a, content_a) in enumerate(all_notes):
        for j, (path_b, title_b, content_b) in enumerate(all_notes):
            if i >= j:  # 중복 방지
                continue

            pairs_analyzed += 1
            print(f"\n[{pairs_analyzed}] {title_a[:30]} ↔ {title_b[:30]}")

            relation = analyze_relation(title_a, content_a, title_b, content_b)
            strength = relation.get("strength", 0.0)
            rel_type = relation.get("relation_type", "related")
            desc = relation.get("description", "")
            bidir = relation.get("bidirectional", False)

            print(f"  타입: {rel_type}, 강도: {strength:.2f}, {desc}")

            if strength < args.threshold:
                print(f"  [SKIP] 임계값 미달 ({strength:.2f} < {args.threshold})")
                skipped += 1
                time.sleep(0.3)
                continue

            # A → B 링크
            if add_link_to_note(path_a, title_b, relation, args.dry_run):
                action = "[DRY]" if args.dry_run else "[LINK]"
                print(f"  {action} {path_a.name} → [[{title_b}]]")
                linked += 1

            # 양방향이면 B → A 도 링크
            if bidir:
                rev_relation = dict(relation)
                if add_link_to_note(path_b, title_a, rev_relation, args.dry_run):
                    action = "[DRY]" if args.dry_run else "[LINK]"
                    print(f"  {action} {path_b.name} → [[{title_a}]]")
                    linked += 1

            time.sleep(0.5)  # API 부하 방지

    print(f"\n완료: {pairs_analyzed}쌍 분석, {linked}개 링크 생성, {skipped}개 스킵")


if __name__ == "__main__":
    main()
