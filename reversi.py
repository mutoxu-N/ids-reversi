import numpy as np
from enum import Enum


def default_board() -> np.ndarray:
    """

    Returns: デフォルトの盤面配列

    """
    board: np.ndarray = np.zeros((8, 8))
    board[3][3] = 2
    board[3][4] = 1
    board[4][3] = 1
    board[4][4] = 2

    return board


class Board:
    """
    盤面の情報
    """

    def __init__(self, board: np.ndarray):
        """

        Args:
            board: 盤面の配列 (正方形)

        """

        # size check
        s = board.shape
        if s[0] != s[1]:
            assert f"盤面が正方形ではありません。 size: {s}"
        self.__size = s[0]
        self.__board = board.copy()

    def __str__(self) -> str:
        r = ""
        for i in self.board:
            r += str(i) + "\n"
        return r

    @property
    def size(self) -> int:
        """

        Returns: 盤面の一辺の大きさ

        """
        return self.__size

    @property
    def board(self) -> np.ndarray:
        """

        Returns: 盤面の状態の配列

        """
        return self.__board.copy()

    def print(self, stone: int = 0) -> None:
        """

        Args:
            stone: stone がおける場所を赤く表示 (0 で非表示)

        """
        board: np.ndarray = self.__board
        c = self.get_can_place(stone)

        r = ""
        for y in range(self.size):
            for x in range(self.size):
                if stone != 0 and (x, y) in c:
                    r += "🔴"
                else:
                    if board[y][x] == 1:
                        r += "⚫"
                    elif board[y][x] == 2:
                        r += "⚪"
                    else:
                        r += "🟩"
            r += "\n"
        print(r)

    def count(self, stone: int):
        """

        Args:
            stone: 石の種類

        Returns: 現在の石の数

        """
        return np.count_nonzero(self.board == stone)

    def get_can_place(self, stone: int = 0) -> tuple:
        """

        Args:
            stone: 設置する石の番号

        Returns:現在の盤面で設置できる座標群 例: ( (0, 0), (0, 1) )

        """
        # 石が指定されなかったら終了
        if stone == 0: return ()

        t = []
        for y in range(self.size):
            for x in range(self.size):
                f = False
                for d in range(8):
                    if self.__check_can_place(stone, x, y, d) > 0:
                        f = True
                        break

                if f: t.append((x, y))

        return tuple(t)

    def get_reverses(self, stone: int, x: int, y: int) -> (bool, np.array):
        """

        Args:
            stone: 設置する石
            x: X座標
            y: Y座標

        Returns: (設置できるか, 方向毎に何ます設置するか)

        """
        t = np.empty(8, dtype=np.uint8)
        f = False
        for d in range(8):
            t[d] = self.__check_can_place(stone, x, y, d)
            if t[d] > 0: f = True

        return f, t

    def __check_can_place(self, stone: int, x: int, y: int, direction: int) -> int:
        """

        Args:
            stone: 設置される石の番号
            x: x座標
            y: y座標
            direction:  0:N, 1:NE, 2:E, 3:SE, 4:S, 5:SW, 6:W, 7:NW を表す。

        Returns: (x, y) に dir の方向 何マス設置できるか

        """
        board = self.__board

        # 石が置いてあったらおけない
        if board[y][x] != 0: return 0

        # N
        if direction == 0:
            if y < 2 or board[y - 1][x] in (0, stone): return 0

            i, j = x, y - 2
            while j >= 0:
                if board[j][i] not in (0, stone):
                    j -= 1
                else:
                    break

            if j < 0 or board[j][i] == 0: return 0
            return y - j

        # NE
        elif direction == 1:
            if self.size - 3 < x or y < 2 or board[y - 1][x + 1] in (0, stone): return 0

            i, j = x + 2, y - 2
            while i < self.size and j >= 0:
                if board[j][i] not in (0, stone):
                    i += 1
                    j -= 1
                else:
                    break

            if self.size <= i or j < 0 or board[j][i] == 0: return 0
            return i - x

        # E
        elif direction == 2:
            if self.size - 3 < x or board[y][x + 1] in (0, stone): return 0

            i, j = x + 1, y
            while i < self.size:
                if board[j][i] not in (0, stone):
                    i += 1
                else:
                    break

            if self.size <= i or board[j][i] == 0: return 0
            return i - x

        # SE
        elif direction == 3:
            if self.size - 3 < x or self.size - 3 < y or board[y + 1][x + 1] in (0, stone): return 0

            i, j = x + 2, y + 2
            while i < self.size and j < self.size:
                if board[j][i] not in (0, stone):
                    i += 1
                    j += 1
                else:
                    break

            if self.size <= i or self.size <= j or board[j][i] == 0: return 0
            return i - x

        # S
        if direction == 4:
            if self.size - 3 < y or board[y + 1][x] in (0, stone): return 0

            i, j = x, y + 2
            while j < self.size:
                if board[j][i] not in (0, stone):
                    j += 1
                else:
                    break

            if self.size <= j or board[j][i] == 0: return 0
            return j - y

        # SW
        elif direction == 5:
            if x < 2 or self.size - 3 < y or board[y + 1][x - 1] in (0, stone): return 0

            i, j = x - 2, y + 2
            while 0 <= i and j < self.size:
                if board[j][i] not in (0, stone):
                    i -= 1
                    j += 1
                else:
                    break

            if i < 0 or self.size <= j or board[j][i] == 0: return 0
            return x - i

        # W
        if direction == 6:
            if x < 2 or board[y][x - 1] in (0, stone): return 0

            i, j = x - 2, y
            while i >= 0:
                if board[j][i] not in (0, stone):
                    i -= 1
                else:
                    break

            if i < 0 or board[j][i] == 0: return 0
            return x - i

        # NW
        elif direction == 7:
            if x < 2 or y < 2 or board[y - 1][x - 1] in (0, stone): return 0

            i, j = x - 2, y - 2
            while 0 <= i and 0 <= j:
                if board[j][i] not in (0, stone):
                    i -= 1
                    j -= 1
                else:
                    break

            if i < 0 or j < 0 or board[j][i] == 0: return 0
            return x - i

        return 0

    def get_stone_position(self, stone) -> np.ndarray:
        """

        Args:
            stone: 石の種類

        Returns: 指定された石がある場所を1, それ以外を0とする配列
        """
        r = np.zeros(self.__board.shape)
        for y in range(self.size):
            for x in range(self.size):
                if self.__board[y][x] == stone:
                    r[y][x] = 1
        return r

    def top_stone(self) -> int:
        """

        Returns: 一番数が多い石の種類

        """
        if self.count(1) < self.count(2): return 2
        else: return 1


class Reversi:
    """
    リバーシ用インターフェース
    1ゲームを管理
    """

    class State(Enum):
        IN_GAME = 0
        FINISHED = 1

    def __init__(self, board: Board = default_board()):
        """

        Args:
            board: 初期の盤面

        """

        self.SIZE = board.size
        self.__board_histories = []
        self.playing = 1
        self.state: Reversi.State = Reversi.State.IN_GAME

        # create new game
        self.__board_histories.append(board)

    @property
    def now_board(self) -> Board:
        """

        Returns: 現在の盤面を取得

        """
        return self.__board_histories[-1]

    @property
    def turns(self) -> int:
        """

        Returns: スタートから何手進んだのか

        """
        return len(self.__board_histories)

    def get_board(self, num: int = -1) -> Board:
        """

        Args:
            num: 取得する盤面のインデックス

        Returns: num番目の盤面

        """
        return self.__board_histories[num]

    def get_can_place(self, stone: int = 0) -> tuple:
        """

        Args:
            stone: 設置する石の番号

        Returns:現在の盤面で設置できる座標群 例: ( (0, 0), (0, 1) )

        """
        return self.now_board.get_can_place(stone)

    def print(self, stone: int = 0, num: int = -1) -> None:
        """

        Args:
            stone: stone がおける場所を赤く表示 (0 で非表示)
            num: 何番目の盤面を print するか

        """
        self.__board_histories[num].print(stone)

    def place(self, stone, x, y) -> None:
        """

        Args:
            stone: 設置する石の種類
            x: X座標
            y: Y座標

        """
        f, l = self.now_board.get_reverses(stone, x, y)

        # ゲーム中ではなかったら終了
        if self.state != Reversi.State.IN_GAME:
            return

        # 設置できないときは終了
        if not f:
            print(f"place failed! (stone={stone}, (x, y) = ({x}, {y}))")
            return

        b: np.ndarray = self.now_board.board

        b[y][x] = stone
        for i in range(1, l[0]):  # N
            b[y - i][x] = stone
        for i in range(1, l[1]):  # NE
            b[y - i][x + i] = stone
        for i in range(1, l[2]):  # E
            b[y][x + i] = stone
        for i in range(1, l[3]):  # SE
            b[y + i][x + i] = stone
        for i in range(1, l[4]):  # S
            b[y + i][x] = stone
        for i in range(1, l[5]):  # SW
            b[y + i][x - i] = stone
        for i in range(1, l[6]):  # W
            b[y][x - i] = stone
        for i in range(1, l[7]):  # NW
            b[y - i][x - i] = stone

        new_board = Board(b)
        self.__board_histories.append(new_board)

        # 空いているますがなかったら終了
        if self.count(0) == 0: self.state = Reversi.State.FINISHED

    def count(self, stone: int, num: int = -1) -> int:
        """

        Args:
            stone: 石の種類
            num: 盤面のインデックス

        Returns: numの石の数

        """
        return self.get_board(num).count(stone)

    def result(self) -> tuple:
        """

        Returns: 対戦結果 (ゲームが終了したか, 勝った石)

        """
        if self.state != Reversi.State.FINISHED: return False, None

        return True,
