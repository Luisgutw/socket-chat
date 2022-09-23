#Luis Gutwein
import socket
import threading
import time

#Socket erstellen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Erzeugen des Sockets mit Adresse und Port
s.bind(('127.0.0.1', 50010))

#Warten auf eingegehende Verbindungsanfragen
s.listen(5)

#Liste mit allen Verbindungen
connections = []

#Handler Methode für die Clients
def handler(c, a):
    global connections
    while True:
        #Daten empfangen
        data = c.recv(1024)
        #Überprüfen, ob Client Server verlassen hat
        if ("{Hat den Server verlassen}").encode("utf-8") in data:
            connections.remove(c)
            c.close()
            for connection in connections:
                connection.send(data)
            break
        #Jedem Client die Nachricht senden
        for connection in connections:
            connection.send(data)

while True:
    #Akzeptieren der Anfragen
    c, a = s.accept()
    #Erstellen eines Threads für mehrere Clients gleichzeitig
    #Leitet zum Handler weiter
    cThread = threading.Thread(target = handler, args = (c, a))
    cThread.daemon = True
    cThread.start()
    #verbindung zur Liste hinzufügen
    connections.append(c)
    
    #Willkommensnachrichten auf Server
    welcome_one = "Willkommen auf dem Server"
    welcome_two = "Drücke auf Senden, um eine Nachricht zu versenden"
    welcome_three = "Wähle einen Username"
    
    welcome_one = welcome_one.encode("utf-8")
    welcome_two = welcome_two.encode("utf-8")
    welcome_three = welcome_three.encode("utf-8")
    
    c.send(welcome_one)
    time.sleep(0.1)
    c.send(welcome_two)
    time.sleep(0.1)
    c.send(welcome_three)
    
    #Ausgabe der Verbindungen auf Server (optional)
    print(connections)