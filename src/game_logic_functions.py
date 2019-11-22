from errors import moveNotValidError


def is_move_valid(inJeu, inLigne, inColonne):
    # the move is valid if and only if the position is empty and all
    # position below is taken
    if inJeu[inLigne][inColonne]: 
        return False
    for i in range(inLigne+1, len(inJeu)):
        if not inJeu[i][inColonne]:
            return False
    return True


def place_token(inJeu, inLigne, inColonne, color):
    """
        Place the token in the grid. Return the grid. Raise moveNotValidError
        if the move is not valid.
    """
    if not is_move_valid(inJeu, inLigne, inColonne):
        raise moveNotValidError("move not valid :" + str(inJeu) + " " + str(inLigne) + " " + str(inColonne))
    inJeu[inLigne][inColonne] = color
    return inJeu


def horizontal_check(inJeu, inLigne, inColonne, color):
    compteur = 0
    ColonnePLus = inColonne + 1
    ColonneMoin = inColonne - 1
    while ColonneMoin >= 0:
        print("e", inLigne, ColonneMoin)
        if inJeu[inLigne][ColonneMoin] == color:
            ColonneMoin -= 1
            compteur += 1
        else:
            break
    while ColonnePLus < 7:
        if inJeu[inLigne][ColonnePLus] == color:
            ColonnePLus += 1
            compteur += 1
        else:
            break
    return compteur+1


def vertical_check(inJeu,inLigne, inColonne, color):
    compteur = 0
    LignePLus = inLigne + 1
    LigneMoin = inLigne - 1
    while LigneMoin >= 0:
        if inJeu[LigneMoin][inColonne] == color:
            LigneMoin -= 1
            compteur += 1
        else:
            break
    while LignePLus < 6:
        if inJeu[LignePLus][inColonne] == color:
            LignePLus += 1
            compteur += 1
        else:
            break
    return compteur +1


def diagonal_left_check(inJeu,inLigne, inColonne, color):
    compteur = 0
    LignePLus = inLigne +1
    LigneMoin = inLigne -1
    ColonnePLus = inColonne +1
    ColonneMoin = inColonne -1
    while LignePLus < 6 and ColonnePLus < 7:
        if inJeu[LignePLus][ColonnePLus] == color:
            LignePLus += 1
            ColonnePLus +=1
            compteur += 1
        else:
            break
    while LigneMoin >= 0 and ColonneMoin >= 0:
        if inJeu[LigneMoin][ColonneMoin] == color:
            LigneMoin -= 1
            ColonneMoin -=1
            compteur += 1
        else:
            break
    return compteur +1


def diagonal_right_check(inJeu,inLigne, inColonne,color):
    compteur = 0
    LignePLus = inLigne +1
    LigneMoin = inLigne -1
    ColonnePLus = inColonne +1
    ColonneMoin = inColonne -1
    while LignePLus < 6 and ColonneMoin >= 0:
        if inJeu[LignePLus][ColonneMoin] == color:
            LignePLus += 1
            ColonneMoin -=1
            compteur += 1
        else:
            break
    while LigneMoin >= 0 and ColonnePLus < 7:
        if inJeu[LigneMoin][ColonnePLus] == color:
            LigneMoin -= 1
            ColonnePLus +=1
            compteur += 1
        else:
            break
    return compteur +1


def victory(inJeu, inLigne, inColonne, color):
    victory_h = horizontal_check(inJeu,inLigne, inColonne,color) >= 4
    victory_v = vertical_check(inJeu,inLigne, inColonne, color) >= 4
    victory_d = diagonal_left_check(inJeu,inLigne, inColonne, color) >= 4 or diagonal_right_check(inJeu, inLigne, inColonne, color) >= 4
    # let's return true if one of them is true
    return victory_h or victory_v or victory_d