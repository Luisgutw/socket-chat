#Luis Gutwein
import socket
import threading
import tkinter as tk
import time

#Variable zum Speichern des Usernames
username =""

#Boolean zum Überprüfen, ob Nachricht selbst gesendet wurde
#Wichtig für die Hintergrundfarbe
gesendet = True


#Socket erstellen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Methode zum Empfangen der Nachrichten
def receive():
    global gesendet
    while True:
        data = s.recv(1024)
        data = data.decode("utf8")
        if not data:
            break
        #Nachricht in neuer Zeile zur Listbox hinzufügen
        liste.insert(tk.END, data)
        #Hintergrundfarbe der Nachrichten
        if gesendet:
            liste.itemconfig(tk.END, {'bg' : 'lightgreen'})
        else:
            gesendet = True
        #automatisch nach unten scrollen
        liste.yview(tk.END)

#Methode zum Senden
def sende():
    global gesendet
    msg = message.get()
    #Überprüfen ob ein Text eingegeben wurde
    if not msg:
        return
    #Input Feld wird geleert
    message.set("")
    #Username vor die Nachricht schreiben
    nachricht = username + ": "
    nachricht += msg
    #Uhrzeit vor die Nachricht schreiben
    uhrzeit = time.strftime('%H:%M:%S ')
    uhrzeit += nachricht
    #gesamte Nachricht encodieren und versenden
    uhrzeit = uhrzeit.encode("utf-8")
    s.send(uhrzeit)
    #Boolean setzen, um zu erkennen, ob man selbst gesendet hat
    gesendet = False
    #beenden beim schließen des Fensters
    if msg == "{Hat den Server verlassen}":
        root.destroy()
        quit()
        
#Methode zum Beenden des Sockets        
def beenden():
    message.set("{Hat den Server verlassen}")
    sende()
    
#Anfangsmethode für den Username    
def name():
    global username
    username = message.get()
    if username:
        #Überprüfen der Länge des Usernames
        if len(username) < 11:
            message.set("")
            onlineText = username + " ist jetzt online"
            onlineText = onlineText.encode("utf-8")
            s.send(onlineText)
            sendenButton()
        else:
            liste.insert(tk.END,"Username ist zu lang. Maximal 10 Zeichen.")
            liste.itemconfig(tk.END, {'bg' : 'salmon'})
        
#neuer Button wird zum Senden erzeugt    
def sendenButton():
    senden_button.destroy()
    send_button = tk.Button(master = senden_frame, text="Senden", command=sende)
    send_button.pack(side = 'left')
 
#Methode für die digitale Uhr 
def uhrzeit_anzeigen():
    aktuelle_zeit = time.strftime('%H:%M:%S:%p')
    uhrzeit_label['text'] = aktuelle_zeit
    #Nach 400 Milisekunden wird die Funktion erneut aufgerufen
    uhrzeit_label.after(400, uhrzeit_anzeigen)


#GUI Fenster mit Tkinter erstellen
root = tk.Tk()
root.title("Socket Messenger")
root.geometry('800x650')
root.configure(bg='palegreen')

#Frame für Listbox
messages_frame = tk.Frame(root)
#Frame für Entry und Button
senden_frame = tk.Frame(root)

#Variable für Eingabefeld
message = tk.StringVar()
message.set("")

#Scrollbar erzeugen
scrollbar = tk.Scrollbar(messages_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Listbox erstellen und zum fenster hinzufügen
liste= tk.Listbox(messages_frame, height=30, width=90, yscrollcommand=scrollbar.set)
liste.pack(side=tk.LEFT, fill=tk.BOTH)

#Label für die Uhrzeit erstellen
uhrzeit_label = tk.Label(root, font= 'ariel 15', bg ='palegreen')
uhrzeit_label.pack()

#Label für die Überschrift
caption_label =tk.Label(root, font = 'ariel 30', bg='palegreen', fg ='deepskyblue')
caption_label['text'] = 'Socket Messenger'
caption_label.pack()


private_label = tk.Label(root, bg='palegreen')
private_label['text'] = 'Created by Luis Gutwein'
private_label.place(relx = 0.09, rely =0.98, anchor='center')

messages_frame.pack()
senden_frame.pack()

#Eingabefeld erzeugen
entry_field = tk.Entry(master = senden_frame, textvariable=message, width = 40)
entry_field.pack(side = 'left')

#Button zur Eingabe des Usernames
senden_button = tk.Button(master = senden_frame, text="akzeptieren", command=name)
senden_button.pack(side = 'left')



#Ausführen der Methode beenden, wenn Fenster geschlossen wird
root.protocol("WM_DELETE_WINDOW", beenden)


#Festlegung des Hosts und des Ports für socket
Host = '127.0.0.1'
Port = 50010
Adresse = (Host, Port)

#Verbindung aufbauen
s.connect(Adresse)

#Methode um die Uhrzeit aufzurufen
uhrzeit_anzeigen()

#Erzeugen des Threads zum gleichzeitgen Ausführen von Senden und Empfangen
cThread = threading.Thread(target=receive)
cThread.daemon = True
cThread.start()
#Endlos Schleife für Tkinter aktivieren
tk.mainloop() 