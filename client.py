import socket

HOST = "127.0.0.1" 
PORT = 5000        

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    client.connect((HOST,PORT))
    print("U lidh me serverin!")
except Exception as e:
    print("Gabim gjatë lidhjes: ", e)
    exit()

print("Shkruaj mesazh (/read file.txt ose tekst)")
print("Shkruaj 'exit' për me dalë\n")


while True:
    message = input("Ti: ")

    if message.lower() == "exit":
        break

    try:
        client.send(message.encode())
        response = client.recv(1024).decode()

        print("Serveri: ", response)
    except:
        print("Lidhja me serverin u ndërpre.")
        break

client.close()
print("U shkëpute nga serveri.")