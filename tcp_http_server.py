import socket 
import threading
import http.server
import socketserver
import json
import time

HOST = "0.0.0.0"
PORT = 5000
HTTP_PORT = 8080
MAX_CLIENTS = 4

clients_active = {}   
total_messages = 0
lock = threading.Lock()


def handle_client(conn,addr):
    global total_messages
    print(f"[LIDHJE] Klienti {addr} u lidh.")
    conn.settimeout(60)
    try:
        while True:
            data =conn.recv(1024)
            if not data:
                break
            message =data.decode()
            print(f"[{addr}] {message}")



            with lock:
              total_messages += 1

            conn.send("OK - mesazhi u pranua".encode())

    except socket.timeout:
        print(f"[TIMEOUT] Klienti {addr} u shkëput (timeout).")
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        print(f"[SHKYQJE] Klienti {addr} u largua.")
        conn.close()
        with lock:
            if addr in clients_active:      
                del clients_active[addr]

class StatsHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/stats":
            try:
                with lock:
                    stats = {
                        "active_clients": len(clients_active),
                        "clients": [
                            {
                                "ip": info["ip"],
                                "port": info["port"],
                                "privilege": info["priv"]
                            }
                            for info in clients_active.values()
                        ],
                        "total_messages": total_messages,
                        "timestamp": time.ctime()
                    }
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(stats, indent=2).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 - Vetem /stats funksionon!")
    
    def log_message(self, format, *args):
        return

def start_http_server():
     with socketserver.ThreadingTCPServer(("", HTTP_PORT), StatsHandler) as httpd:
        print(f"HTTP Server aktiv ne portin {HTTP_PORT}")
        print(f"Testo: http://localhost:{HTTP_PORT}/stats")
        httpd.serve_forever()

def start_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("===================================")
    print(f"TCP Server aktiv ne {HOST}:{PORT}")
    print(f"Max klientë: {MAX_CLIENTS}")
    print("===================================")

    while True:
        conn, addr = server.accept()
        with lock:
            if len(clients_active) >= MAX_CLIENTS:
                conn.send("Serveri i mbingarkuar!".encode())
                conn.close()
                continue
            
           
            clients_active[addr] = {         
                "ip": addr[0],
                "port": addr[1],
                "priv": "read-only"
            }
        
        print(f"[AKTIV] Klientë: {len(clients_active)}/{MAX_CLIENTS}")
        
        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    print("Personi 3 (HTTP Stats) gati!")
    start_tcp_server()

