import sqlite3
import random


class GestionnaireBase:
    """Classe de base pour gérer les connexions à la base de données"""
    
    def __init__(self, nom_db='words.db'): # Permet d'initialiser un objet à chaque fois que l'on crée un objet dans la classe
        self.nom_db = nom_db # Crée un attribut et le stocke dans l'objet + Création variable
        self._initialiser_base() # Appelle la méthode
    
    def _initialiser_base(self):  # Création de la méthode
        con = sqlite3.connect(self.nom_db) # Crée une base de données et établit une connexion
        cursor = con.cursor()
        
        # Table verbes avec colonnes de performance
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS verbes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            infinitif TEXT NOT NULL,
            preterit TEXT NOT NULL,
            participe_passe TEXT NOT NULL,
            traduction_fr TEXT NOT NULL,
            succes INTEGER DEFAULT 0,
            tentatives INTEGER DEFAULT 0
        )
        ''')
        
        # Table acronymes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS acronymes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acronyme TEXT NOT NULL,
            definition TEXT NOT NULL,
            succes INTEGER DEFAULT 0,
            tentatives INTEGER DEFAULT 0
        )
        ''')
        
        # Vérifier si les colonnes succes/tentatives existent dans verbes
        cursor.execute("PRAGMA table_info(verbes)")
        colonnes = [col[1] for col in cursor.fetchall()] # Crée une liste contenant le deuxième champ de chaque ligne retournée par la requête SQL précédente
         
        if 'succes' not in colonnes:
            cursor.execute('ALTER TABLE verbes ADD COLUMN succes INTEGER DEFAULT 0')
        if 'tentatives' not in colonnes:
            cursor.execute('ALTER TABLE verbes ADD COLUMN tentatives INTEGER DEFAULT 0')
        
        # Données d'exemple pour les verbes
        cursor.execute('SELECT COUNT(*) FROM verbes')
        if cursor.fetchone()[0] == 0: # Récupére toutes les lignes résultant d’une requête SQL exécutée auparavant
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
            cursor.executemany('''
            INSERT INTO verbes (infinitif, preterit, participe_passe, traduction_fr)
            VALUES (?, ?, ?, ?)
            ''', verbes_data)
        
        # Données d'exemple pour les acronymes
        cursor.execute('SELECT COUNT(*) FROM acronymes')
        if cursor.fetchone()[0] == 0:
            acronymes_data = [
                ('ONU', 'Organisation des Nations Unies'),
                ('NATO', 'North Atlantic Treaty Organization'),
                ('UNESCO', 'United Nations Educational Scientific and Cultural Organization'),
                ('FBI', 'Federal Bureau of Investigation'),
                ('CIA', 'Central Intelligence Agency'),
            ]
            cursor.executemany('''
            INSERT INTO acronymes (acronyme, definition)
            VALUES (?, ?)
            ''', acronymes_data)
        
        con.commit()
        con.close()


class GestionnaireVerbes(GestionnaireBase):
    """Gère les opérations sur les verbes"""
    
    def tous_les_verbes(self):
        con = sqlite3.connect(self.nom_db)
        cursor = con.cursor()
        cursor.execute('SELECT * FROM verbes')
        verbes = cursor.fetchall()
        con.close()
        return verbes
    
    def ajouter_verbe(self, infinitif, preterit, participe_passe, traduction_fr):
        con = sqlite3.connect(self.nom_db)
        cursor = con.cursor()
        cursor.execute('''
        INSERT INTO verbes (infinitif, preterit, participe_passe, traduction_fr, succes, tentatives)
        VALUES (?, ?, ?, ?, 0, 0)
        ''', (infinitif, preterit, participe_passe, traduction_fr))
        con.commit()
        con.close()
    
    def supprimer_verbe(self, infinitif):
        con = sqlite3.connect(self.nom_db)
        cursor = con.cursor()
        cursor.execute('DELETE FROM verbes WHERE LOWER(infinitif) = ?', (infinitif.lower(),))
        nb_supprimes = cursor.rowcount
        con.commit()
        con.close()
        return nb_supprimes > 0
    
    def mettre_a_jour_stats(self, verbe_id, reussi):
        """Met à jour les statistiques de réussite"""
        con = sqlite3.connect(self.nom_db)
        cursor = con.cursor()
        
        if reussi:
            cursor.execute('''
            UPDATE verbes 
            SET succes = succes + 1, tentatives = tentatives + 1 
            WHERE id = ?
            ''', (verbe_id,))
        else:
            cursor.execute('''
            UPDATE verbes 
            SET tentatives = tentatives + 1 
            WHERE id = ?
            ''', (verbe_id,))
        
        con.commit()
        con.close()
    
    def obtenir_verbes_ponderes(self):
        """Retourne les verbes triés par taux d'échec (les moins réussis en premier)"""
        verbes = self.tous_les_verbes()
        
        # Calculer le taux d'échec pour chaque verbe
        verbes_avec_poids = []
        for verbe in verbes:
            id, infinitif, preterit, participe_passe, traduction_fr, succes, tentatives = verbe
            
            # Si jamais testé, priorité moyenne
            if tentatives == 0:
                poids = 0.5
            else:
                # Plus le taux d'échec est élevé, plus le poids est élevé
                poids = 1 - (succes / tentatives)
            
            verbes_avec_poids.append((verbe, poids))
        
        # Trier par poids décroissant (les plus difficiles en premier)
        verbes_avec_poids.sort(key=lambda x: x[1], reverse=True)
        
        return [v[0] for v in verbes_avec_poids]


class GestionnaireAcronymes(GestionnaireBase):
    """Gère les opérations sur les acronymes"""
    
    def tous_les_acronymes(self):
        con = sqlite3.connect(self.nom_db)
        cursor = con.cursor()
        cursor.execute('SELECT * FROM acronymes')
        acronymes = cursor.fetchall()
        con.close()
        return acronymes
    
    def ajouter_acronyme(self, acronyme, definition):
        con = sqlite3.connect(self.nom_db)
        cursor = con.cursor()
        cursor.execute('''
        INSERT INTO acronymes (acronyme, definition, succes, tentatives)
        VALUES (?, ?, 0, 0)
        ''', (acronyme, definition))
        con.commit()
        con.close()
    
    def supprimer_acronyme(self, acronyme):
        con = sqlite3.connect(self.nom_db)
        cursor = con.cursor()
        cursor.execute('DELETE FROM acronymes WHERE LOWER(acronyme) = ?', (acronyme.lower(),))
        nb_supprimes = cursor.rowcount
        con.commit()
        con.close()
        return nb_supprimes > 0
    
    def mettre_a_jour_stats(self, acronyme_id, reussi):
        """Met à jour les statistiques de réussite"""
        con = sqlite3.connect(self.nom_db)
        cursor = con.cursor()
        
        if reussi:
            cursor.execute('''
            UPDATE acronymes 
            SET succes = succes + 1, tentatives = tentatives + 1 
            WHERE id = ?
            ''', (acronyme_id,))
        else:
            cursor.execute('''
            UPDATE acronymes 
            SET tentatives = tentatives + 1 
            WHERE id = ?
            ''', (acronyme_id,))
        
        con.commit()
        con.close()
    
    def obtenir_acronymes_ponderes(self):
        """Retourne les acronymes triés par taux d'échec"""
        acronymes = self.tous_les_acronymes()
        
        acronymes_avec_poids = []
        for acronyme in acronymes:
            id, acro, definition, succes, tentatives = acronyme
            
            if tentatives == 0:
                poids = 0.5
            else:
                poids = 1 - (succes / tentatives)
            
            acronymes_avec_poids.append((acronyme, poids))
        
        acronymes_avec_poids.sort(key=lambda x: x[1], reverse=True)
        
        return [a[0] for a in acronymes_avec_poids]


class QuizInfini:
    """Gère les quiz en mode infini avec sélection intelligente"""
    
    def __init__(self, gestionnaire_verbes, gestionnaire_acronymes):
        self.gest_verbes = gestionnaire_verbes
        self.gest_acronymes = gestionnaire_acronymes
    
    def quiz_verbes_complet_infini(self):
        """Quiz verbes complet en mode infini"""
        print("\n" + "=" * 50)
        print("     QUIZ VERBES COMPLET (Mode Infini)")
        print("=" * 50)
        print("Les mots que tu rates reviendront plus souvent !")
        print("Tape 'quit' pour arrêter\n")
        
        questions_posees = 0
        
        while True:
            # Récupérer les verbes triés par difficulté
            verbes = self.gest_verbes.obtenir_verbes_ponderes()
            
            if not verbes:
                print("Aucun verbe dans la base !")
                return
            
            # Prendre un verbe parmi les 5 plus difficiles (ou tous si moins de 5)
            pool_size = min(5, len(verbes))
            verbe = random.choice(verbes[:pool_size])
            
            id, infinitif, preterit, participe_passe, traduction_fr, succes, tentatives = verbe
            
            print(f"\n{'='*50}")
            print(f"Question {questions_posees + 1} | Verbe : {infinitif}")
            print(f"{'='*50}")
            
            # Traduction
            rep_trad = input(f"Traduction française : ").strip()
            if rep_trad.lower() == 'quit':
                break
            
            # Prétérit
            rep_pret = input(f"Prétérit : ").strip()
            if rep_pret.lower() == 'quit':
                break
            
            # Participe passé
            rep_pp = input(f"Participe passé : ").strip()
            if rep_pp.lower() == 'quit':
                break
            
            # Vérification
            points = 0
            
            if rep_trad.lower() == traduction_fr.lower():
                print("✓ Traduction correcte !")
                points += 1
            else:
                print(f"✗ Traduction : {traduction_fr}")
            
            if rep_pret.lower() == preterit.lower():
                print("✓ Prétérit correct !")
                points += 1
            else:
                print(f"✗ Prétérit : {preterit}")
            
            if rep_pp.lower() == participe_passe.lower():
                print("✓ Participe passé correct !")
                points += 1
            else:
                print(f"✗ Participe passé : {participe_passe}")
            
            # Mise à jour des stats
            reussi = (points == 3)
            self.gest_verbes.mettre_a_jour_stats(id, reussi)
            
            # Afficher le score
            taux = (succes + (1 if reussi else 0)) / (tentatives + 1) * 100
            print(f"\nScore : {points}/3")
            print(f"Taux de réussite pour ce mot : {taux:.1f}%")
            
            questions_posees += 1
        
        print(f"\n✓ Quiz terminé ! {questions_posees} questions posées.")
    
    def quiz_verbes_traduction_infini(self):
        """Quiz traduction uniquement en mode infini"""
        print("\n" + "=" * 50)
        print("     QUIZ TRADUCTION (Mode Infini)")
        print("=" * 50)
        print("Tape 'quit' pour arrêter\n")
        
        questions_posees = 0
        
        while True:
            verbes = self.gest_verbes.obtenir_verbes_ponderes()
            
            if not verbes:
                print("Aucun verbe dans la base !")
                return
            
            pool_size = min(5, len(verbes))
            verbe = random.choice(verbes[:pool_size])
            
            id, infinitif, preterit, participe_passe, traduction_fr, succes, tentatives = verbe
            
            print(f"\nQuestion {questions_posees + 1} : {infinitif}")
            rep = input("Traduction française : ").strip()
            
            if rep.lower() == 'quit':
                break
            
            reussi = (rep.lower() == traduction_fr.lower())
            
            if reussi:
                print("✓ Correct !")
            else:
                print(f"✗ Réponse : {traduction_fr}")
            
            self.gest_verbes.mettre_a_jour_stats(id, reussi)
            
            taux = (succes + (1 if reussi else 0)) / (tentatives + 1) * 100
            print(f"Taux de réussite : {taux:.1f}%")
            
            questions_posees += 1
        
        print(f"\n✓ Quiz terminé ! {questions_posees} questions posées.")
    
    def quiz_verbes_conjugaison_infini(self):
        """Quiz conjugaison uniquement en mode infini"""
        print("\n" + "=" * 50)
        print("     QUIZ CONJUGAISON (Mode Infini)")
        print("=" * 50)
        print("Tape 'quit' pour arrêter\n")
        
        questions_posees = 0
        
        while True:
            verbes = self.gest_verbes.obtenir_verbes_ponderes()
            
            if not verbes:
                print("Aucun verbe dans la base !")
                return
            
            pool_size = min(5, len(verbes))
            verbe = random.choice(verbes[:pool_size])
            
            id, infinitif, preterit, participe_passe, traduction_fr, succes, tentatives = verbe
            
            print(f"\nQuestion {questions_posees + 1} : {infinitif}")
            
            rep_pret = input("Prétérit : ").strip()
            if rep_pret.lower() == 'quit':
                break
            
            rep_pp = input("Participe passé : ").strip()
            if rep_pp.lower() == 'quit':
                break
            
            points = 0
            
            if rep_pret.lower() == preterit.lower():
                print("✓ Prétérit correct !")
                points += 1
            else:
                print(f"✗ Prétérit : {preterit}")
            
            if rep_pp.lower() == participe_passe.lower():
                print("✓ Participe passé correct !")
                points += 1
            else:
                print(f"✗ Participe passé : {participe_passe}")
            
            reussi = (points == 2)
            self.gest_verbes.mettre_a_jour_stats(id, reussi)
            
            taux = (succes + (1 if reussi else 0)) / (tentatives + 1) * 100
            print(f"Score : {points}/2")
            print(f"Taux de réussite : {taux:.1f}%")
            
            questions_posees += 1
        
        print(f"\n✓ Quiz terminé ! {questions_posees} questions posées.")
    
    def quiz_acronymes_infini(self):
        """Quiz acronymes en mode infini"""
        print("\n" + "=" * 50)
        print("     QUIZ ACRONYMES (Mode Infini)")
        print("=" * 50)
        print("Tape 'quit' pour arrêter\n")
        
        questions_posees = 0
        
        while True:
            acronymes = self.gest_acronymes.obtenir_acronymes_ponderes()
            
            if not acronymes:
                print("Aucun acronyme dans la base !")
                return
            
            pool_size = min(5, len(acronymes))
            acronyme = random.choice(acronymes[:pool_size])
            
            id, acro, definition, succes, tentatives = acronyme
            
            print(f"\nQuestion {questions_posees + 1} : {acro}")
            rep = input("Définition complète : ").strip()
            
            if rep.lower() == 'quit':
                break
            
            reussi = (rep.lower() == definition.lower())
            
            if reussi:
                print("✓ Correct !")
            else:
                print(f"✗ Réponse : {definition}")
            
            self.gest_acronymes.mettre_a_jour_stats(id, reussi)
            
            taux = (succes + (1 if reussi else 0)) / (tentatives + 1) * 100
            print(f"Taux de réussite : {taux:.1f}%")
            
            questions_posees += 1
        
        print(f"\n✓ Quiz terminé ! {questions_posees} questions posées.")


class InterfaceUtilisateur:
    
    def __init__(self): 
        self.gest_verbes = GestionnaireVerbes()
        self.gest_acronymes = GestionnaireAcronymes()
        self.quiz = QuizInfini(self.gest_verbes, self.gest_acronymes)
    
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
        
        self.gest_verbes.ajouter_verbe(infinitif, preterit, participe_passe, traduction_fr)
        print(f"\n✓ Le verbe '{infinitif}' a été ajouté avec succès !")
    
    def ajouter_acronyme_interface(self):
        print("\n" + "=" * 40)
        print("       AJOUTER UN NOUVEL ACRONYME")
        print("=" * 40)
        
        acronyme = input("Acronyme (ex: NASA) : ").strip().upper()
        if not acronyme:
            print("Opération annulée.")
            return
        
        definition = input("Définition complète : ").strip()
        if not definition:
            print("Opération annulée.")
            return
        
        self.gest_acronymes.ajouter_acronyme(acronyme, definition)
        print(f"\n✓ L'acronyme '{acronyme}' a été ajouté avec succès !")
    
    def supprimer_verbe_interface(self):
        print("\n" + "=" * 40)
        print("         SUPPRIMER UN VERBE")
        print("=" * 40)
        
        infinitif = input("Quel verbe veux-tu supprimer ? : ").strip()
        
        if not infinitif:
            print("Opération annulée.")
            return
        
        if self.gest_verbes.supprimer_verbe(infinitif):
            print(f"✓ Le verbe '{infinitif}' a été supprimé !")
        else:
            print(f"✗ Le verbe '{infinitif}' n'existe pas.")
    
    def supprimer_acronyme_interface(self):
        print("\n" + "=" * 40)
        print("         SUPPRIMER UN ACRONYME")
        print("=" * 40)
        
        acronyme = input("Quel acronyme veux-tu supprimer ? : ").strip()
        
        if not acronyme:
            print("Opération annulée.")
            return
        
        if self.gest_acronymes.supprimer_acronyme(acronyme):
            print(f"✓ L'acronyme '{acronyme}' a été supprimé !")
        else:
            print(f"✗ L'acronyme '{acronyme}' n'existe pas.")
    
    def afficher_statistiques(self):
        print("\n" + "=" * 50)
        print("              STATISTIQUES")
        print("=" * 50)
        
        print("\n📚 VERBES :")
        verbes = self.gest_verbes.tous_les_verbes()
        if verbes:
            for verbe in verbes:
                id, infinitif, preterit, participe_passe, traduction_fr, succes, tentatives = verbe
                if tentatives > 0:
                    taux = (succes / tentatives) * 100
                    print(f"{infinitif:15} | Réussite : {taux:5.1f}% ({succes}/{tentatives})")
                else:
                    print(f"{infinitif:15} | Jamais testé")
        else:
            print("Aucun verbe dans la base.")
        
        print("\n📖 ACRONYMES :")
        acronymes = self.gest_acronymes.tous_les_acronymes()
        if acronymes:
            for acronyme in acronymes:
                id, acro, definition, succes, tentatives = acronyme
                if tentatives > 0:
                    taux = (succes / tentatives) * 100
                    print(f"{acro:15} | Réussite : {taux:5.1f}% ({succes}/{tentatives})")
                else:
                    print(f"{acro:15} | Jamais testé")
        else:
            print("Aucun acronyme dans la base.")
        
        print("=" * 50)
    
    def afficher_menu(self):
        print("\n" + "=" * 50)
        print("              MENU PRINCIPAL")
        print("=" * 50)
        print("📚 QUIZ VERBES (Mode Infini)")
        print("  1. Quiz Complet")
        print("  2. Quiz Traduction")
        print("  3. Quiz Conjugaison")
        print("\n📖 QUIZ ACRONYMES")
        print("  4. Quiz Acronymes")
        print("\n⚙️  GESTION")
        print("  5. Ajouter un verbe")
        print("  6. Ajouter un acronyme")
        print("  7. Supprimer un verbe")
        print("  8. Supprimer un acronyme")
        print("  9. Statistiques")
        print("\n  q. Quitter")
        print("=" * 50)
    
    def lancer(self):
        print("\n" + "🎓" * 25)
        print("  BIENVENUE DANS LE QUIZ INTELLIGENT !")
        print("🎓" * 25)
        
        while True:
            self.afficher_menu()
            choix = input("\nChoisis une option : ").strip().lower()
            
            if choix == '1':
                self.quiz.quiz_verbes_complet_infini()
            elif choix == '2':
                self.quiz.quiz_verbes_traduction_infini()
            elif choix == '3':
                self.quiz.quiz_verbes_conjugaison_infini()
            elif choix == '4':
                self.quiz.quiz_acronymes_infini()
            elif choix == '5':
                self.ajouter_verbe_interface()
            elif choix == '6':
                self.ajouter_acronyme_interface()
            elif choix == '7':
                self.supprimer_verbe_interface()
            elif choix == '8':
                self.supprimer_acronyme_interface()
            elif choix == '9':
                self.afficher_statistiques()
            elif choix == 'q':
                print("\n" + "👋" * 25)
                print("  Au revoir et bon apprentissage !")
                print("👋" * 25 + "\n")
                break
            else:
                print("❌ Choix invalide !")


if __name__ == "__main__":
    app = InterfaceUtilisateur()
    app.lancer()