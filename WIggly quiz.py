import sqlite3
import random # Bibliothèque perméttant de générer des nombres aléatoires et de faire des choix au hasard

# Crée une base de donnée et établit une connexion
con = sqlite3.connect('words.db')
cur = con.cursor()  # Création d'un curseur pour exécuter des commandes SQL

# Création de la table
cur.execute('''
CREATE TABLE IF NOT EXISTS verbes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    infinitif TEXT NOT NULL,
    preterit TEXT NOT NULL,
    participe_passe TEXT NOT NULL,
    traduction_fr TEXT NOT NULL
)
''')
     
# Données d'exemple
verbes_data = [
    ('be', 'was/were', 'been', 'être'),
    ('have', 'had', 'had', 'avoir'),
    ('do', 'did', 'done', 'faire'),
    ('go', 'went', 'gone', 'aller'),
    ('see', 'saw', 'seen', 'voir'),
    ('come', 'came', 'come', 'venir'),
    ('take', 'took', 'taken', 'prendre'),
    ('get', 'got', 'got/gotten', 'obtenir'),
    ('make', 'made', 'made', 'faire/fabriquer'),
    ('know', 'knew', 'known', 'savoir/connaître'),
]

# Exécute la même requête SQL plusieurs fois avec des données différentes à chaque fois.
cur.executemany('''
INSERT INTO verbes (infinitif, preterit, participe_passe, traduction_fr)
VALUES (?, ?, ?, ?)
''', verbes_data)

# Sauvegarde des changements
con.commit()
con.close()

def obtenir_tous_les_verbes():
    """Récupère tous les verbes de la base de données"""
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM verbes') # Exécute une requête SQL pour récupérer toutes les données de la table
    verbes = cursor.fetchall() # Récupère tous les résultats de la requête SQL précédente et les stockes
    conn.close()
    return verbes

def quiz_complet():
    """Quiz complet (traduction + prétérit + participe passé)"""
    verbes = obtenir_tous_les_verbes()
    
    if not verbes:
        print("Aucun verbe dans la base de données!")
        return
    
    score = 0
    total = 0
    
    print("\n=== Wiggly quiz ===")
    print("Tapez 'quit' pour arrêter\n")
    
    random.shuffle(verbes) # Permet de mélanger aléatoirement les verbes
    
    for verbe in verbes:
        id_verbe, infinitif, preterit, participe_passe, traduction = verbe
        
        print(f"\n--- Verbe : {infinitif} ---")
        
        # Question 1 : Traduction
        reponse_trad = input(f"Traduction française de '{infinitif}' : ").strip().lower()
        if reponse_trad == 'quit':
            break
        
        # Question 2 : Prétérit
        reponse_preterit = input(f"Prétérit de '{infinitif}' : ").strip().lower()
        if reponse_preterit == 'quit':
            break
        
        # Question 3 : Participe passé
        reponse_pp = input(f"Participe passé de '{infinitif}' : ").strip().lower()
        if reponse_pp == 'quit':
            break
        
        # Vérification des réponses
        points_gagnes = 0
        
        if reponse_trad == traduction.lower():
            print("✓ Traduction correcte!")
            points_gagnes += 1
        else:
            print(f"✗ Traduction incorrecte. Bonne réponse : {traduction}")
        
        if reponse_preterit == preterit.lower():
            print("✓ Prétérit correct!")
            points_gagnes += 1
        else:
            print(f"✗ Prétérit incorrect. Bonne réponse : {preterit}")
        
        if reponse_pp == participe_passe.lower():
            print("✓ Participe passé correct!")
            points_gagnes += 1
        else:
            print(f"✗ Participe passé incorrect. Bonne réponse : {participe_passe}")
        
        score += points_gagnes
        total += 3
        
        print(f"\nScore pour ce verbe : {points_gagnes}/3")
        print(f"Score total : {score}/{total}")
    
    print("\n" + "="*50)
    print(f"QUIZ TERMINÉ!")
    print(f"Score final : {score}/{total}")
    if total > 0:
        pourcentage = (score / total) * 100
        print(f"Pourcentage de réussite : {pourcentage:.1f}%")
    print("="*50)

def quiz_traduction():
    """Quiz uniquement sur les traductions"""
    verbes = obtenir_tous_les_verbes()
    random.shuffle(verbes)
    
    score = 0
    print("\n=== QUIZ TRADUCTION ===\n")
    
    for verbe in verbes:
        infinitif, traduction = verbe[1], verbe[4]
        reponse = input(f"Traduction de '{infinitif}' : ").strip().lower()
        
        if reponse == 'quit':
            break
        
        if reponse == traduction.lower():
            print("✓ Correct!\n")
            score += 1
        else:
            print(f"✗ Incorrect. Bonne réponse : {traduction}\n")
    
    print(f"Score final : {score}/{len(verbes)}")

def quiz_conjugaison():
    """Quiz uniquement sur prétérit et participe passé"""
    verbes = obtenir_tous_les_verbes()
    random.shuffle(verbes)
    
    score = 0
    total = 0
    print("\n=== QUIZ CONJUGAISON ===\n")
    
    for verbe in verbes:
        infinitif, preterit, participe_passe = verbe[1], verbe[2], verbe[3]
        
        print(f"Verbe : {infinitif}")
        rep_pret = input("Prétérit : ").strip().lower()
        if rep_pret == 'quit':
            break
        
        rep_pp = input("Participe passé : ").strip().lower()
        if rep_pp == 'quit':
            break
        
        if rep_pret == preterit.lower():
            print("✓ Prétérit correct!")
            score += 1
        else:
            print(f"✗ Bonne réponse : {preterit}")
        
        if rep_pp == participe_passe.lower():
            print("✓ Participe passé correct!")
            score += 1
        else:
            print(f"✗ Bonne réponse : {participe_passe}")
        
        total += 2
        print()
    
    print(f"Score final : {score}/{total}")

def menu_quiz():
    """Menu principal"""
    print("\n=== MENU QUIZ ===")
    print("1. Quiz complet")
    print("2. Quiz traduction")
    print("3. Quiz conjugaison")
    print("4. Quitter")
    
    choix = input("\nVotre choix (1-4) : ")
    
    if choix == '1':
        quiz_complet()
        menu_quiz()  # Retour au menu
    elif choix == '2':
        quiz_traduction()
        menu_quiz()  # Retour au menu
    elif choix == '3':
        quiz_conjugaison()
        menu_quiz()  # Retour au menu
    elif choix == '4':
        print("Au revoir!")
    else:
        print("Choix invalide")
        menu_quiz()

if __name__ == "__main__":
    menu_quiz()