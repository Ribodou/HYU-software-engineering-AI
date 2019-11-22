from errors import aiCantMoveError
from game_logic_functions import is_move_valid


class AI:
    def __init__(self):
        pass

    def __str__(self):
        return repr(self)
    
    def play(self, inJeu,color):
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
