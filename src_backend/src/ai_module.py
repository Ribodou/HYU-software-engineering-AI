from errors import aiCantMoveError
from game_logic_functions import is_move_valid
import alpha_zero
import min_max

class AI:
    def __init__(self):
        pass

    def __str__(self):
        return repr(self)
    
    def play(self, inJeu, color, difficulty="random"):
        print(color, 'is playing with difficulty ', difficulty)
        if difficulty == "random":
            return self.play_random(inJeu, color)
        elif difficulty == "min-max":
            return self.play_minmax(inJeu, color)
        elif difficulty == "alpha-zero":
            return self.play_alpha_zero(inJeu, color)
        else:
            print("**Difficulty unknown, please change it. Playing random instead...**")
            return self.play_random(inJeu, color)
            
    def play_random(self, inJeu,color):
        """
            Play for ai or raise aiCantMoveError if the ai con't play.
        """
        for i in range(7):  # column
            for j in range(6): # line
                if is_move_valid(inJeu, j, i):
                    inJeu[j][i] = color
                    print("I, the ai, play", j, i)
                    return inJeu, j, i
        raise aiCantMoveError("the ai can't move")
    
    def play_minmax(self, inJeu,color):
        inJeu2 = inJeu.copy()
        try:
            row,col = min_max.play_ia(inJeu)
            inJeu[row][col] = color
            print("I, the ai, play", row, col)
            return inJeu, row, col
        except aiCantMoveError:
            return self.play_random(inJeu2, color)

    def play_alpha_zero(self, inJeu, color):
        pass  # TODO

