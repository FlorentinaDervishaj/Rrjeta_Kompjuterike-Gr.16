import socket
import threading

# =========================
# KONFIGURIMI I SERVERIT
# =========================
HOST = "0.0.0.0"
PORT = 5000
MAX_CLIENTS = 4

clients = []
messages_log = []  # ruan mesazhet për monitorim

# =========================
# FUNKSIONI PËR SECILIN KLIENT
# =========================
def handle_client(conn, addr):
    print(f"[LIDHJE] {addr} u lidh")

    # nëse klienti nuk dërgon mesazh për 60 sekonda → mbyllet
    conn.settimeout(60)

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode()

            # ruaj mesazhin (kërkesë e profesoreshës - monitorim)
            messages_log.append((addr, message))

            print(f"[{addr}] {message}")

            conn.send("OK - mesazhi u pranua".encode())

        except socket.timeout:
            print(f"[TIMEOUT] {addr} nuk dërgoi mesazh")
            break
        except:
            break

    print(f"[SHKYQJE] {addr}")
    conn.close()

    if conn in clients:
        clients.remove(conn)

# =========================
# KRIJIMI I SERVERIT TCP
# =========================
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Serveri është aktiv...")
print("Në pritje të klientëve...")

# =========================
# PRANIMI I KLIENTËVE
# =========================
while True:
    conn, addr = server.accept()

    # limitimi i lidhjeve (MAX 4 klientë)
    if len(clients) >= MAX_CLIENTS:
        conn.send("Serveri është i mbingarkuar!".encode())
        conn.close()
        continue

    clients.append(conn)

    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
