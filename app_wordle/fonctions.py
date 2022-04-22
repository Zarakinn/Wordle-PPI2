
def ValidPassword(uc_password : str) -> bool:
    # Un password est valide ssi il comporte entre 10 et 32 carractères, dont 1 chiffre, 1 minuscule et 1 majuscule
    if len(uc_password) < 10 or len(uc_password) > 32:
        return False

    maj, min, num = False, False, False

    for c in uc_password:
        maj = maj + c.isupper()
        min = min + c.islower()
        num = num + c.isdigit()

    return bool(maj * min * num)


def Encrypt(uc_string : str) -> str:

    ec_string = uc_string

    #TODO encypter

    return ec_string


def triFusion(tab : list) -> None:
    # Effectue un tri fusion sur tab
    if len(tab) > 1:
        mid = len(tab) // 2

        G = tab[:mid]  # sous-tableau gauche
        D = tab[mid:]  # sous-tableau droit

        triFusion(G)
        triFusion(D)

        # Fusion
        i = j = k = 0

        while i < len(G) and j < len(D):
            if G[i] < D[j]:
                tab[k] = G[i]
                i += 1
            else:
                tab[k] = D[j]
                j += 1
            k += 1

        while i < len(G):
            tab[k] = G[i]
            i += 1
            k += 1

        while j < len(D):
            tab[k] = D[j]
            j += 1
            k += 1
    return None


def positionInList(tab : list, element : int) -> int:   # tab.index(element) ne renvoie pas 0 en cas d'erreur
    for i in range(len(tab)):
        if tab[i] == element:  # comme ça les égalités ont le meme rang
            return i
    return 0


