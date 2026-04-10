import socket
import threading

# =========================
# KONFIGURIMI I SERVERIT
# =========================
HOST = "0.0.0.0"   # Serveri dëgjon në të gjitha IP-të e rrjetit
PORT = 5000        # Porta e serverit (mund të ndryshohet sipas nevojës)
MAX_CLIENTS = 4    # Numri maksimal i klientëve të lejuar

# Lista për menaxhimin e klientëve aktivë
clients = []

# =========================
# MENAXHIMI I KLIENTIT
# =========================
def handle_client(conn, addr):
    """
    Funksion që trajton secilin klient në thread të veçantë
    """

    print(f"[LIDHJE] Klienti {addr} u lidh me serverin.")

    # Timeout: nëse klienti nuk dërgon mesazh për 60 sekonda, shkëputet
    conn.settimeout(60)

    try:
        while True:
            data = conn.recv(1024)

            # Nëse nuk ka të dhëna → klienti u shkëput
            if not data:
                break

            message = data.decode()

            print(f"[{addr}] {message}")

            # Përgjigje për klientin
            conn.send("OK - mesazhi u pranua".encode())

    except socket.timeout:
        print(f"[TIMEOUT] Klienti {addr} nuk dërgoi mesazh për 60 sekonda.")

    except Exception as e:
        print(f"[ERROR] Klienti {addr}: {e}")

    finally:
        # Mbyll lidhjen dhe hiq klientin nga lista
        print(f"[SHKYQJE] Klienti {addr} u shkëput.")
        conn.close()

        if conn in clients:
            clients.remove(conn)

# =========================
# KRIJIMI I SERVERIT TCP
# =========================
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("===================================")
print(f"Serveri është aktiv në {HOST}:{PORT}")
print(f"Max klientë të lejuar: {MAX_CLIENTS}")
print("Në pritje të klientëve...")
print("===================================")

# =========================
# PRANIMI I KLIENTËVE
# =========================
while True:
    conn, addr = server.accept()

    # Kontrollo limitin e klientëve
    if len(clients) >= MAX_CLIENTS:
        conn.send("Serveri është i mbingarkuar. Provoni më vonë.".encode())
        conn.close()
        continue

    # Shto klientin në listë aktive
    clients.append(conn)

    print(f"[AKTIV] Klientë të lidhur: {len(clients)}/{MAX_CLIENTS}")

    # Krijo thread për klientin
    thread = threading.Thread(
        target=handle_client,
        args=(conn, addr),
        daemon=True
    )
    thread.start()
