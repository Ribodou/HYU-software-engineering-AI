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



# ----- bottle functions -----------------------------------------------------

@app.route('/', method=['GET', 'POST'])
def index():
    """
        Return nothing, just 200.
    """
    return HTTPResponse(status=200)
    # data_json = request.body.read().decode("utf-8")
    # if data_json:
    #     data = json.loads(data_json)
    #     print(data)


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


@app.route('/api/game/<id>', method=['GET', 'POST'])
def play_game(id):
    """
        Play the game names "id". Be carefull, "id" is a string !
        Always return a empty game for now.
    """
    #let's laod the game or create a new one if it does not exists
    try:
        with open("sav/" + id + ".json", "r") as sav:
            game = json.loads(sav.read())  # should be a 6*7 array
    except FileNotFoundError:  # new game
        game = [["" for _ in range(7)] for _ in range(6)]  # 6 * 7 array
        with open("sav/" + id + ".json", "w") as sav:
            sav.write(json.dumps(game))
    
    return HTTPResponse(
        body=from_list_to_json(game),
        status=200,
        headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    )


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8081, quiet=True)