import os
import sys
import random as rd
import json
import ai_module
from game_logic_functions import victory
from errors import moveNotValidError, aiCantMoveError
from timeit import default_timer as timer
import time

ABSOLUTE_PATH_TO_SCRIPT=os.path.realpath(os.getcwd())
ABSOLUTE_SAVE_FOLDER_PATH=ABSOLUTE_PATH_TO_SCRIPT + "/../minmax_vs_alpha_sav/"

timestr = time.strftime("%d%m%Y-%H%M%S")


PLAYER_COLOR = {
    'player_one': 'black',
    'player_two': 'red'
}

stats = {
    'game_history': {}
}

'''
{
        'title': 'MM_p1w4_vs_p2w4',
        'starting_player': 'player_one',
        'iterations': 1,
        'player_one': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        }
    },
    {
        'title': 'MM_p1w4_vs_p2w3',
        'starting_player': 'player_one',
        'iterations': 1,
        'player_one': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 3
            }
        }
    },
    {
        'title': 'MM_p1w4_vs_p2w2',
        'starting_player': 'player_one',
        'iterations': 1,
        'player_one': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 2
            }
        }
    },
    {
        'title': 'MM_p1w4_vs_1',
        'starting_player': 'player_one',
        'iterations': 1,
        'player_one': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 1
            }
        }
    },
    {
        'title': 'MM_p2w4_vs_p1w4',
        'starting_player': 'player_two',
        'iterations': 1,
        'player_one': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        }
    },
    {
        'title': 'MM_p2w3_vs_p1w4',
        'starting_player': 'player_two',
        'iterations': 1,
        'player_one': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 3
            }
        }
    },
    {
        'title': 'MM_p2w2_vs_p1w4',
        'starting_player': 'player_two',
        'iterations': 1,
        'player_one': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 2
            }
        }
    },
    {
        'title': 'MM_p2w1_vs_p1w4',
        'starting_player': 'player_two',
        'iterations': 1,
        'player_one': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 1
            }
        }
    }
'''



games = [
    {
        'title': 'AZ_vs_p1w1_MM_iter8', # MiniMax with windowLength 1 and iter8 file  vs AlphaZero
        'starting_player': 'player_two',
        'iterations': 5,
        'player_one': {
            'AI': 'alpha-zero',
            'options': {}
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        }
    }   
]


'''
{
        'title': 'p1w4_MM_vs_AZ', # MiniMax with window 4  vs AlphaZero
        'starting_player': 'player_two',
        'iterations': 1,
        'player_one': {
            'AI': 'alpha-zero',
            'options': {}
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        }
    }, 
    {
        'title': 'AZ_vs_p1w4_MM', # MiniMax with window 4  vs AlphaZero
        'starting_player': 'player_one',
        'iterations': 20,
        'player_one': {
            'AI': 'alpha-zero',
            'options': {}
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 4
            }
        }
    },
    {
        'title': 'AZ_vs_p1w3_MM', 
        'starting_player': 'player_one',
        'iterations': 3,
        'player_one': {
            'AI': 'alpha-zero',
            'options': {}
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 3
            }
        }
    },
    {
        'title': 'AZ_vs_p1w2_MM', # MiniMax with window 4  vs AlphaZero
        'starting_player': 'player_one',
        'iterations': 3,
        'player_one': {
            'AI': 'alpha-zero',
            'options': {}
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 2
            }
        }
    },
    {
        'title': 'AZ_vs_p1w1_MM', # MiniMax with window 4  vs AlphaZero
        'starting_player': 'player_one',
        'iterations': 3,
        'player_one': {
            'AI': 'alpha-zero',
            'options': {}
        },
        'player_two': {
            'AI': 'min-max',
            'options': {
                'windowLength': 1
            }
        }
    }
'''



for game in games:
    print("##################################################")
    print('                  Game settings')
    print('Title: ', game['title'])
    print('Starting player: ', game['starting_player'])
    print('Player ONE plays with AI:      ', game['player_one']['AI'], '      and options: ', game['player_one']['options'])
    print('Player TWO plays with AI:      ', game['player_two']['AI'], '      and options: ', game['player_two']['options'])
    print("##################################################")



    stats[game['title']] = {
        'iterations_count': 0,
        'player_one': {
            'won_count': 0,
            'settings': game['player_one']
        },
        'player_two': {
            'won_count': 0,
            'settings': game['player_two']
        },
        'game_ids': []
    }

    for iter in range(1, game['iterations'] + 1):
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
                gameFile = json.loads(sav.read())  # should contains a 6*7 array, the name of the first player and a list of moves
        except FileNotFoundError:  # new game
            tab = [["" for _ in range(7)] for _ in range(6)]  # 6 * 7 array
            first_player = None
            list_of_moves = {}
            gameFile = {}
            gameFile['moves_count'] = 0
            gameFile['player_one_settings'] = game['player_one']
            gameFile['player_two_settings'] = game['player_two']
            gameFile['time_elapsed_player_one'] = 0
            gameFile['time_elapsed_player_two'] = 0
            gameFile["tab"] = tab
            gameFile["first_player"] = game['starting_player']
            gameFile["winner"] = ''
            gameFile["list_of_moves"] = list_of_moves
            with open(ABSOLUTE_SAVE_FOLDER_PATH + game_id + ".json", "w") as sav:
                sav.write(json.dumps(gameFile))
            
        #####################################################################################################
        #  Functions
        #####################################################################################################

        def ai_make_move(game, player, aiName, options):
            try:
                ai = ai_module.AI()
                game["tab"], row, col = ai.play(game["tab"], PLAYER_COLOR[player], aiName, options)
            except aiCantMoveError as e:
                print(e)
            
            return game["tab"], row, col

        #####################################################################################################
        #  Moves
        #####################################################################################################

        someone_won = False
        current_player_name = game['starting_player']

        while(not someone_won):
            print("############################################################################################### Player: ", current_player_name)
            aiOptios = game[current_player_name]['options']
            start = timer()
            gameFile["tab"], row_move, col_move = ai_make_move(
                gameFile,
                current_player_name,
                game[current_player_name]['AI'],
                aiOptios
            )
            end = timer()
            time_elapsed = end - start
            gameFile[('time_elapsed_' + current_player_name)] += time_elapsed
            gameFile['moves_count'] += 1
            gameFile["list_of_moves"][gameFile['moves_count']] = {'row':row_move, 'col': col_move, 'color': PLAYER_COLOR[current_player_name]}

            if victory(gameFile["tab"], row_move, col_move, PLAYER_COLOR[current_player_name]):
                someone_won = True
                gameFile["winner"] = current_player_name
                stats[game['title']][current_player_name]['won_count'] += 1
                
                print("##################################################")
                print('                  Game stats')
                print('Title: ', game['title'])
                print('Starting player: ', game['starting_player'])
                print('Winning player: ', gameFile["winner"])
                print('Moves to win: ', gameFile['moves_count'])
                print('Player ONE plays with AI:      ', game['player_one']['AI'], '      and options: ', game['player_one']['options'])
                print('Player TWO plays with AI:      ', game['player_two']['AI'], '      and options: ', game['player_two']['options'])
                print("##################################################")

                break
            
            current_player_name = 'player_two' if (current_player_name == 'player_one') else 'player_one'
        

        stats[game['title']]['game_ids'].append(game_id)
        stats[game['title']]['iterations_count'] += 1

        with open(ABSOLUTE_SAVE_FOLDER_PATH + game_id + ".json", "w") as sav:
            sav.write(json.dumps(gameFile))
            
        print('#########################################################################')
        print('#########################################################################')
        print('####   Updating the stats file    #######################################')
        print('#########################################################################')
        print('#########################################################################')
        with open(ABSOLUTE_SAVE_FOLDER_PATH + 'run_' + timestr + ".json", "w") as sav:
            sav.write(json.dumps(stats))


#with open(ABSOLUTE_SAVE_FOLDER_PATH + 'run_' + timestr + ".json", "w") as sav:
#        sav.write(json.dumps(stats))