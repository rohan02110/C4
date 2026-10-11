#!/usr/bin/env python3
"""
unlock_daemon.py — Ashwatthama Host & Quarantine Server
Listens on:
- Port 80 (Public): Serves quarantine dashboard & download of ashwatthama_trace.mem.zip
- Port 8081 (Internal): Webhook receiver for Drona Vault (Case 4471 unlock dispatch)
"""

import os
import sys
import threading
from urllib.parse import parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler

VAULT_DIR = os.getenv("VAULT_DIR", "/vault")
ZIP_FILE = os.path.join(VAULT_DIR, "ashwatthama_trace.mem.zip")

# In-memory unlock state
UNLOCKED_STATE = {
    "unlocked": False,
    "unlocked_by": None,
    "timestamp": None
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ashwatthama Host — Quarantine Vault</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #030712;
            color: #f3f4f6;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .terminal {
            width: 100%;
            max-width: 750px;
            background: #111827;
            border: 1px solid {BORDER_COLOR};
            box-shadow: 0 0 25px {GLOW_COLOR};
            border-radius: 8px;
            overflow: hidden;
        }
        .header {
            background: #1f2937;
            padding: 12px 18px;
            border-bottom: 1px solid #374151;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .badge {
            font-size: 11px;
            font-weight: bold;
            padding: 3px 8px;
            border-radius: 4px;
            background: {BADGE_BG};
            color: {BADGE_COLOR};
        }
        .content {
            padding: 24px;
            line-height: 1.6;
        }
        .status-box {
            background: #030712;
            border: 1px solid #374151;
            border-radius: 6px;
            padding: 16px;
            margin: 18px 0;
            font-size: 13px;
        }
        .btn {
            display: inline-block;
            background: {BTN_BG};
            color: {BTN_COLOR};
            padding: 12px 20px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 6px;
            border: 1px solid {BTN_BORDER};
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .btn:hover {
            box-shadow: 0 0 15px {GLOW_COLOR};
        }
        .log {
            color: #9ca3af;
            font-size: 12px;
            margin-top: 16px;
        }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="header">
            <div>[HOST: ashwatthama.internal] // KURUKSHETRA DEFENSE GRID</div>
            <div class="badge">{STATUS_TEXT}</div>
        </div>
        <div class="content">
            <h2 style="color: #f97316; margin-bottom: 8px;">RING 4: ASHWATTHAMA'S MEMORY ISOLATION</h2>
            <p style="color: #9ca3af; font-size: 13px;">
                Quarantine Node <code>vyuha_sync.exe</code> (PID: 4472). In-memory volatile forensic dump intercepted.
            </p>

            <div class="status-box">
                <div><strong>LOCK STATE:</strong> {STATUS_TEXT}</div>
                <div><strong>SYNCHRONIZATION:</strong> {SYNC_STATUS}</div>
                <div><strong>TARGET ARTIFACT:</strong> ashwatthama_trace.mem.zip ({FILE_SIZE})</div>
            </div>

            {ACTION_SECTION}

            <div class="log">
                <div>[SYSTEM] Memory VAD descriptors locked under military clearance.</div>
                <div>[SYSTEM] Webhook trigger listening on internal interface (port 8081).</div>
                <div>[HINT] Inject Case 4471 into Drona's Archive (Ring 3) to trigger autonomous unlock dispatch.</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

class PublicHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress noisy log outputs

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            is_unlocked = UNLOCKED_STATE["unlocked"]
            file_size = "12.5 MB" if os.path.exists(ZIP_FILE) else "PENDING"

            if is_unlocked:
                border_color = "#10b981"
                glow_color = "rgba(16, 185, 129, 0.2)"
                badge_bg = "#064e3b"
                badge_color = "#34d399"
                status_text = "UNLOCKED // CLEARANCE 4471 VERIFIED"
                sync_status = "Webhook dispatched by Drona Vault. Case 4471 verified."
                btn_bg = "#059669"
                btn_color = "#ffffff"
                btn_border = "#10b981"
                action_section = f'<a href="/downloads/ashwatthama_trace.mem.zip" class="btn">⬇ DOWNLOAD FORENSIC ARTIFACT (ashwatthama_trace.mem.zip)</a>'
            else:
                border_color = "#ef4444"
                glow_color = "rgba(239, 68, 68, 0.2)"
                badge_bg = "#7f1d1d"
                badge_color = "#f87171"
                status_text = "QUARANTINE ENFORCED // ACCESS DENIED"
                sync_status = "Awaiting Drona Vault SQL Webhook dispatch (Case 4471)..."
                btn_bg = "#374151"
                btn_color = "#9ca3af"
                btn_border = "#4b5563"
                action_section = '<div style="color: #ef4444; font-weight: bold;">[ACCESS FORBIDDEN] Ashwatthama vault locked. Trigger Drona SQLi (Case 4471) to unlock.</div>'

            html = HTML_TEMPLATE.replace("{BORDER_COLOR}", border_color)\
                                .replace("{GLOW_COLOR}", glow_color)\
                                .replace("{BADGE_BG}", badge_bg)\
                                .replace("{BADGE_COLOR}", badge_color)\
                                .replace("{STATUS_TEXT}", status_text)\
                                .replace("{SYNC_STATUS}", sync_status)\
                                .replace("{FILE_SIZE}", file_size)\
                                .replace("{BTN_BG}", btn_bg)\
                                .replace("{BTN_COLOR}", btn_color)\
                                .replace("{BTN_BORDER}", btn_border)\
                                .replace("{ACTION_SECTION}", action_section)
            self.wfile.write(html.encode("utf-8"))

        elif path == "/downloads/ashwatthama_trace.mem.zip":
            if not UNLOCKED_STATE["unlocked"]:
                self.send_response(403)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "FORBIDDEN", "message": "Access Denied: Case 4471 clearance required from Drona\'s Vault."}')
                return

            if not os.path.exists(ZIP_FILE):
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "NOT_FOUND", "message": "Forensic zip artifact missing on disk."}')
                return

            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", 'attachment; filename="ashwatthama_trace.mem.zip"')
            self.send_header("Content-Length", str(os.path.getsize(ZIP_FILE)))
            self.end_headers()
            with open(ZIP_FILE, "rb") as f:
                while chunk := f.read(64 * 1024):
                    self.wfile.write(chunk)

        elif path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok", "service": "ashwatthama-host"}')
        else:
            self.send_response(404)
            self.end_headers()

class InternalWebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_POST(self):
        self.handle_unlock()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            unlocked = UNLOCKED_STATE["unlocked"]
            self.wfile.write(f'{{"unlocked": {str(unlocked).lower()}}}'.encode())
        elif parsed.path == "/unlock":
            self.handle_unlock()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_unlock(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        case_id = query.get("case", [""])[0]

        if case_id == "4471":
            UNLOCKED_STATE["unlocked"] = True
            UNLOCKED_STATE["unlocked_by"] = "Case 4471 (Drona SQLi Webhook)"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "success", "message": "Ashwatthama memory artifact unlocked successfully."}')
        else:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "error", "message": "Invalid or missing case clearance parameter."}')

def run_servers():
    print("[*] Starting Ashwatthama Host services...")
    # Public server on Port 80
    public_server = HTTPServer(("0.0.0.0", 80), PublicHandler)
    t1 = threading.Thread(target=public_server.serve_forever, daemon=True)
    t1.start()
    print("[+] Public quarantine web portal active on port 80")

    # Internal webhook receiver on Port 8081
    internal_server = HTTPServer(("0.0.0.0", 8081), InternalWebhookHandler)
    t2 = threading.Thread(target=internal_server.serve_forever, daemon=True)
    t2.start()
    print("[+] Internal webhook receiver active on port 8081")

    # Keep main thread alive
    t1.join()

if __name__ == "__main__":
    run_servers()
