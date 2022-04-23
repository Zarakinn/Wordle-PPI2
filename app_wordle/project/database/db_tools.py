from operator import ge
import os
import sqlite3
import string
import fonctions

from project.exceptions import *
from project.database import dict_creator

# Emplacement du fichier de la base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database.db")
DB_FILE_FROM_PROJECT = f"project{os.sep}database{os.sep}" + DB_FILE

SCHEMA_FILE = f"project{os.sep}database{os.sep}schema.sql"
DICT_FILE = f"project{os.sep}database{os.sep}dictionnaire_data.sql"


# Requêtes basiques sur la base de données
def basic_query(sql, param_sql, disable_dict_factory=False, one_row=False):
    global cursor
    try:
        connexion = get_db(disable_dict_factory)
    except sqlite3.Error as error:
        connexionBaseDeDonneeError(str(error))
        return
    try:
        cursor = connexion.cursor()
        cursor.execute(sql, param_sql)
        if one_row:
            query = cursor.fetchone()
        else:
            query = cursor.fetchall()
    except sqlite3.Error as error:
        requetageBaseDeDonneeError(str(error))
        return
    finally:
        cursor.close()
        connexion.close()
    return query


def basic_insert(sql, param_sql):
    global cursor
    try:
        connexion = get_db(True)
    except sqlite3.Error as error:
        connexionBaseDeDonneeError()
        return
    try:
        cursor = connexion.cursor()
        cursor.execute(sql, param_sql)
        connexion.commit()
    except sqlite3.Error as error:
        requetageBaseDeDonneeError()
    finally:
        cursor.close()
        connexion.close()


def get_db(disable_dict_factory=False):
    db = sqlite3.connect(DB_FILE)
    if not disable_dict_factory:
        db.row_factory = dict_factory
    return db


# Voir: https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def generate_max_id(tables: string) -> int:
    try:
        if tables == "utilisateur":
            new_id = basic_query("SELECT MAX(idUtilisateur) FROM utilisateur", [], disable_dict_factory=True,
                                 one_row=True)
        elif tables == "partie":
            new_id = basic_query("SELECT MAX(idPartie) FROM partie", [], disable_dict_factory=True, one_row=True)
        elif tables == "parametre":
            new_id = basic_query("SELECT MAX(id) FROM parametre", [], disable_dict_factory=True, one_row=True)
        elif tables == "dictionnaire":
            new_id = basic_query("SELECT MAX(idMot) FROM dictionnaire", [], disable_dict_factory=True, one_row=True)

        if new_id == (None,):
            new_id = [0]

        return new_id[0] + 1
    except sqlite3.Error as error:
        print("Erreur lors de la génération d'un id max : ", error)


def create_db():
    connexion = sqlite3.connect(DB_FILE)
    cursor = connexion.cursor()

    # Création  des tables
    with open(SCHEMA_FILE) as file:
        sql = file.read()
        cursor.executescript(sql)

    # Récuperation des données du dictionnaire et insertion dans la base de données
    lex = dict_creator.get_dict_data()
    print("Insertion des données du dictionnaire dans la base de données...")
    lex.to_sql("dictionnaire", connexion, if_exists="replace")


## Convention uc = unencrypted, ec = encrypted

def is_valid_inscription(pseudo: str, uc_password: str) -> bool:
    querry = basic_query("SELECT * FROM utilisateur WHERE pseudo =?",pseudo,True)
    pseudo_available = querry == []
    is_valid_password = fonctions.is_valid_password(uc_password)
    return pseudo_available and is_valid_password


def save_inscription(pseudo: str, uc_password: str) -> None:
    ec_password = fonctions.encrypt(uc_password)
    id_joueur = generate_max_id("utilisateur")
    basic_insert("INSERT INTO utilisateur (idUtilisateur,pseudo,password) VALUES (?,?,?)",
                 (id_joueur, str(pseudo), str(ec_password)))


def is_good_password(pseudo: str, uc_password: str):  # -> bool,string:
    querry = basic_query("SELECT password FROM utilisateur WHERE pseudo = ?", (pseudo,), True, True)
    if querry == [] or querry == None:
        return False, "Joueur non répertorié dans la base de donnée"
    elif fonctions.encrypt(uc_password) == querry[0]:
        return True, "Bon identifiant"
    else:
        return False, "Mauvais identifiant"


def connect(pseudo: str):
    querry = basic_query("SELECT * FROM utilisateur WHERE pseudo = ?", (pseudo,), True, True)

    print("Info utilisateur :")
    print(querry)

    return querry[0], querry[1], querry[3], querry[4]  # renvoie pseudo, paramètre derniere partie et partie en cours


def register_game(motATrouver: string, idParam: int, idJoueur: int = -1) -> int:
    date = basic_query("SELECT CURRENT_TIMESTAMP", [], True, True)[0]
    idPartie = generate_max_id("partie")
    querry = "INSERT INTO partie (idPartie, parametre,estEnCours,idJoueur,motATrouver,date,tourActuel,aGagne,scorePartie) VALUES (?,?,?,?,?,?,?,?,?)"
    param_sql = (idPartie, idParam, 1, idJoueur, motATrouver, date, 0, 0, 0)

    basic_insert(querry, param_sql)
    return idPartie


def get_id_param(nb_essais: int, nb_lettres: int, difficulté: int) -> int:
    idParam = basic_query("SELECT id FROM parametre WHERE longueur = ? AND nbEssais = ? AND difficulte = ?",
                          (nb_lettres, nb_essais, difficulté), True, True)

    if idParam == [] or idParam == None:
        # Creer param
        idParam = generate_max_id("parametre")
        basic_insert("INSERT INTO parametre (id,longueur,nbEssais,difficulte) VALUES (?,?,?,?)",
                     (idParam, nb_lettres, nb_essais, difficulté))
    else:
        idParam = idParam[0]

    print(f"Id parametre = {idParam}")

    return idParam


def update_current_game_utilisateur(idUtilisateur: int, idPartie: int) -> None:
    basic_query("UPDATE utilisateur SET partieEnCours = ? WHERE idUtilisateur = ?", (idPartie, idUtilisateur))


# Calcul des scores


def calcul_score_partie(idPartie: int) -> None:
    idParam = basic_query("SELECT parametre FROM Partie WHERE idPartie = ?", idPartie)

    L = basic_query("SELECT longueur FROM parametre WHERE id =?", idParam)
    E = basic_query("SELECT nbEssais FROM parametre WHERE id =?", idParam)
    D = basic_query("SELECT difficulte FROM parametre WHERE id =?", idParam)

    scorePartie = D * (L + 13 - E)

    basic_query("UPDATE partie SET scorePartie = ?", scorePartie)


def calcul_score_utilisateur(idUtilisateur: int) -> None:  # au cas où    #TODO

    scorePartieList = basic_query("SELECT scorePartie FROM partie WHERE idJoueur = ?", idUtilisateur)
    newScoreUtilisateur = sum(scorePartieList)
    basic_query("UPDATE utilisateur SET scoreUtilisateur = ?", newScoreUtilisateur)


def add_score_utilisateur(idPartie: int) -> None:
    idJoueur = basic_query("SELECT idJoueur FROM partie WHERE idPartie = ?", idPartie)

    scoreUtilisateur = basic_query("SELECT scoreUtilisateur FROM utilisateur WHERE idUtilisateur = ?", idJoueur)
    scorePartie = basic_query("SELECT scorePartie FROM partie WHERE idPartie = ?", idPartie)

    newScoreUtilisateur = scoreUtilisateur + scorePartie

    basic_query("UPDATE utilisateur SET scoreUtilisateur = ?", newScoreUtilisateur)


# gets
def get_leaderboard_list() -> list:  # TODO

    leaderboardList = basic_query("SELECT scoreUtilisateur FROM utilisateur", ())
    return leaderboardList


def get_rang(scoreUtilisateur: int) -> int:
    Leaderboard = getLeaderboardList()
    rang = fonctions.positionInList(Leaderboard,scoreUtilisateur)
    return rang


def get_nb_parties_jouees(idUtilisateur: int) -> int:  # TODO

    nbPartiesJouees = basic_query("SELECT count(estEnCours) FROM partie WHERE idJoueur = ? AND estEnCours = ?", (idUtilisateur, False)) #Ligne too long ?
    return nbPartiesJouees


def get_nb_parties_gagnees(idUtilisateur: int) -> int:  # TODO

    nbPartiesGagnees = basic_query("SELECT count(aGagne) FROM partie WHERE idJoueur = ? AND aGagne = ?", (idUtilisateur, True)) #Ligne too long ?
    return nbPartiesGagnees


def getLongueurPreferee(idUtilisateur : int) -> int:  #TODO
    longueurList = basic_query("SELECT parametre.longueur FROM partie JOIN parametre ON partie.parametre = parametre.id WHERE partie.idJoueur = ?", idUtilisateur)

    return longueurPreferee



def getDifficultePreferee(idUtilisateur : int) -> int:  #TODO

    difficulteList = basic_query("SELECT parametre.difficulte FROM partie JOIN parametre ON partie.parametre = parametre.id WHERE partie.idJoueur = ?", idUtilisateur)

    return difficultePreferee

def get_statistiques(idUtilisateur: int) -> list:  # TODO

    scoreUtilisateur = basic_query("SELECT scoreUtilisateur FROM utilisateur WHERE idUtilisateur = ?", idUtilisateur)

    rang = get_rang(scoreUtilisateur)

    nbPartieJouees = get_nb_parties_jouees(idUtilisateur)

    nbPartieGagnees = get_nb_parties_gagnees(idUtilisateur)

    tauxDeVictoire = int(10*nbPartieGagnees/nbPartieJouees)/10   #un chiffre apres la virgule

    longueurPreferee = getLongueurPreferee(idUtilisateur)

    difficultePreferee = getDifficultePreferee(idUtilisateur)

    return [rang,scoreUtilisateur,nbPartieJouees,nbPartieGagnees,tautDeVictoire,longueurPreferee,difficultePreferee]
            difficultePreferee]
    return statList

