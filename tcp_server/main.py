import os
import threading

from config import SERVER_FILES_DIR, DEMO_FILES
from core.server import start_tcp_server
from monitor.http_server import start_http_monitor
from utils.logger import log


def _create_demo_files() -> None:
    os.makedirs(SERVER_FILES_DIR, exist_ok=True)
    for filename, content in DEMO_FILES.items():
        path = os.path.join(SERVER_FILES_DIR, filename)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            log.info(f"[INIT] Skedari demo u krijua: {filename}")


if __name__ == "__main__":
    _create_demo_files()
    http_thread = threading.Thread(target=start_http_monitor, daemon=True, name="http-monitor")
    http_thread.start()
    start_tcp_server()
