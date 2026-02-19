import sqlite3
import random

# Crée une base de données et établit une connexion
con = sqlite3.connect('words.db')
cursor = con.cursor()  # Création d'un curseur pour exécuter des commandes SQL

# Création de la table
cursor.execute('''
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

# Insertion des données (seulement si la table est vide pour éviter les doublons)
cursor.execute('SELECT COUNT(*) FROM verbes') # Compte le nombre total de lignes dans la table verbes
if cursor.fetchone()[0] == 0: # Vérifie si le résultat de la requete précedente est égal à zéro
    cursor.executemany('''
    INSERT INTO verbes (infinitif, preterit, participe_passe, traduction_fr)
    VALUES (?, ?, ?, ?)
    ''', verbes_data)

# Sauvegarde des changements
con.commit()
con.close()


def tous_les_verbes():
    con = sqlite3.connect('words.db')
    cursor = con.cursor()
    cursor.execute('SELECT * FROM verbes')
    verbes = cursor.fetchall() # Récupére tous les résultats de la requetes SQL précédente et les stockes
    con.close()
    return verbes


def demander_nb_questions(max_questions):
    while True:
        reponse = input(f"Combien de questions veux-tu ? (1-{max_questions}, ou 'tout' pour toutes) : ").strip().lower()
        if reponse == 'tout':
            return max_questions
        if reponse.isdigit(): # Vérifie si la chaîne de caractères est composée uniquement de chiffres
            nb = int(reponse) # Converti une chaîne de caractères en nombre entier
            if 1 <= nb <= max_questions: # Vérifie que le nombre choisi est bien compris entre 1 et la variable max_questions 
                return nb
        print(f"Entrée invalide. Choisis un nombre entre 1 et {max_questions}.")


def quiz_complet():
    verbes = tous_les_verbes()

    if not verbes:
        print('Aucun verbe dans la base de données !')
        return

    score = 0
    total = 0

    print("QUIZ COMPLET")
    print("Taper 'quit' pour arrêter")

    random.shuffle(verbes) # Mélange aléatoirement la liste
    nb_questions = demander_nb_questions(len(verbes))
    verbes = verbes[:nb_questions] # Découpe la liste de verbes pour ne garder que les premiers mots de la liste mélangés

    for verbe in verbes:
        id, infinitif, preterit, participe_passe, traduction_fr = verbe # Décompose verbe en 5 variables séparées
        print("Verbe: ", infinitif)

        # Traduction
        traduction = input(f"Traduction française de '{infinitif}' : ").strip().lower()
        if traduction == 'quit':
            break

        # Prétérit
        rep_preterit = input(f"Prétérit de '{infinitif}' : ").strip().lower()
        if rep_preterit == 'quit':
            break

        # Participe passé
        rep_participe = input(f"Participe passé de '{infinitif}' : ").strip().lower()
        if rep_participe == 'quit':
            break

        points_gagnes = 0


        if traduction == traduction_fr.lower():
            print('Traduction correcte !')
            points_gagnes += 1
        else:
            print(f'Traduction incorrecte ! La bonne réponse est : {traduction_fr}')

        if rep_preterit == preterit.lower():
            print('Prétérit correct !')
            points_gagnes += 1
        else:
            print(f'Prétérit incorrect ! La bonne réponse est : {preterit}')

        if rep_participe == participe_passe.lower():
            print('Participe passé correct !')
            points_gagnes += 1
        else:
            print(f'Participe passé incorrect ! La bonne réponse est : {participe_passe}')

        total += 3
        score += points_gagnes

        print(f"Score pour ce verbe : {points_gagnes}/3")
        print(f"Score total : {score}/{total}")

    print("Fin du quiz !")
    print(f'Votre score final : {score}/{total}')
    if total > 0:
        pourcentage = score / total * 100
        print(f'Pourcentage de réussite : {pourcentage:.1f}%')
    print("=" * 50)


def quiz_traduction():
    verbes = tous_les_verbes()
    random.shuffle(verbes)

    score = 0
    total = 0
    print("Quiz traduction")

    nb_questions = demander_nb_questions(len(verbes))
    verbes = verbes[:nb_questions]

    for verbe in verbes:
        infinitif, traduction = verbe[1], verbe[4]
        reponse = input(f"Traduction française de '{infinitif}' : ").strip().lower()

        if reponse == 'quit':
            break

        total += 1

        if reponse == traduction.lower():
            print('Traduction correcte !')
            score += 1
        else:
            print(f'Traduction incorrecte ! La bonne réponse est : {traduction}')

    print(f"Votre score final : {score}/{total}")


def quiz_conjugaison():
    verbes = tous_les_verbes()
    random.shuffle(verbes)

    score = 0
    total = 0
    print("Quiz conjugaison")

    nb_questions = demander_nb_questions(len(verbes))
    verbes = verbes[:nb_questions]

    for verbe in verbes:

        infinitif, preterit, participe_passe = verbe[1], verbe[2], verbe[3]

        print(f"Infinitif : {infinitif}")

        rep_pret = input(f"Prétérit de '{infinitif}' : ").strip().lower()
        if rep_pret == 'quit':
            break

        rep_pp = input(f"Participe passé de '{infinitif}' : ").strip().lower()
        if rep_pp == 'quit':
            break


        if rep_pret == preterit.lower():
            print('Prétérit correct !')
            score += 1
        else:
            print(f'Prétérit incorrect ! La bonne réponse est : {preterit}')

        if rep_pp == participe_passe.lower():
            print('Participe passé correct !')
            score += 1
        else:
            print(f'Participe passé incorrect ! La bonne réponse est : {participe_passe}')

        total += 2
        print(f"Score pour ce verbe : {score}/{total}")

    print(f"Votre score final : {score}/{total}")


def menu_quiz():
    while True:
        print("\n" + "=" * 30)
        print("       MENU QUIZ")
        print("=" * 30)
        print("1. Quiz complet")
        print("2. Quiz traduction")
        print("3. Quiz conjugaison")
        print("4. Quitter")

        choix = input("Choisis un quiz (1-4) : ")

        if choix == '1':
            quiz_complet()
        elif choix == '2':
            quiz_traduction()
        elif choix == '3':
            quiz_conjugaison()
        elif choix == '4':
            print("Au revoir !")
            break
        else:
            print("Choix invalide !")


if __name__ == "__main__": 
    menu_quiz()





    

































