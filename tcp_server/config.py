# ── Rrjeti ───────────────────────────────────────────────────────────────────
SERVER_IP   = "0.0.0.0"   # Dëgjon në të gjitha interfejset
SERVER_PORT = 9999         # Porti kryesor TCP
HTTP_PORT   = 8080         # Porti i HTTP monitorit
MAX_CLIENTS = 4            # Numri i anëtarëve të grupit

# ── Sjellja e serverit ────────────────────────────────────────────────────────
TIMEOUT_SEC = 60           # Sekonda pa aktivitet → lidhja mbyllet
BUFFER_SIZE = 4096         # Bytes të lexuara nga socketi çdo herë

# ── Skedarë ───────────────────────────────────────────────────────────────────
SERVER_FILES_DIR = "./server_files"   # Folder-i i aksesueshem nga klientet
LOGS_DIR         = "./logs"

# ── Skedarë demo (krijohen automatikisht nëse nuk ekzistojnë) ─────────────────
DEMO_FILES = {
    "readme.txt": "Mirë se erdhe në server!\nKy është skedari readme.\n",
    "info.txt":   "Grupi 16 — Rrjetat Kompjuterike\nServeri TCP me privilegje\n",
    "data.csv":   "id,emri,vlera\n1,Alice,100\n2,Bob,200\n3,Carol,150\n",
}

# ── Privilegjet ───────────────────────────────────────────────────────────────
# Formati: { "emri_klientit": "admin" | "read" }
PRIVILEGES = {
    "admin":   "admin",
    "client2": "read",
    "client3": "read",
    "client4": "read",
}

# Klienti mund të bëhet admin gjatë sesionit duke dërguar /admin <password>
ADMIN_PASSWORD  = "admin123"
RECONNECT_WAIT  = 5       # sekonda pritje para rikonektimit automatik