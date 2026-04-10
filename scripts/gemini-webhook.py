"""
Gemini → Obsidian 웹훅 서버
북마크릿에서 POST 요청을 받아 Vault에 문헌 노트로 저장

실행:
  python scripts/gemini-webhook.py

기본 포트: 19999 (충돌 시 --port 옵션으로 변경)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

VAULT_PATH = os.environ.get(
    "OBSIDIAN_VAULT_PATH",
    "C:/Users/kjswi/Documents/googleDrive/ObsiVault"
)
SAVE_FOLDER = "01-literature"  # 저장 위치


def slugify(text: str) -> str:
    text = re.sub(r"[^\w가-힣\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text[:50].lower().strip("-")


def make_note(data: dict) -> str:
    """수신 데이터 → Obsidian 마크다운 노트"""
    today = datetime.now().strftime("%Y-%m-%d")
    title = data.get("title", "Gemini Chat").strip() or "Gemini Chat"
    messages = data.get("messages", [])
    url = data.get("url", "https://gemini.google.com")

    # Frontmatter
    lines = [
        "---",
        f'title: "{title}"',
        f"date: {today}",
        'type: "literature"',
        'source: "gemini"',
        f'url: "{url}"',
        'tags: [gemini, chat, literature]',
        "---",
        "",
        f"# {title}",
        "",
        f"> 출처: Gemini | {today}",
        "",
        "---",
        "",
    ]

    # 대화 내용
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "").strip()
        if not content:
            continue

        if role == "user":
            lines.append(f"## 질문")
            lines.append("")
            lines.append(content)
        else:
            lines.append(f"## Gemini 답변")
            lines.append("")
            lines.append(content)

        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """CORS preflight 처리"""
        self.send_response(200)
        self._set_cors()
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))

            note = make_note(data)
            today = datetime.now().strftime("%Y-%m-%d")
            title = data.get("title", "gemini-chat")
            slug = slugify(title)
            filename = f"{today}-gemini-{slug}.md"

            save_dir = Path(VAULT_PATH) / SAVE_FOLDER
            save_dir.mkdir(parents=True, exist_ok=True)
            file_path = save_dir / filename
            file_path.write_text(note, encoding="utf-8")

            print(f"[저장] {file_path}")
            self._respond(200, {"status": "ok", "file": filename})

        except Exception as e:
            print(f"[오류] {e}", file=sys.stderr)
            self._respond(500, {"status": "error", "message": str(e)})

    def _respond(self, code: int, body: dict):
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self._set_cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _set_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, fmt, *args):
        print(f"[{self.address_string()}] {fmt % args}")


def main():
    parser = argparse.ArgumentParser(description="Gemini → Obsidian 웹훅 서버")
    parser.add_argument("--port", type=int, default=19999)
    args = parser.parse_args()

    print(f"Gemini 웹훅 서버 시작: http://localhost:{args.port}")
    print(f"저장 경로: {VAULT_PATH}/{SAVE_FOLDER}/")
    print("종료: Ctrl+C")

    server = HTTPServer(("localhost", args.port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n서버 종료")


if __name__ == "__main__":
    main()
