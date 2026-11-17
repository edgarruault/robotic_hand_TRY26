import tkinter as tk
from tkinter import ttk, messagebox
import serial
from serial.tools import list_ports

fenetre = tk.Tk()
fenetre.title("Quatre servos — clavier AZERTY")
fenetre.geometry("620x440")
liaison = None
pret = False
touches = set()
relachements = {}
colonnes = [('r', 'f'), ('g', 't'), ('y', 'h'), ('u', 'j')]
reception = bytearray()

ttk.Label(fenetre, text="Choisis le port USB de la Uno :").pack(pady=8)
port = ttk.Combobox(fenetre, width=48, state="readonly")
port.pack()

def actualiser():
    ports = [p.device for p in list_ports.comports()]
    port['values'] = ports
    if ports:
        port.set(next((p for p in ports if 'usb' in p.lower()), ports[0]))

def deconnecter():
    global liaison, pret
    pret = False
    touches.clear()
    if liaison:
        try:
            liaison.write(b'1111\n')
        except serial.SerialException:
            pass
        liaison.close()
        liaison = None
    etat.set("Deconnecte")

def activer():
    global pret
    if liaison:
        touches.clear()
        pret = True
        etat.set("Connecte — clique ici puis utilise les touches")
        zone.focus_set()

def connecter():
    global liaison
    deconnecter()
    try:
        liaison = serial.Serial(port.get(), 9600, timeout=0, write_timeout=0.1)
        reception.clear()
        retour.set("Arduino : en attente de confirmation")
    except (serial.SerialException, ValueError) as erreur:
        messagebox.showerror("Connexion impossible", str(erreur))
        return
    etat.set("Demarrage de l'Arduino... patiente 2 secondes")
    fenetre.after(2000, activer)

barre = ttk.Frame(fenetre)
barre.pack(pady=10)
ttk.Button(barre, text="Actualiser", command=actualiser).pack(side="left")
ttk.Button(barre, text="Connecter", command=connecter).pack(side="left")
ttk.Button(barre, text="Deconnecter", command=deconnecter).pack(side="left")

zone = tk.Label(fenetre, text="Maintiens une touche pour tourner :\n\n"
                "D3 : R / F      D5 : G / T\n"
                "D7 : Y / H      D9 : U / J\n\n"
                "Relache pour arreter — S : arret general",
                font=("Helvetica", 15), takefocus=True, pady=15)
zone.pack(fill="both", expand=True)
zone.bind('<Button-1>', lambda e: zone.focus_set())
etat = tk.StringVar(value="Deconnecte")
ttk.Label(fenetre, textvariable=etat).pack(pady=10)
envoi = tk.StringVar(value="Touches : aucune")
retour = tk.StringVar(value="Arduino : non confirme")
ttk.Label(fenetre, textvariable=envoi).pack()
ttk.Label(fenetre, textvariable=retour).pack(pady=8)

def lire_touche(event):
    cle = event.keysym.lower()
    return ',' if cle == 'comma' else cle

def appui(event):
    if not pret or fenetre.focus_get() is None:
        return
    cle = lire_touche(event)
    if cle in relachements:
        fenetre.after_cancel(relachements.pop(cle))
    if cle == 's':
        touches.clear()
    elif cle in ('r', 'f', 't', 'g', 'y', 'h', 'u', 'j'):
        touches.add(cle)

def relachement(event):
    cle = lire_touche(event)
    if cle in relachements:
        fenetre.after_cancel(relachements.pop(cle))
    def terminer():
        touches.discard(cle)
        relachements.pop(cle, None)
    # Filtre les faux relachements de la repetition clavier.
    relachements[cle] = fenetre.after(10, terminer)

def envoyer():
    if liaison and pret:
        if fenetre.focus_get() is None:
            touches.clear()
        valeurs = [str(1 + int(a in touches) - int(b in touches))
                   for a, b in colonnes]
        try:
            liaison.write((''.join(valeurs) + '\n').encode('ascii'))
            envoi.set("Touches : " + (', '.join(sorted(touches)) or 'aucune')
                      + " | Envoi : " + ''.join(valeurs))
            reception.extend(liaison.read(liaison.in_waiting))
            while b'\n' in reception:
                ligne, _, reste = reception.partition(b'\n')
                reception[:] = reste
                texte = ligne.decode('ascii', errors='replace').strip()
                if texte.startswith('OK:'):
                    retour.set("Arduino confirme : " + texte[3:])
                elif texte:
                    retour.set("Autre programme Arduino : " + texte[:60])
            if len(reception) > 1024:
                reception.clear()
        except serial.SerialException as erreur:
            deconnecter()
            etat.set("Connexion perdue : " + str(erreur))
    fenetre.after(50, envoyer)

def fermer():
    deconnecter()
    fenetre.destroy()

fenetre.bind('<KeyPress>', appui)
fenetre.bind('<KeyRelease>', relachement)
fenetre.protocol('WM_DELETE_WINDOW', fermer)
actualiser()
envoyer()
fenetre.mainloop()
