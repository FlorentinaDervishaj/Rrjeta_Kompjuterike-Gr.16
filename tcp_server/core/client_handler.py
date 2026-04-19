import socket
import time
from datetime import datetime

from config import TIMEOUT_SEC, BUFFER_SIZE, LOGS_DIR, SERVER_IP, SERVER_PORT, HTTP_PORT, MAX_CLIENTS
from core.state import server_state
from auth.privileges import get_privilege
from commands.processor import process_command, WELCOME_TEXT, QUIT_SIGNAL
from utils.logger import log

# ── message_log — lista globale e logut ──────────────────────────────────────
message_log: list = []


def save_message_to_log(addr_str: str, message: str) -> None:
    ip, port = addr_str.split(":", 1)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "ip":        ip,
        "port":      port,
        "message":   message,
        "timestamp": timestamp,
    }
    with server_state["lock"]:
        message_log.append(entry)
        server_state.setdefault("total_messages", 0)
        server_state["total_messages"] += 1

    log_path = f"{LOGS_DIR}/server_logs.txt"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {addr_str} -> {message}\n")
    except OSError as e:
        log.warning(f"[LOG] Nuk u ruajt log-u: {e}")


def _send(conn: socket.socket, message: str) -> None:
    try:
        conn.sendall((message + "\n").encode("utf-8"))
    except Exception as e:
        log.warning(f"Dergimi deshtoi: {e}")


def _do_handshake(conn: socket.socket) -> str:
    conn.settimeout(30)
    try:
        raw = conn.recv(BUFFER_SIZE)
        if not raw:
            return "guest"
        handshake = raw.decode("utf-8").strip()
        if handshake.startswith("NAME:"):
            name = handshake[5:].strip()
        else:
            name = handshake[:20].strip()
        return name if name else "guest"
    except Exception:
        return "guest"


def _register_client(addr_str: str, client_name: str, conn: socket.socket, privilege: str) -> None:
    ip, port = addr_str.split(":", 1)
    with server_state["lock"]:
        server_state["active_clients"][addr_str] = {
            "name":         client_name,
            "conn":         conn,
            "privilege":    privilege,
            "priv":         privilege,
            "ip":           ip,
            "port":         port,
            "messages":     [],
            "connected_at": datetime.now().isoformat(),
            "last_seen":    time.time(),
        }
        server_state["total_connections"] += 1


def _unregister_client(addr_str: str) -> None:
    with server_state["lock"]:
        server_state["active_clients"].pop(addr_str, None)


# ── Funksioni kryesor i thread-it ─────────────────────────────────────────────
def handle_client(conn: socket.socket, addr: tuple) -> None:
    client_name = "i_panjohur"
    addr_str    = f"{addr[0]}:{addr[1]}"

    try:
        # ── 1. Handshake ──────────────────────────────────────────────────────
        client_name = _do_handshake(conn)
        privilege   = get_privilege(client_name)

        # ── 2. Regjistrim ─────────────────────────────────────────────────────
        _register_client(addr_str, client_name, conn, privilege)
        log.info(f"[+] Klienti u lidh: {client_name} @ {addr_str} [{privilege}]")

        # ── 3. Welcome message ────────────────────────────────────────────────
        _send(conn, WELCOME_TEXT)
        _send(conn, f"Privilegji yt: {privilege}")

        # ── Timeout dinamik: admin -> 2x kohe ─────────────────────────────────
        timeout = TIMEOUT_SEC * 2 if privilege == "admin" else TIMEOUT_SEC
        conn.settimeout(timeout)

        # ── 4. Loop kryesor ───────────────────────────────────────────────────
        while True:
            try:
                data = conn.recv(BUFFER_SIZE)
            except socket.timeout:
                log.warning(f"[TIMEOUT] {client_name} @ {addr_str} — pasivitet {timeout}s")
                _send(conn, "TIMEOUT: Lidhja u mbyll per mosaktivitet.")
                break

            if not data:
                log.info(f"[-] {client_name} u shkepute (lidhja mbyllur nga klienti)")
                break

            text = data.decode("utf-8", errors="replace").strip()

            # ── 5. Ruaj çdo mesazh ne log ─────────────────────────────────────
            save_message_to_log(addr_str, text)

            # RREGULLIM: Merr privilegjin e fundit dinamikisht
            # (ne rast qe klienti ka bere /admin gjate sesionit)
            with server_state["lock"]:
                client_info = server_state["active_clients"].get(addr_str, {})
                current_privilege = client_info.get("privilege", privilege)

            response = process_command(text, client_name, current_privilege, addr_str)

            # ── /quit ─────────────────────────────────────────────────────────
            if response == QUIT_SIGNAL:
                _send(conn, "Lidhja u mbyll. Mirupafshim!")
                log.info(f"[QUIT] {client_name} @ {addr_str} kerkoi mbyllje.")
                break

            _send(conn, response)

    except ConnectionResetError:
        log.warning(f"[!] {client_name} shkeputi pa paralajmerim (ConnectionReset)")
    except Exception as e:
        log.error(f"[ERROR] Gabim me {client_name}: {e}")
    finally:
        # ── 7. Cleanup ────────────────────────────────────────────────────────
        _unregister_client(addr_str)
        conn.close()
        log.info(f"[~] Lidhja u mbyll: {client_name} @ {addr_str}")