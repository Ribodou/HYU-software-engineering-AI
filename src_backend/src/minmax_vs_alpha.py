import os
import sys
import random as rd
import json
import ai_module
from game_logic_functions import victory
from errors import moveNotValidError, aiCantMoveError
from timeit import default_timer as timer

ABSOLUTE_PATH_TO_SCRIPT=os.path.realpath(sys.path[0])
ABSOLUTE_SAVE_FOLDER_PATH=ABSOLUTE_PATH_TO_SCRIPT + "/../minmax_vs_alpha_sav/"

MINMAX_COLOR = 'black'
ALPHAZERO_COLOR = 'red'

ITERATIONS = 3


stats = {
    'iterations_count': 0,
    'MinMax_Won': 0,
    'AlphaZero_Won': 0,
}

for iter in range(1, ITERATIONS + 1):
    #####################################################################################################
    #  Create new Game
    #####################################################################################################

    print("Creating a new game")
    # a_uuid = str(uuid4())  # more secure, but will not work with current front
    a_uuid = rd.randint(0, 1000000)
    game_id = str(a_uuid)
    print('This game ID is: ', game_id)

    #let's load the game or create a new one if it does not exists
    try:
        with open(ABSOLUTE_SAVE_FOLDER_PATH + game_id + ".json", "r") as sav:
            game = json.loads(sav.read())  # should contains a 6*7 array, the name of the first player and a list of moves
    except FileNotFoundError:  # new game
        tab = [["" for _ in range(7)] for _ in range(6)]  # 6 * 7 array
        first_player = None
        list_of_moves = {}
        game = {}
        game['moves_count'] = 0
        game['time_elapsed_black'] = 0
        game['time_elapsed_red'] = 0
        game["tab"] = tab
        game["first_player"] = first_player
        game["list_of_moves"] = list_of_moves
        with open(ABSOLUTE_SAVE_FOLDER_PATH + game_id + ".json", "w") as sav:
            sav.write(json.dumps(game))

    #####################################################################################################
    #  Functions
    #####################################################################################################

    def minMax_Move(game, options):
        try:
            ai = ai_module.AI()
            game["tab"], row, col = ai.play(game["tab"], MINMAX_COLOR, 'min-max', options)
        except aiCantMoveError as e:
            print(e)
        
        return game["tab"], row, col

    def alphaZero_Move(game, options):
        try:
            ai = ai_module.AI()
            game["tab"], row, col = ai.play(game["tab"], ALPHAZERO_COLOR, 'min-max', options)
        except aiCantMoveError as e:
            print(e)
        
        return game["tab"], row, col

    #####################################################################################################
    #  Moves
    #####################################################################################################

    someone_won = False

    while(not someone_won):
        ############### MinMax
        minMaxOptions = {'windowLength': 1}
        start = timer()
        game["tab"], minmax_row_move, minmax_col_move = minMax_Move(game, minMaxOptions)
        end = timer()
        time_elapsed = end - start
        game[('time_elapsed_' + MINMAX_COLOR)] += time_elapsed
        game['moves_count'] += 1
        game["list_of_moves"][game['moves_count']] = {'row':minmax_row_move, 'col': minmax_col_move, 'color': MINMAX_COLOR}

        if victory(game["tab"], minmax_row_move, minmax_col_move, MINMAX_COLOR):
            someone_won = True
            stats['MinMax_Won'] += 1
            print("##################################################")
            print('Min Max Won!')
            print("##################################################")
            break # TODO

        ############### AlphaZero
        alphaZeroOptions = {'windowLength': 4}
        start = timer()
        game["tab"], alphaZero_row_move, alphaZero_col_move = alphaZero_Move(game, alphaZeroOptions)
        end = timer()
        time_elapsed = end - start
        game[('time_elapsed_' + ALPHAZERO_COLOR)] += time_elapsed
        game['moves_count'] += 1
        game["list_of_moves"][game['moves_count']] = {'row':alphaZero_row_move, 'col': alphaZero_col_move, 'color': ALPHAZERO_COLOR}

        if victory(game["tab"], alphaZero_row_move, alphaZero_col_move, ALPHAZERO_COLOR):
            someone_won = True
            stats['AlphaZero_Won'] += 1
            print("##################################################")
            print('AlphaZero Won!')
            print("##################################################")
            break # TODO


    with open(ABSOLUTE_SAVE_FOLDER_PATH + game_id + ".json", "w") as sav:
        sav.write(json.dumps(game))

    stats['iterations_count'] += 1

with open(ABSOLUTE_SAVE_FOLDER_PATH + 'iterations_' + str(ITERATIONS) + ".json", "w") as sav:
        sav.write(json.dumps(stats))