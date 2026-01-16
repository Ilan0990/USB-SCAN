# Bibliothèque standard pour gérer une base données locale
import sqlite3 
conn = sqlite3.connect("usb_analysis.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    prenom TEXT,
    poste TEXT,
    reponse TEXT,
    date_heure TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS usb_devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    manufacturer TEXT,
    device_id TEXT,
    description TEXT,
    detected_at TEXT,
    FOREIGN KEY (user_id) REFERENCES utilisateurs(id)
)
""")

conn.commit()

# Biblothèque standard pour rajouter la date et l'heure 
from datetime import datetime

# Biblothèque pour connaître toutes les informations d'un système sous Windows
import wmi 
def get_usb_devices():
    usb_devices = []
    c = wmi.WMI() # Crée un objet WMI qui va permettre de récupérer des informations sur les périphériques connectés à l'ordinateur
    for device in c.Win32_PnPEntity(): # Parcourt chacun des périphériques Plug and Play de l'ordinateur reconnu par Windows
        if device.PNPClass == "USB": # Filtre les péréphériques pour garder que les USB
            usb_devices.append({ 
                "name": device.Name,
                "manufacturer": device.Manufacturer,
                "device_id": device.DeviceID,
                "description": device.Description
            })
    return usb_devices # Renvoie la liste complète des périphériques USB détectés avec leur informations

# Liste pour stocker les réponses
reponses_utilisateur = []

# Crée une boucle
continu = True
while continu:

    # Demander le nom de l'utilisateur
    prenom = input("Quel est votre prénom ?")

    # Demander le prénom de l'utilisateur
    nom = input("Quel est votre nom ?")

    # Demande le numéro du poste
    poste = input ("Quelle est le numéro ton poste ?")

    # Afficher le message de bienvenue
    print(f"Bonjour, {prenom} {nom}, poste {poste} !")

    # Demander si l'utilisateur souhaite continuer
    reponse = input("Souhaitez-vous continuer ? (oui/non) ").strip().lower()

    date_heure = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    cursor.execute("""
    INSERT INTO utilisateurs (nom, prenom, poste, reponse, date_heure)
    VALUES (?, ?, ?, ?, ?)
    """, (nom, prenom, poste, reponse, date_heure))

    user_id = cursor.lastrowid # ID de l'utilisateur inséré

    for usb in get_usb_devices:
    cursor.execute("""
    INSERT INTO usb_devices 
    (user_id, name, manufacturer, device_id, description, detected_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        usb["name"],
        usb["manufacturer"],
        usb["device_id"],
        usb["description"],
        date_heure
    )) 
    conn.commit()


    

    # Stocker la réponse
    reponses_utilisateur.append({"nom": nom,"prenom": prenom,"reponse": reponse,"date": date_heure,"poste": poste})
    
    if reponse == "non":
        continu = False # Arrête la boucle
        print("Au revoir !")
conn.close        




    


