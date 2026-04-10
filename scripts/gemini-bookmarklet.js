/**
 * Gemini → Obsidian 북마크릿 (소스 원본)
 *
 * 브라우저 북마크에 등록할 때는 아래 "북마크릿 코드" 섹션을 사용하세요.
 * 이 파일은 가독성을 위한 원본입니다.
 */

(function () {
  const WEBHOOK = "http://localhost:19999";

  // ── 1. 페이지 확인 ──────────────────────────────────────────
  if (!location.hostname.includes("gemini.google.com")) {
    alert("Gemini 페이지에서만 사용하세요.");
    return;
  }

  // ── 2. 제목 추출 ────────────────────────────────────────────
  const title =
    document.title.replace(/\s*[-–|]\s*Gemini.*$/i, "").trim() ||
    document.querySelector("h1, .conversation-title")?.textContent?.trim() ||
    "Gemini Chat";

  // ── 3. 메시지 추출 ──────────────────────────────────────────
  const messages = [];

  // Gemini DOM 셀렉터 (버전 변경 시 아래 목록에 추가)
  const selectors = {
    turn: [
      "message-content",           // 최신
      "[data-turn-index]",
      ".conversation-turn",
      "model-response, user-query",
    ],
    user: [
      ".user-query-text-line",
      "[data-message-author-role='user']",
      ".user-request-text",
      "user-query .query-text",
    ],
    model: [
      ".model-response-text",
      "[data-message-author-role='model']",
      ".response-content",
      "model-response .response-text",
      ".markdown-main-panel",
    ],
  };

  // 방법 A: user/model 쌍으로 추출
  const userEls = document.querySelectorAll(selectors.user.join(","));
  const modelEls = document.querySelectorAll(selectors.model.join(","));

  const maxLen = Math.max(userEls.length, modelEls.length);

  if (maxLen > 0) {
    for (let i = 0; i < maxLen; i++) {
      if (userEls[i]) {
        messages.push({ role: "user", content: userEls[i].innerText.trim() });
      }
      if (modelEls[i]) {
        messages.push({ role: "model", content: modelEls[i].innerText.trim() });
      }
    }
  }

  // 방법 B: 아무것도 못 잡으면 전체 텍스트 폴백
  if (messages.length === 0) {
    const body = document.querySelector("main, .conversation-container, body");
    messages.push({ role: "model", content: body?.innerText?.trim() || "(내용 없음)" });
  }

  // ── 4. 전송 ────────────────────────────────────────────────
  const payload = {
    title: title,
    url: location.href,
    messages: messages,
    captured_at: new Date().toISOString(),
  };

  fetch(WEBHOOK, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then((r) => r.json())
    .then((res) => {
      if (res.status === "ok") {
        alert("✅ Obsidian에 저장됨\n파일: " + res.file);
      } else {
        alert("❌ 저장 실패: " + res.message);
      }
    })
    .catch((e) => {
      alert("❌ 서버 연결 실패\n서버가 실행 중인지 확인하세요.\n\npython scripts/gemini-webhook.py");
    });
})();
