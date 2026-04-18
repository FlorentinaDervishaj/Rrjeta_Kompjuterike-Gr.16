import socket


# =========================
# KONFIGURIMI I SERVERIT
# =========================
HOST = "127.0.0.1" # IP e serverit
PORT = 5000        # Porta e serverit

# =========================
# LIDHJA ME SERVER
# =========================
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST,PORT))
    print("U lidh me serverin!")
except Exception as e:
    print("Gabim gjatë lidhjes: ", e)
    exit()

print("Shkruaj mesazh (/read file.txt ose tekst)")
print("Shkruaj 'exit' për me dalë\n")

# =========================
# KOMUNIKIMI
# =========================
while True:
    message = input("Ti: ")

    if message.lower() == "exit":
        break

    try:
        #dërgo mesazhin te serveri
        client.send(message.encode())

        #Merr përgjigjen nga serveri
        response = client.recv(1024).decode()

        print("Serveri: ", response)

    except:
        print("Lidhja me serverin u ndërpre.")
        break

# =========================
# MBYLLJA
# =========================
client.close()
print("U shkëpute nga serveri.")