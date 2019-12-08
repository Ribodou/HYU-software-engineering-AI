from bottle import Bottle, run, route, request, HTTPResponse, response
import random as rd
import json
from game_logic_functions import victory
# from uuid import uuid4
from errors import moveNotValidError, aiCantMoveError
import ai_module
from game_logic_functions import place_token
import os
import sys

ABSOLUTE_PATH_TO_SCRIPT=os.path.realpath(sys.path[0])


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


app = Bottle()

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
    # a_uuid = str(uuid4())  # more secure, but will not work with current front
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
    
    print( os.path.join(ABSOLUTE_PATH_TO_SCRIPT, "/../sav/" + game_id + ".json") )

    #let's load the game or create a new one if it does not exists
    try:
        with open(ABSOLUTE_PATH_TO_SCRIPT + "/../sav/" + game_id + ".json", "r") as sav:
            game = json.loads(sav.read())  # should contains a 6*7 array, the name of the first player and a list of moves
    except FileNotFoundError:  # new game
        tab = [["" for _ in range(7)] for _ in range(6)]  # 6 * 7 array
        first_player = None
        list_of_moves = []
        game = {}
        game["tab"] = tab
        game["first_player"] = first_player
        game["list_of_moves"] = list_of_moves
        with open(ABSOLUTE_PATH_TO_SCRIPT + "/../sav/" + game_id + ".json", "w") as sav:
            sav.write(json.dumps(game))
    
    return HTTPResponse(
        body=from_list_to_json(game["tab"]),
        status=200,
        headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    )

@app.route('/api/game/<game_id>/move', method=["OPTIONS"])
def play_game_pass(game_id):
    print("passed (options)")
    return HTTPResponse(
        body={"error": "No argument"},
        status=200,
        headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
    )


@app.route('/api/game/<game_id>/move', method=['GET', 'POST'])
def play_game(game_id):
    """
        Play the game names "game_id". Be carefull, "game_id" is a string !
    """
    try:
        with open(ABSOLUTE_PATH_TO_SCRIPT + "/../sav/" + game_id + ".json", "r") as sav:
            game = json.loads(sav.read())  # should contains a 6*7 array, the name of the first player and a list of moves
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
    offset = len(game["tab"]) - 1
    # transformation into something our program can understand
    data["row"] = abs(data["row"]-offset)
    print("I received", data, "from the front")
    
    try:
        game["tab"] = place_token(game["tab"], data["row"], data["col"], data["color"])
        if not game["first_player"]:
            game["first_player"] = data["color"]  # for now, the first player is considered human
        game["list_of_moves"].append((data["row"], data["col"]))
    except moveNotValidError as e:
        print(e)
        return HTTPResponse(
            body={"msg": "The move is not valid."},
            status=406,
            headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
        )
    
    if victory(game["tab"], data["row"], data["col"], data["color"]):
        pass # TODO

    ai_color = "black"
    if ai_color == data["color"]:
        ai_color = "red"

    try:
        ai = ai_module.AI()
        game["tab"], row, col = ai.play(game["tab"], ai_color)
        game["list_of_moves"].append((row, col))
    except aiCantMoveError:
        return HTTPResponse(
            body={"msg": "The AI can't play."},
            status=406,
            headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
        )

    if victory(game["tab"], row, col, ai_color):
        pass # TODO

    with open(ABSOLUTE_PATH_TO_SCRIPT + "/../sav/" + game_id + ".json", "w") as sav:
        sav.write(json.dumps(game))

    print("returning", {"col": col, "row": abs(row-offset)})
    return HTTPResponse(
        body={"col": col, "row": abs(row-offset)},  # TODO: pass the game too
        status=200,
        headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
    )


@app.route('/api/game/<game_id>/undo-move', method=['GET', 'POST'])
def undo_move(game_id):
    """
        Undo the last move of the game named "game_id". Be carefull, "game_id" is a string !
    """
    try:
        with open(ABSOLUTE_PATH_TO_SCRIPT + "/../sav/" + game_id + ".json", "r") as sav:
            game = json.loads(sav.read())  # should contains a 6*7 array, the name of the first player and a list of moves
    except FileNotFoundError:  # the game does not exists
        return HTTPResponse(
            body={"msg": "The game does not exists"},
            status=406,
            headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
        )

    if len(game["list_of_moves"]) == 0:
        return HTTPResponse(
            body={"msg": "You didn't played yet"},
            status=406,
            headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'}
        )
    
    print("list of move before", game["list_of_moves"])

    lastmove = game["list_of_moves"].pop(-1)
    game["tab"][lastmove[0]][lastmove[1]] = ""
    if len(game["list_of_moves"]) % 2 != 0:  # if the last player is not human, then we must go back two times
        lastmove = game["list_of_moves"].pop(-1)
        game["tab"][lastmove[0]][lastmove[1]] = ""

    print("list of move after", game["list_of_moves"])

    with open(ABSOLUTE_PATH_TO_SCRIPT + "/../sav/" + game_id + ".json", "w") as sav:
        sav.write(json.dumps(game))
    
    return HTTPResponse(
        body=from_list_to_json(game["tab"]),
        status=200,
        headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    )
