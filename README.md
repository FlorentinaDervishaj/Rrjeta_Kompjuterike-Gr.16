# Rrjeta_Kompjuterike-Gr.16

# TCP Server
##  Përshkrimi pjesës parë
Kjo pjesë e projektit përfaqëson një server të thjeshtë TCP i ndërtuar në Python duke përdorur socket dhe threading. Serveri lejon lidhjen e disa klientëve në të njëjtën kohë dhe menaxhon komunikimin mes tyre.

Qëllimi kësaj pjese është të demonstrojë konceptet bazë të rrjeteve kompjuterike si:
- komunikimi client-server
- përdorimi i TCP socket
- menaxhimi i shumë klientëve njëkohësisht (multi-threading)

##  Funksionalitetet e implementuara
- Krijimi i serverit TCP me Python
- Vendosja e IP adresës dhe portit
- Pranimi i lidhjeve nga klientët
- Menaxhimi i klientëve me threading
- Limitimi i numrit të klientëve aktiv (MAX CLIENTS = 4)
- Refuzimi i klientëve kur serveri është i mbingarkuar
- Timeout për klientët jo-aktiv (60 sekonda)
- Dërgimi i përgjigjes për çdo mesazh të pranuar
- Menaxhimi i listës së klientëve aktiv

##  Teknologjitë e përdorura
- Python 3
- Socket Programming (TCP)
- Threading

##  Si të ekzekutohet projekti
1. Hap terminalin në folderin e projektit
2. Ekzekuto serverin me komandën:
   python server.py

Serveri do të fillojë të dëgjojë klientët në:
IP: 0.0.0.0  
Port: 5000

##  Lidhja e klientëve
Klientët mund të lidhen në server duke përdorur IP-në e serverit dhe portin 5000.

Shembull:
IP: <IP e serverit>  
Port: 5000

##  Funksionimi i serverit
- Çdo klient trajtohet në një thread të veçantë
- Serveri pranon deri në 4 klientë njëkohësisht
- Nëse limiti tejkalohet, lidhja refuzohet
- Nëse klienti nuk dërgon mesazh për 60 sekonda, ai shkëputet automatikisht

##  Autori
- Fiona Grabovci – Implementimi i serverit TCP (socket + threading + menaxhimi i klientëve)
