import os
import threading

from config import SERVER_FILES_DIR, DEMO_FILES
from core.server import start_tcp_server
from utils.logger import log





if __name__ == "__main__":
    http_thread = threading.Thread()
    http_thread.start()
    start_tcp_server()
