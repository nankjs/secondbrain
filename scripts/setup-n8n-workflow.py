"""
n8n 워크플로우 API 등록 스크립트 (P2-T7)
n8n-workflows/collection-pipeline.json을 n8n에 임포트
"""

import json
import urllib.request
import urllib.error
import base64
import sys
import os

N8N_URL = "http://localhost:15678"
USERNAME = "admin"
PASSWORD = "secondbrain2026"
WORKFLOW_FILE = os.path.join(
    os.path.dirname(__file__),
    "../n8n-workflows/collection-pipeline-n8n.json"
)


def api_request(method: str, path: str, data: dict = None) -> dict:
    url = N8N_URL + "/api/v1" + path
    token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode()
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        content = e.read().decode()
        return {"error": f"HTTP {e.code}: {content[:300]}"}
    except Exception as e:
        return {"error": str(e)}


def create_workflow() -> dict:
    """n8n에 기본 워크플로우 생성"""
    workflow = {
        "name": "secondbrain-weekly-collection",
        "nodes": [
            {
                "id": "cron-trigger",
                "name": "Weekly Monday 09:00 KST",
                "type": "n8n-nodes-base.cron",
                "typeVersion": 1,
                "position": [250, 300],
                "parameters": {
                    "triggerTimes": {
                        "item": [{"mode": "everyWeek", "hour": 0, "minute": 0, "weekday": 1}]
                    }
                }
            },
            {
                "id": "miniflux-fetch",
                "name": "Fetch MiniFlux Entries",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 3,
                "position": [450, 300],
                "parameters": {
                    "method": "GET",
                    "url": "http://miniflux:8080/v1/entries?status=unread&limit=20",
                    "authentication": "genericCredentialType",
                    "genericAuthType": "basicAuth",
                    "options": {}
                }
            },
            {
                "id": "arxiv-fetch",
                "name": "Fetch ArXiv Papers",
                "type": "n8n-nodes-base.executeCommand",
                "typeVersion": 1,
                "position": [450, 450],
                "parameters": {
                    "command": "python C:/KJS/AVARTA/secondBrain/scripts/collect-arxiv.py --query combined --max 5 --days 14"
                }
            },
            {
                "id": "set-status",
                "name": "Collection Status",
                "type": "n8n-nodes-base.set",
                "typeVersion": 1,
                "position": [650, 350],
                "parameters": {
                    "values": {
                        "string": [
                            {"name": "status", "value": "collected"},
                            {"name": "collected_at", "value": "={{$now}}"}
                        ]
                    }
                }
            }
        ],
        "connections": {
            "Weekly Monday 09:00 KST": {
                "main": [[
                    {"node": "Fetch MiniFlux Entries", "type": "main", "index": 0},
                    {"node": "Fetch ArXiv Papers", "type": "main", "index": 0}
                ]]
            },
            "Fetch MiniFlux Entries": {
                "main": [[{"node": "Collection Status", "type": "main", "index": 0}]]
            }
        },
        "active": False,
        "settings": {"timezone": "Asia/Seoul"},
        "tags": [{"name": "secondbrain"}, {"name": "collection"}]
    }
    return api_request("POST", "/workflows", workflow)


def main():
    print("n8n 워크플로우 등록")
    print(f"  서버: {N8N_URL}")

    # 기존 워크플로우 확인
    existing = api_request("GET", "/workflows")
    if "error" not in existing:
        wf_list = existing.get("data", [])
        for wf in wf_list:
            if "secondbrain" in wf.get("name", ""):
                print(f"  [SKIP] 이미 존재: {wf['name']} (ID={wf['id']})")
                return

    result = create_workflow()
    if "error" in result:
        print(f"  [FAIL] {result['error']}")
        sys.exit(1)
    else:
        wf_id = result.get("id", "?")
        print(f"  [OK] 워크플로우 생성: secondbrain-weekly-collection (ID={wf_id})")
        print(f"\n  n8n UI: {N8N_URL}")
        print(f"  로그인: admin / secondbrain2026")
        print(f"  워크플로우 활성화 후 '매주 월요일 09:00 KST' 자동 실행")


if __name__ == "__main__":
    main()
