# Rrjeta_Kompjuterike-Gr.16

##  Përshkrimi i Projektit
Ky projekt paraqet implementimin e një sistemi të shpërndarë client-server në gjuhën Python, duke kombinuar komunikimin përmes TCP socket-eve me një HTTP server për monitorim në kohë reale.

##  Qëllimi i Projektit
Demonstrimi praktik i koncepteve kryesore të rrjeteve kompjuterike:
-	Komunikimi client-server
-	Menaxhimi i shumë klientëve njëkohësisht
-	Kontrolli i qasjes (privilegjet)
-	Monitorimi i aktivitetit të serverit

##  Arkitektura e Sistemit
🔹 TCP Server
TCP Server-i është komponenti kryesor që menaxhon komunikimin me klientët.
Funksionalitetet:
-	Dëgjimi në IP dhe port të konfiguruar
-	Pranimi i shumë klientëve (multi-threading)
-	Kufizimi i numrit të klientëve aktiv (max clients)
-	Timeout për klientët joaktiv
-	Ruajtja e mesazheve për monitorim
-	Menaxhimi i privilegjeve (admin / read-only)

🔹 HTTP Server (Monitoring)
HTTP Server-i funksionon paralelisht dhe mundëson monitorimin e sistemit.
Endpoint:
GET /stats
Kthen në JSON:
-	Numrin e klientëve aktiv
-	IP dhe portet e tyre
-	Numrin total të mesazheve
-	Kohën e serverit

🔹 TCP Client
Client-i mundëson komunikimin me serverin dhe ekzekutimin e komandave.
Funksionalitetet:
-	Lidhja me serverin (IP + port)
-	Dërgimi dhe pranimi i mesazheve
-	Ekzekutimi i komandave

Ndarja e roleve:
-	Admin client – qasje e plotë
-	User client – vetëm read


##  Teknologjitë e përdorura
Teknologjitë e Përdorura:
-	Python 3
-	socket (TCP)
-	threading
-	http.server
-	socketserver
-	JSON

##  Si të ekzekutohet projekti
1. Hap terminalin në folderin e projektit
2. Ekzekuto serverin me komandën:
   python server.py

Serveri
```bash
python tcp_server.py
```
python main.py
-	TCP Server: 0.0.0.0:5000
-	HTTP Server: http://localhost:8080/stats

Client-i
```bash
python client.py
```

##  Karakteristikat Kryesore
Karakteristikat Kryesore
-	Multi-threading dhe kontroll i ngarkesës
-	Role-based access control
-	Monitorim në kohë reale përmes HTTP
-	Integrim i TCP dhe HTTP


 ## Testimi
Ky projekt mund të testohet në një rrjet lokal (LAN) duke përdorur disa pajisje të lidhura në të njëjtin rrjet WiFi.

Testimi përfshin:
- Lidhjen e disa klientëve me serverin
- Dërgimin dhe pranimin e mesazheve
- Verifikimin e limitit të klientëve (maksimum 4)
- Testimin e timeout për klientët joaktiv

##  Autorët
-	Fiona Grabovci – TCP Server
-	Rinor Maliqi -TCP Server(Logjika)
-	Florentina Dervishaj – HTTP Server
-	Fjolla Jakupi – TCP Client
