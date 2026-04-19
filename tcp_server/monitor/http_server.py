import json
import socketserver
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler

from config import SERVER_IP, HTTP_PORT
from core.state import server_state
from utils.logger import log


class MonitorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/stats":
            self._serve_stats()
        elif self.path == "/logs":
            self._serve_logs()
        elif self.path == "/":
            self._serve_index()
        else:
            self.send_error(404, "Endpoints: /stats dhe /logs")

    def _serve_stats(self):

        from core.client_handler import message_log

        with server_state["lock"]:
            clients_info = {
                addr: {
                    "name":          info["name"],
                    "ip":            info["ip"],
                    "port":          info["port"],
                    "privilege":     info["privilege"],
                    "priv":          info["priv"],
                    "connected_at":  info["connected_at"],
                    "message_count": len(info["messages"]),
                    "last_messages": [m["text"] for m in info["messages"][-5:]],
                }
                for addr, info in server_state["active_clients"].items()
            }

            stats = {
                "timestamp":            datetime.now().isoformat(),
                "timestamp_readable":   time.ctime(),
                "active_connections":   len(server_state["active_clients"]),
                "active_clients":       len(server_state["active_clients"]),
                "max_clients":          4,
                "total_connections":    server_state["total_connections"],
                "rejected_connections": server_state["rejected_connections"],
                "total_messages":       server_state["total_messages"],
                "clients":              clients_info,
                # 10 mesazhet e fundit nga message_log (nga kolegu)
                "recent_messages":      list(message_log[-10:]),
            }

        self._send_json(stats)

    def _serve_logs(self):
        from core.client_handler import message_log

        with server_state["lock"]:
            logs_copy = list(message_log)

        self._send_json(logs_copy)

    def _serve_index(self):
        body = (
            b"<h2>TCP Server Monitor</h2>"
            b"<p><a href='/stats'>GET /stats</a> &mdash; Statistikat JSON</p>"
            b"<p><a href='/logs'>GET /logs</a> &mdash; Te gjitha mesazhet</p>"
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, data: dict | list) -> None:
        try:
            body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {e}".encode())

    def log_message(self, fmt, *args):
        log.debug(f"[HTTP] {fmt % args}")


def start_http_monitor() -> None:
    with socketserver.ThreadingTCPServer((SERVER_IP, HTTP_PORT), MonitorHandler) as httpd:
        httpd.allow_reuse_address = True
        log.info(f"[HTTP] Monitor aktiv → http://localhost:{HTTP_PORT}/stats")
        log.info(f"[HTTP] Logs aktiv   → http://localhost:{HTTP_PORT}/logs")
        httpd.serve_forever()