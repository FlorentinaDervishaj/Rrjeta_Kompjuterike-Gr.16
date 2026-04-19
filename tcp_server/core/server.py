import socket
import threading

from config import SERVER_IP, SERVER_PORT, MAX_CLIENTS
from core.state import server_state
from core.client_handler import handle_client
from utils.logger import log


def start_tcp_server() -> None:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((SERVER_IP, SERVER_PORT))
    server_sock.listen(MAX_CLIENTS)

    log.info(f"[SERVER] TCP aktiv → {SERVER_IP}:{SERVER_PORT}")
    log.info(f"[SERVER] Max klientë: {MAX_CLIENTS}")

    try:
        while True:
            conn, addr = server_sock.accept()
            with server_state["lock"]:
                active_count = len(server_state["active_clients"])

            if active_count >= MAX_CLIENTS:
                log.warning(f"[LIMIT] Lidhja refuzua nga {addr} — limit {MAX_CLIENTS} arritur")
                try:
                    conn.sendall("REJECTED Server i ngarkuar. Provo serish.\n".encode("utf-8"))
                except Exception:
                    pass
                conn.close()
                with server_state["lock"]:
                    server_state["rejected_connections"] += 1
                continue
            t = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True,
                name=f"client-{addr[0]}:{addr[1]}"
            )
            t.start()
            log.info(f"[ACCEPT] {addr[0]}:{addr[1]} → Thread: {t.name}")

    except KeyboardInterrupt:
        log.info("\n[SERVER] Ndërprerje nga tastiera. Mbyllje e serverit...")
    finally:
        server_sock.close()
        log.info("[SERVER] Socketi u mbyll.")

if __name__=="__main__":
    start_tcp_server()
