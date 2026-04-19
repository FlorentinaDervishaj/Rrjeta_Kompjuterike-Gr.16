import time

from config import SERVER_IP, SERVER_PORT, HTTP_PORT, MAX_CLIENTS
from auth.privileges import get_privilege_by_addr, try_elevate_to_admin
from commands.file_commands import (
    cmd_list, cmd_read, cmd_upload,
    cmd_download, cmd_delete, cmd_search, cmd_info,
)
from core.state import server_state
from utils.logger import log

WELCOME_TEXT = (
    "=== Mire se vini ne server! ===\n"
    "Komandat e disponueshme:\n"
    "  /admin <fjalekalimi>      - Merr privilegje admin\n"
    "  /whoami                   - Shiko privilegjin tend\n"
    "  /list                     - Listo fajllat (admin)\n"
    "  /read <fajll>             - Lexo fajll (admin)\n"
    "  /upload <emer> <data>     - Ngarko fajll (admin)\n"
    "  /download <fajll>         - Shkarko fajll (admin)\n"
    "  /delete <fajll>           - Fshi fajll (admin)\n"
    "  /search <tekst>           - Kerko ne fajlla (admin)\n"
    "  /info <fajll>             - Metadatat e fajllit\n"
    "  /serverinfo               - Info rreth serverit\n"
    "  /quit                     - Mbyll lidhjen\n"
    "================================"
)

QUIT_SIGNAL = "__QUIT__"


def process_command(message: str, client_name: str, privilege: str, addr_str: str) -> str:
    if not message.startswith("/"):
        log.info(f"[{addr_str}] {message}")
        return "OK - mesazhi u pranua"

    parts = message.split(" ", 1)
    cmd   = parts[0].lower()
    arg   = parts[1].strip() if len(parts) > 1 else ""

    # ── /quit ─────────────────────────────────────────────────────────────────
    if cmd == "/quit":
        return QUIT_SIGNAL

    # ── /help ─────────────────────────────────────────────────────────────────
    if cmd == "/help":
        return WELCOME_TEXT

    # ── /whoami ───────────────────────────────────────────────────────────────
    if cmd == "/whoami":
        priv = get_privilege_by_addr(addr_str)
        return f"Privilegji yt: {priv}"

    # ── /admin <password> ─────────────────────────────────────────────────────
    if cmd == "/admin":
        if not arg:
            return "ERROR Sintaksa: /admin <fjalekalimi>"
        if try_elevate_to_admin(addr_str, arg):
            log.info(f"[ADMIN] {addr_str} mori privilegje admin.")
            return "Sukses! Tani ke privilegje ADMIN."
        return "Fjalekalimi i gabuar!"

    # ── /serverinfo ───────────────────────────────────────────────────────────
    if cmd == "/serverinfo":
        with server_state["lock"]:
            active = len(server_state["active_clients"])
            total  = server_state.setdefault("total_messages", 0)
        return (
            f"Server IP     : {SERVER_IP}, Port: {SERVER_PORT}\n"
            f"Klienti aktive: {active}/{MAX_CLIENTS}\n"
            f"Mesazhe totale: {total}\n"
            f"HTTP Stats    : http://localhost:{HTTP_PORT}/stats\n"
            f"HTTP Logs     : http://localhost:{HTTP_PORT}/logs"
        )

    # ── Komandat e skedareve ──────────────────────────────────────────────────
    file_commands = {
        "/list":     lambda: cmd_list(addr_str),
        "/read":     lambda: cmd_read(arg, addr_str),
        "/upload":   lambda: cmd_upload(arg, addr_str),
        "/download": lambda: cmd_download(arg, addr_str),
        "/delete":   lambda: cmd_delete(arg, addr_str),
        "/search":   lambda: cmd_search(arg, addr_str),
        "/info":     lambda: cmd_info(arg, addr_str),
    }

    if cmd in file_commands:
        return file_commands[cmd]()

    return f"ERROR Komanda e panjohur: '{cmd}'. Shkruaj /help per listen."
