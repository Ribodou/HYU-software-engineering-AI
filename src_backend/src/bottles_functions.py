from bottle import Bottle, run, route, request, HTTPResponse, response
import random as rd
import json
from game_logic_functions import victory
# from uuid import uuid4
from errors import moveNotValidError, aiCantMoveError
import ai_module
from game_logic_functions import place_token


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
        ai = ai_module.AI()
        game, row, col = ai.play(game, ai_color)
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