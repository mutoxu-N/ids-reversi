from reversi.Reversi import Reversi, Board
import numpy as np

class MonteCalro:
    def __init__(self, board: Board, player: np.int8):
        self.__game = Reversi(board)
        self.__player = player

    def play(self):
        while self.__game.state == Reversi.State.IN_GAME:

            pass
