import sqlite3
import random


class GestionnaireVerbes: # Définit une classe

    def __init__(self, nom_db='words.db'): # Permet d'initialiser un objet à chaque fois que l'on crée un objet dans la classe
        self.nom_db = nom_db # Crée un attribut et le stocke dans l'objet + Création variable
        self._initialiser_base() # Appelle la méthode

    def _initialiser_base(self): # Création de la méthode
        con = sqlite3.connect(self.nom_db) # Crée une base de données et établit une connexion
        cursor = con.cursor() # Création d'un curseur pour exécuter des commandes SQL

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
        if cursor.fetchone()[0] == 0: # Vérifie si le résultat de la requête précédente est égal à zéro
            cursor.executemany('''
            INSERT INTO verbes (infinitif, preterit, participe_passe, traduction_fr)
            VALUES (?, ?, ?, ?)
            ''', verbes_data)

        con.commit()
        con.close()
    
    def tous_les_mots(self):
        con = sqlite3.connect(self.nom_db)
        cursor = con.cursor()
        cursor.execute('SELECT * FROM verbes')
        verbes = cursor.fetchall() # Récupère tous les résultats de la requête SQL précédente et les stocke
        con.close()
        return verbes

    def ajouter_verbe(self, infinitif, preterit, participe_passe, traduction_fr):
        con = sqlite3.connect(self.nom_db)
        cursor = con.cursor()
        cursor.execute('''
        INSERT INTO verbes (infinitif, preterit, participe_passe, traduction_fr)
        VALUES (?, ?, ?, ?)
        ''', (infinitif, preterit, participe_passe, traduction_fr))
        con.commit()
        con.close()

    def supprimer_verbe(self, infinitif):
        con = sqlite3.connect(self.nom_db)
        cursor = con.cursor()
        cursor.execute('DELETE FROM verbes WHERE LOWER(infinitif) = ?', (infinitif.lower(),))
        nb_supprimes = cursor.rowcount # Vérifie combien de lignes ont été supprimées
        con.commit()
        con.close()
        return nb_supprimes > 0 # Vérifie que la valeur soit supérieure à 0


class Quiz:

    def __init__(self, gestionnaire):
        self.gestionnaire = gestionnaire

    def demander_nb_questions(self, max_questions):
        while True:
            reponse = input(
                f"Combien de questions veux-tu ? (1-{max_questions}, ou 'tout' pour toutes) : ").strip().lower()
            if reponse == 'tout':
                return max_questions
            if reponse.isdigit(): # Vérifie si la chaîne de caractères est composée uniquement de chiffres
                nb = int(reponse) # Converti une chaîne de caractères en nombre entier
                if 1 <= nb <= max_questions: # Vérifie que le nombre choisi est bien compris entre 1 et la variable max_questions
                    return nb
            print(f"Entrée invalide. Choisis un nombre entre 1 et {max_questions}.")

    def quiz_complet(self):
        verbes = self.gestionnaire.tous_les_verbes()

        if not verbes:
            print('Aucun verbe dans la base de données !')
            return

        score = 0
        total = 0

        print("\n" + "=" * 40)
        print("          QUIZ COMPLET")
        print("=" * 40)
        print("Taper 'quit' pour arrêter\n")

        random.shuffle(verbes) # Mélange aléatoirement la liste
        nb_questions = self.demander_nb_questions(len(verbes))
        verbes = verbes[:nb_questions] # Découpe la liste de verbes pour ne garder que les premiers mots de la liste mélangés2

        for verbe in verbes:
            id, infinitif, preterit, participe_passe, traduction_fr = verbe
            print(f"\nVerbe : {infinitif}")

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
                print('✓ Traduction correcte !')
                points_gagnes += 1
            else:
                print(f'✗ Traduction incorrecte ! La bonne réponse est : {traduction_fr}')

            if rep_preterit == preterit.lower():
                print('✓ Prétérit correct !')
                points_gagnes += 1
            else:
                print(f'✗ Prétérit incorrect ! La bonne réponse est : {preterit}')

            if rep_participe == participe_passe.lower():
                print('✓ Participe passé correct !')
                points_gagnes += 1
            else:
                print(f'✗ Participe passé incorrect ! La bonne réponse est : {participe_passe}')

            total += 3
            score += points_gagnes

            print(f"Score pour ce verbe : {points_gagnes}/3")
            print(f"Score total : {score}/{total}")

        self._afficher_score_final(score, total)

    def quiz_traduction(self):
        verbes = self.gestionnaire.tous_les_verbes()

        if not verbes:
            print('Aucun verbe dans la base de données !')
            return

        random.shuffle(verbes)

        score = 0
        total = 0

        print("\n" + "=" * 40)
        print("          QUIZ TRADUCTION")
        print("=" * 40)
        print("Taper 'quit' pour arrêter\n")

        nb_questions = self.demander_nb_questions(len(verbes))
        verbes = verbes[:nb_questions]

        for verbe in verbes:
            infinitif, traduction = verbe[1], verbe[4]
            reponse = input(f"Traduction française de '{infinitif}' : ").strip().lower()

            if reponse == 'quit':
                break

            total += 1

            if reponse == traduction.lower():
                print('✓ Traduction correcte !')
                score += 1
            else:
                print(f'✗ Traduction incorrecte ! La bonne réponse est : {traduction}')

        self._afficher_score_final(score, total)

    def quiz_conjugaison(self):
        verbes = self.gestionnaire.tous_les_verbes()

        if not verbes:
            print('Aucun verbe dans la base de données !')
            return

        random.shuffle(verbes)

        score = 0
        total = 0

        print("\n" + "=" * 40)
        print("          QUIZ CONJUGAISON")
        print("=" * 40)
        print("Taper 'quit' pour arrêter\n")

        nb_questions = self.demander_nb_questions(len(verbes))
        verbes = verbes[:nb_questions]

        for verbe in verbes:
            infinitif, preterit, participe_passe = verbe[1], verbe[2], verbe[3]

            print(f"\nInfinitif : {infinitif}")

            rep_pret = input(f"Prétérit de '{infinitif}' : ").strip().lower()
            if rep_pret == 'quit':
                break

            rep_pp = input(f"Participe passé de '{infinitif}' : ").strip().lower()
            if rep_pp == 'quit':
                break

            if rep_pret == preterit.lower():
                print('✓ Prétérit correct !')
                score += 1
            else:
                print(f'✗ Prétérit incorrect ! La bonne réponse est : {preterit}')

            if rep_pp == participe_passe.lower():
                print('✓ Participe passé correct !')
                score += 1
            else:
                print(f'✗ Participe passé incorrect ! La bonne réponse est : {participe_passe}')

            total += 2

        self._afficher_score_final(score, total)

    def _afficher_score_final(self, score, total):
        print("\n" + "=" * 40)
        print("          FIN DU QUIZ")
        print("=" * 40)
        print(f'Votre score final : {score}/{total}')
        if total > 0:
            pourcentage = score / total * 100
            print(f'Pourcentage de réussite : {pourcentage:.1f}%')
        print("=" * 40)


class InterfaceUtilisateur:

    def __init__(self):
        self.gestionnaire = GestionnaireVerbes()
        self.quiz = Quiz(self.gestionnaire)

    def ajouter_verbe_interface(self):
        print("\n" + "=" * 40)
        print("       AJOUTER UN NOUVEAU VERBE")
        print("=" * 40)

        infinitif = input("Infinitif (ex: eat) : ").strip()
        if not infinitif:
            print("Opération annulée.")
            return

        preterit = input("Prétérit (ex: ate) : ").strip()
        if not preterit:
            print("Opération annulée.")
            return

        participe_passe = input("Participe passé (ex: eaten) : ").strip()
        if not participe_passe:
            print("Opération annulée.")
            return

        traduction_fr = input("Traduction française (ex: manger) : ").strip()
        if not traduction_fr:
            print("Opération annulée.")
            return

        self.gestionnaire.ajouter_verbe(infinitif, preterit, participe_passe, traduction_fr)
        print(f"\n✓ Le verbe '{infinitif}' a été ajouté avec succès !")

    def tous_les_mots(self):
        con = sqlite3.connect(self.gestionnaire.nom_db)
        cursor = con.cursor()
        cursor.execute('SELECT * FROM verbes')
        verbes = cursor.fetchall() # Récupère tous les résultats de la requête SQL précédente et les stocke
        con.close()
        succes = 10
        tentatives = 15
        for word in verbes:
            id, infinitif, preterit, participe_passe, traduction_fr = word
            print (f"{infinitif}, {traduction_fr}, {succes/tentatives*100:.2f}%") 

    def supprimer_verbe_interface(self):
        print("\n" + "=" * 40)
        print("         SUPPRIMER UN VERBE")
        print("=" * 40)

        infinitif = input("Quel verbe veux-tu supprimer ? (ex: be) : ").strip()

        if not infinitif:
            print("Opération annulée.")
            return

        if self.gestionnaire.supprimer_verbe(infinitif):
            print(f"✓ Le verbe '{infinitif}' a été supprimé !")
        else:
            print(f"✗ Le verbe '{infinitif}' n'existe pas.")

    def afficher_menu(self):
        print("\n" + "=" * 40)
        print("           MENU PRINCIPAL")
        print("=" * 40)
        print("1. Quiz complet")
        print("2. Quiz traduction")
        print("3. Quiz conjugaison")
        print("4. Ajouter un verbe")
        print("5. Supprimer un verbe")
        print("6. Liste des mots")
        print("q. Quitter")
        print("=" * 40)

    def lancer(self):
        while True:
            self.afficher_menu()
            choix = input("Choisis une option (1-6) : ").strip()

            if choix == '1':
                self.quiz.quiz_complet()
            elif choix == '2':
                self.quiz.quiz_traduction()
            elif choix == '3':
                self.quiz.quiz_conjugaison()
            elif choix == '4':
                self.ajouter_verbe_interface()
            elif choix == '5':
                self.supprimer_verbe_interface()
            elif choix == '6':
                self.tous_les_mots()
            elif choix == 'q':
                print("\nAu revoir ! 👋")
                break
            else:
                print("❌ Choix invalide !")


if __name__ == "__main__":
    app = InterfaceUtilisateur()
    app.lancer()

