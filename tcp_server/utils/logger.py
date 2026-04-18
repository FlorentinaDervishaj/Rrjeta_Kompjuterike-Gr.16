import logging
import os
from config import LOGS_DIR

os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{LOGS_DIR}/server_logs.txt", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger("TCPServer")
