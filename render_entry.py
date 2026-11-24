#!/usr/bin/env python3
"""Render Web Service entry point.

1. Starts a tiny HTTP server on $PORT (Render requires a web service to listen).
2. Pings its own public URL (RENDER_EXTERNAL_URL) every KEEPALIVE_SECONDS so the
   free instance is less likely to spin down after 15 min without traffic.
   An external monitor (UptimeRobot, every 5 min) is still the more reliable option.
3. Runs the Telegram bot (long polling) unchanged.
"""
import os
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer


class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"tts-bot ok"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    do_HEAD = do_GET

    def log_message(self, *args):
        pass


def start_health_server():
    port = int(os.getenv("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), Health)
    threading.Thread(target=server.serve_forever, daemon=True).start()


def start_keepalive():
    url = os.getenv("RENDER_EXTERNAL_URL", "").strip()
    interval = int(os.getenv("KEEPALIVE_SECONDS", "600"))
    if not url or interval <= 0:
        return

    def loop():
        time.sleep(60)
        while True:
            try:
                urllib.request.urlopen(url, timeout=20).read()
            except Exception:
                pass
            time.sleep(interval)

    threading.Thread(target=loop, daemon=True).start()


if __name__ == "__main__":
    start_health_server()
    start_keepalive()
    import tts_bot_fixed
    tts_bot_fixed.main()
