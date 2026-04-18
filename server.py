import socket
import threading

HOST = "0.0.0.0"   
PORT = 5000        
MAX_CLIENTS = 4    

clients = []

def handle_client(conn, addr):

    print(f"[LIDHJE] Klienti {addr} u lidh me serverin.")

    conn.settimeout(60)

    try:
        while True:
            data = conn.recv(1024)

            if not data:
                break

            message = data.decode()

            print(f"[{addr}] {message}")

            conn.send("OK - mesazhi u pranua".encode())

    except socket.timeout:
        print(f"[TIMEOUT] Klienti {addr} nuk dërgoi mesazh për 60 sekonda.")

    except Exception as e:
        print(f"[ERROR] Klienti {addr}: {e}")

    finally:
        print(f"[SHKYQJE] Klienti {addr} u shkëput.")
        conn.close()

        if conn in clients:
            clients.remove(conn)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("===================================")
print(f"Serveri është aktiv në {HOST}:{PORT}")
print(f"Max klientë të lejuar: {MAX_CLIENTS}")
print("Në pritje të klientëve...")
print("===================================")

while True:
    conn, addr = server.accept()

    if len(clients) >= MAX_CLIENTS:
        conn.send("Serveri është i mbingarkuar. Provoni më vonë.".encode())
        conn.close()
        continue

    clients.append(conn)

    print(f"[AKTIV] Klientë të lidhur: {len(clients)}/{MAX_CLIENTS}")

    thread = threading.Thread(
        target=handle_client,
        args=(conn, addr),
        daemon=True
    )
    thread.start()
