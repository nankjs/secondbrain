"""
Google Takeout Gemini 채팅 기록 → Obsidian 노트 변환

사용법:
  python scripts/parse-gemini-history.py --input <HTML파일> [--dry-run]

동작:
  1. HTML 파싱 → 425개 대화 추출
  2. DeepSeek V3로 주제 분류 (배치 처리)
  3. 주제별 MD 노트 → ObsiVault/04-gemini/
  4. auto-linking이 관심사 신호로 활용
"""

import argparse
import html as html_lib
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

VAULT = os.environ.get("OBSIDIAN_VAULT_PATH", "C:/Users/kjswi/Documents/googleDrive/ObsiVault")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
OUTPUT_FOLDER = "04-gemini"
BATCH_SIZE = 20  # 주제 분류 배치 크기


# ── 파싱 ────────────────────────────────────────────────────────

def parse_conversations(html_path: str) -> list[dict]:
    """HTML에서 대화 추출: {query, response, timestamp}"""
    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    cells = re.findall(
        r'class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">(.+?)</div>',
        content, re.DOTALL
    )

    conversations = []
    for cell in cells:
        text = html_lib.unescape(re.sub(r'<[^>]+>', ' ', cell))
        text = re.sub(r'\s+', ' ', text).strip()

        # "항목을 검색함 YYYY. M. D. 오전/오후 HH:MM:SS KST" 패턴으로 분리
        m = re.search(
            r'항목을 검색함\s+(\d{4}\.\s*\d{1,2}\.\s*\d{1,2}\.\s*(?:오전|오후)\s*[\d:]+\s*KST)',
            text
        )
        if not m:
            continue

        query = text[:m.start()].strip()
        ts_raw = m.group(1).strip()
        response = text[m.end():].strip()

        if not query or not response:
            continue

        # 타임스탬프 파싱
        ts_clean = re.sub(r'\s+', ' ', ts_raw)
        try:
            # "2026. 4. 22. 오후 12:43:46 KST" → datetime
            ts_clean = ts_clean.replace('KST', '').strip()
            ampm_match = re.search(r'(오전|오후)\s*([\d:]+)', ts_clean)
            date_match = re.search(r'(\d{4})\.\s*(\d{1,2})\.\s*(\d{1,2})\.', ts_clean)
            if date_match and ampm_match:
                year, month, day = date_match.groups()
                ampm, time_str = ampm_match.groups()
                h, mi, s = time_str.split(':')
                h = int(h)
                if ampm == '오후' and h != 12:
                    h += 12
                elif ampm == '오전' and h == 12:
                    h = 0
                dt = datetime(int(year), int(month), int(day), h, int(mi), int(s))
                date_str = dt.strftime("%Y-%m-%d")
            else:
                date_str = "unknown"
        except Exception:
            date_str = "unknown"

        conversations.append({
            "query": query,
            "response": response[:2000],
            "timestamp": ts_raw,
            "date": date_str,
        })

    return conversations


# ── 주제 분류 ────────────────────────────────────────────────────

def assign_topics_batch(queries: list[str]) -> list[str]:
    """DeepSeek V3로 쿼리 목록에 주제 레이블 일괄 부여"""
    numbered = "\n".join(f"{i+1}. {q[:120]}" for i, q in enumerate(queries))
    prompt = (
        "다음 Gemini 대화 쿼리 목록을 보고 각 쿼리에 한국어 주제 레이블을 부여하라.\n"
        "주제는 5~15자의 명사형으로, 같은 주제면 동일한 레이블을 사용하라.\n"
        "예시 주제: 옵시디언 활용, 기독교 신앙, AI/LLM 기술, 건설 클레임, 성경 공부, "
        "경제/투자, 학습 방법, 프로그래밍, 교회 사역, 물리학\n\n"
        f"쿼리 목록:\n{numbered}\n\n"
        "응답 형식(JSON 배열만, 다른 텍스트 없이):\n"
        '["주제1", "주제2", ...]'
    )

    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 800,
    }).encode("utf-8")

    req = urllib.request.Request(
        DEEPSEEK_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            result = json.loads(r.read())
            response = result["choices"][0]["message"]["content"].strip()

        arr_match = re.search(r'\[.+\]', response, re.DOTALL)
        if arr_match:
            topics = json.loads(arr_match.group())
            if len(topics) == len(queries):
                return topics
    except Exception as e:
        print(f"  [WARN] 주제 분류 실패: {e}", file=sys.stderr)

    return ["기타"] * len(queries)


def assign_all_topics(conversations: list[dict]) -> list[dict]:
    """전체 대화에 주제 배정 (배치 처리)"""
    queries = [c["query"] for c in conversations]
    all_topics = []

    total_batches = (len(queries) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(0, len(queries), BATCH_SIZE):
        batch = queries[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        print(f"  주제 분류 배치 {batch_num}/{total_batches} ({len(batch)}개)...", file=sys.stderr)
        topics = assign_topics_batch(batch)
        all_topics.extend(topics)
        time.sleep(0.5)

    for conv, topic in zip(conversations, all_topics):
        conv["topic"] = topic

    return conversations


# ── 노트 생성 ────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s가-힣]", "", text)
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", text.strip()))[:40].lower().strip("-")


def build_topic_note(topic: str, convs: list[dict]) -> str:
    convs_sorted = sorted(convs, key=lambda c: c["date"])
    date_range = f"{convs_sorted[0]['date']} ~ {convs_sorted[-1]['date']}"
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"---",
        f'title: "{topic}"',
        f"date: {today}",
        f"type: interest-signal",
        f"source: gemini-history",
        f"topic: \"{topic}\"",
        f"conversation_count: {len(convs)}",
        f"date_range: \"{date_range}\"",
        f"tags: [gemini, interest-signal, {slugify(topic)}]",
        f"---",
        f"",
        f"# {topic}",
        f"",
        f"> Gemini 채팅 기록 | {len(convs)}개 대화 | {date_range}",
        f"",
        f"---",
        f"",
    ]

    for conv in convs_sorted:
        lines += [
            f"## {conv['date']} — {conv['query'][:60]}",
            f"",
            f"**질문:** {conv['query']}",
            f"",
            f"{conv['response']}",
            f"",
            f"---",
            f"",
        ]

    return "\n".join(lines)


# ── 메인 ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Gemini 채팅 기록 → Obsidian 노트")
    parser.add_argument("--input", required=True, help="HTML 파일 경로")
    parser.add_argument("--dry-run", action="store_true", help="파일 저장 없이 분석만")
    args = parser.parse_args()

    if not DEEPSEEK_API_KEY:
        print("[FAIL] DEEPSEEK_API_KEY 미설정", file=sys.stderr)
        sys.exit(1)

    print(f"[파싱] {args.input}", file=sys.stderr)
    conversations = parse_conversations(args.input)
    print(f"[파싱] {len(conversations)}개 대화 추출 완료", file=sys.stderr)

    print("[주제 분류] DeepSeek V3 배치 처리 중...", file=sys.stderr)
    conversations = assign_all_topics(conversations)

    # 주제별 그룹핑
    topic_groups: dict[str, list] = {}
    for conv in conversations:
        topic = conv.get("topic", "기타")
        topic_groups.setdefault(topic, []).append(conv)

    print(f"\n[주제 목록] {len(topic_groups)}개 주제:", file=sys.stderr)
    for topic, convs in sorted(topic_groups.items(), key=lambda x: -len(x[1])):
        print(f"  {topic}: {len(convs)}개", file=sys.stderr)

    if args.dry_run:
        print("\n[DRY RUN] 파일 저장 생략", file=sys.stderr)
        return

    # 저장
    out_dir = Path(VAULT) / OUTPUT_FOLDER
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for topic, convs in topic_groups.items():
        filename = f"gemini-{slugify(topic)}.md"
        filepath = out_dir / filename
        note = build_topic_note(topic, convs)
        filepath.write_text(note, encoding="utf-8")
        saved.append(str(filepath))
        print(f"  [저장] {filename} ({len(convs)}개 대화)", file=sys.stderr)

    print(f"\n[완료] {len(saved)}개 파일 → {out_dir}", file=sys.stderr)
    print(json.dumps({"topic_count": len(saved), "conversation_count": len(conversations)}))


if __name__ == "__main__":
    main()
