import socket
HOST = "127.0.0.1"
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
    print(f"[+] U lidh me serverin {HOST}:{PORT}")
except Exception as e:
    print("Gabim gjate lidhjes:", e)
    exit()
name = input("Emri yt: ").strip()
if not name:
    name = "guest"
client.send(f"NAME:{name}\n".encode())
client.settimeout(1.0)
try:
    while True:
        chunk = client.recv(4096).decode("utf-8", errors="replace")
        if not chunk:
            break
        print(chunk, end="", flush=True)
except:
    pass
client.settimeout(None)
print()
print("Shkruaj /whoami per te pare privilegjin tend.")
print("Shkruaj /admin admin123 per privilegje te plota.")
print("Shkruaj /help per te gjitha komandat.")
print("Shkruaj 'exit' per te dale.\n")
while True:
    message = input("Ti: ")

    if message.lower() == "exit":
        break
    try:
        client.send((message + "\n").encode())
    except:
        print("Lidhja u nderprë.")
        break
    try:
        response = client.recv(4096).decode("utf-8", errors="replace")
        print("Serveri:", response)
    except:
        print("Lidhja u nderprë.")
        break

client.close()
print("U shkepute nga serveri.")