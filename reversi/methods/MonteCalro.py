from reversi.Reversi import Reversi, Board
import numpy as np


class MonteCalro:
    def __init__(self, board: Board, player: np.int8, count: int = 100):
        self.__init_board = board
        self.__player = player
        self.__simulate_counts = count

        self.__candidates = board.get_can_place(self.__player)
        self.__wins = np.full(board.board.shape, 0, dtype=np.int8)
        self.__count = count
        self.__result = None

    @property
    def result(self):
        return tuple(self.__result)

    def run(self) -> tuple:
        cnt = np.full(len(self.__candidates), 0, dtype=np.int32)
        for i, pos in enumerate(self.__candidates):
            j = 0
            while j < self.__count:
                result = self.__play(pos)
                if result is None: continue

                if result: cnt[i] += 1
                j += 1
        self.__result = cnt / self.__count
        return self.result

    def __play(self, from_: tuple[int, int]) -> bool | None:
        game = Reversi(self.__init_board, self.__player)
        game.place(from_, self.__player)
        game.next_turn()

        # random play
        game.auto_play()

        wins = game.top_stones()

        if len(wins) > 1: return None  # 引き分け

        if self.__player in wins: return True  # WIN
        else: return False  # LOSE
