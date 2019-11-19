from bottle import Bottle, run, route, request, HTTPResponse, response
import json
from uuid import uuid4
import random as rd



app = Bottle()


# ----- functions ------------------------------------------------------------

def from_list_to_json(a_list):
    """
        Takes a list and return some json accepted by the front.
    """
    print("=================")
    dictionnary = {}
    offset = len(a_list) - 1
    for i, row in enumerate(a_list):
        print(row)
        for j, data in enumerate(row):
            if data:
                key = str(i) + str(j)
                dictionnary[key] = {
                    "row": abs(i-offset),
                    "col": j,
                    "color": data
                }
    print("=================")
    return json.dumps(dictionnary)


class moveNotValidError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class aiCantMoveError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

        
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


def play_AI(inJeu,color):
    """
        Play for ai or raise aiCantMoveError if the ai con't play.
    """
    for i in range(5):  # column
        for j in range(6): # line
            if is_move_valid(inJeu, j, i):
                inJeu[j][i] = color
                print("I, the ai, play", j, i)
                return inJeu, j, i
    raise aiCantMoveError("the ai can't move")


# ----- bottle functions -----------------------------------------------------

@app.route('/', method=['GET', 'POST'])
def index():
    """
        Return nothing, just 200.
    """
    return HTTPResponse(status=200)


@app.route('/api/game/start', method=['GET', 'POST'])
def start_game():
    """
        Start a new game and send the id to the client.
    """
    print("a new game should start")
    a_uuid = str(uuid4())  # more secure, but will not work with current front
    a_uuid = rd.randint(0, 1000000)
    return_value = {"id": a_uuid}
    return HTTPResponse(
        body=json.dumps(return_value),
        status=200,
        headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    )


@app.route('/api/game/<game_id>', method=['GET', 'POST'])
def load_game(game_id):
    """
        Load the game names "game_id". Be carefull, "game_id" is a string !
    """
    #let's load the game or create a new one if it does not exists
    try:
        with open("sav/" + game_id + ".json", "r") as sav:
            game = json.loads(sav.read())  # should be a 6*7 array
    except FileNotFoundError:  # new game
        game = [["" for _ in range(7)] for _ in range(6)]  # 6 * 7 array
        with open("sav/" + game_id + ".json", "w") as sav:
            sav.write(json.dumps(game))
    
    return HTTPResponse(
        body=from_list_to_json(game),
        status=200,
        headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    )

@app.route('/api/<game_id>/move', method=["OPTIONS"])
def play_game_pass(game_id):
    print("passed (options)")
    return HTTPResponse(
        body={"error": "No argument"},
        status=200,
        headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
    )


@app.route('/api/<game_id>/move', method=['GET', 'POST'])
def play_game(game_id):
    """
        Play the game names "game_id". Be carefull, "game_id" is a string !
    """
    try:
        with open("sav/" + game_id + ".json", "r") as sav:
            game = json.loads(sav.read())  # should be a 6*7 array
    except FileNotFoundError:  # the game does not exists
        return HTTPResponse(
            body={"msg": "The game does not exists"},
            status=406,
            headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
        )
    
    data_json = request.body.read().decode("utf-8")

    if not data_json:
        print("no data passed")
        return HTTPResponse(
            body={"msg": "No parameters given"},
            status=406,
            headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
        )
    
    data = json.loads(data_json)
    offset = len(game) - 1
    print("I received", data, "from the front")
    
    try:
        game = place_token(game, abs(data["row"]-offset), data["col"], data["color"])
    except moveNotValidError as e:
        print(e)
        return HTTPResponse(
            body={"msg": "The move is not valid."},
            status=406,
            headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
        )
    
    if victory(game, abs(data["row"]-offset), data["col"], data["color"]):
        pass # TODO

    ai_color = "black"
    if ai_color == data["color"]:
        ai_color = "red"

    try:
        game, row, col = play_AI(game, ai_color)
    except aiCantMoveError:
        return HTTPResponse(
            body={"msg": "The AI can't play."},
            status=406,
            headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
        )

    if victory(game, row, col, ai_color):
        pass # TODO

    with open("sav/" + game_id + ".json", "w") as sav:
        sav.write(json.dumps(game))


    return HTTPResponse(
        body={"col": col, "row": abs(row-offset)},  # TODO: pass the game too
        status=200,
        headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
    )

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8081, quiet=True)