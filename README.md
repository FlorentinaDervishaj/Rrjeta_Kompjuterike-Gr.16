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


## HTTP Server

## Përshkrimi i pjesës së dytë

Kjo pjesë e projektit implementon një HTTP server të thjeshtë në Python, duke përdorur modulet `http.server` dhe `socketserver`.  
Qëllimi i tij është të ofrojë statistika në kohë reale për funksionimin e TCP serverit dhe të mundësojë monitorimin e sistemit përmes një endpoint-i të dedikuar.

Kjo pjesë demonstron konceptet kryesore si:

- komunikimi përmes protokollit HTTP  
- ndërtimi i një API-je bazike  
- bashkëpunimi ndërmjet serverit TCP dhe HTTP  
- përdorimi i multi-threading për ekzekutim paralel  

## Funksionalitetet kryesore

- Inicializimi i një HTTP serveri në Python  
- Implementimi i endpoint-it `/stats`  
- Kthimi i të dhënave në format JSON  
- Paraqitja e numrit të klientëve aktivë  
- Listimi i klientëve (IP, port, privilegje)  
- Numërimi i mesazheve të pranuara nga serveri TCP  
- Shfaqja e kohës aktuale të serverit  
- Menaxhimi i kërkesave të pavlefshme (404)  
- Përdorimi i threading për trajtim efikas të kërkesave  

## Teknologjitë e përdorura

- Python 3  
- `http.server`  
- `socketserver`  
- JSON  

## Ekzekutimi i projektit

Për të nisur serverin:

1. Hap terminalin në folderin e projektit  
2. Ekzekuto komandën:

```bash
python server.py
```

HTTP serveri do të jetë aktiv në:

IP: localhost
Port: 8080
Qasja në statistika

Statistikat mund të shihen duke hapur në browser:

http://localhost:8080/stats

## Funksionimi
HTTP serveri funksionon paralelisht me TCP serverin
Çdo kërkesë trajtohet në mënyrë të pavarur
-Endpoint /stats gjeneron një përgjigje në JSON
-Të dhënat merren nga strukturat globale (clients_active, total_messages)
-Përdoret lock për të siguruar integritetin e të dhënave gjatë ekzekutimit paralel

## Përfundim
Kjo pjesë e projektit ofron:
-monitorim në kohë reale të serverit
-pasqyrë të aktivitetit të klientëve
-integrim të dy protokolleve (TCP dhe HTTP) në një sistem të vetëm

## Autori
-Florentina Dervishaj – Implementimi i HTTP serverit për statistika
