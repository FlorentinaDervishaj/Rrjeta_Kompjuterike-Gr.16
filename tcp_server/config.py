# ── Rrjeti ───────────────────────────────────────────────────────────────────
SERVER_IP   = "0.0.0.0"
SERVER_PORT = 9999
HTTP_PORT   = 8080
MAX_CLIENTS = 4

# ── Sjellja e serverit ────────────────────────────────────────────────────────
TIMEOUT_SEC = 60
BUFFER_SIZE = 4096

# ── Skedarë ───────────────────────────────────────────────────────────────────
SERVER_FILES_DIR = "./server_files"
LOGS_DIR         = "./logs"

# ── Skedarë demo ─────────────────
DEMO_FILES = {
    "readme.txt": "Mirë se erdhe në server!\nKy është skedari readme.\n",
    "info.txt":   "Grupi 16 — Rrjetat Kompjuterike\nServeri TCP me privilegje\n",
    "data.csv":   "id,emri,vlera\n1,Alice,100\n2,Bob,200\n3,Carol,150\n",
}

# ── Privilegjet ───────────────────────────────────────────────────────────────
# Formati: { "emri_klientit": "admin" | "read" }
PRIVILEGES = {
    "client2": "read-only",
    "client3": "read-only",
    "client4": "read-only",
}

# ── Admin dinamik ─────────────────────────────────────────────────
# Klienti mund të bëhet admin gjatë sesionit duke dërguar /admin <password>
ADMIN_PASSWORD  = "admin123"
RECONNECT_WAIT  = 5  