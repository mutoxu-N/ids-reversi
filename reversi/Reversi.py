import numpy as np
from enum import Enum
import sys


class Board:
    """
    盤面の情報
    """

    def __init__(self, board: np.ndarray, stone_size_=None):
        """

        Args:
            board: 盤面の配列 (正方形)

        """

        # size check
        s = board.shape
        if s[0] != s[1]:
            assert f"盤面が正方形ではありません。 size: {s}"
        self.__size = s[0]
        self.__board = board.astype(np.int8)
        self.__STONE_SIZE = int(stone_size_ if stone_size_ else np.max(self.__board))

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

    @property
    def stone_size(self) -> int:
        """

        Returns:　石の種類数を取得

        """
        return self.__STONE_SIZE

    def print(self, stone: int = 0) -> None:
        """

        Args:
            stone: stone がおける場所を赤く表示 (0 で非表示, stone >= 9 で正常に動作しない)

        """

        if self.__STONE_SIZE > 8:
            print("石の種類が9種類以上だと出力できません。")
            return

        board: np.ndarray = self.__board
        c = self.get_can_place(stone)

        stones = ["🟩", "⚫", "⚪", "🔵", "🟡", "🟠", "🟣", "🟤", "🟢"]
        r = "" if stone == 0 else f"put: {stone}\n"
        for y in range(self.size):
            for x in range(self.size):
                if stone != 0 and (x, y) in c:
                    r += "🔴"
                else:
                    r += stones[board[y][x]]
            r += "\n"
        print(r, end="")

    def count(self, stone: int):
        """

        Args:
            stone: 石の種類

        Returns: 現在の石の数

        """
        return np.count_nonzero(self.board == stone)

    def get_can_place(self, stone: int = 0) -> tuple[tuple[int, int], ...]:
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


def default_board() -> Board:
    """

    Returns: デフォルトの盤面配列

    """
    board: np.ndarray = np.zeros((8, 8), dtype=np.int8)
    board[3][3] = 2
    board[3][4] = 1
    board[4][3] = 1
    board[4][4] = 2

    return Board(board)


class Reversi:
    """
    リバーシ用インターフェース
    1ゲームを管理
    """

    class State(Enum):
        IN_GAME = 0
        FINISHED = 1

    def __init__(self, board: Board = default_board(), player: np.int8 = None):
        """

        Args:
            board: 初期の盤面

        """

        # init
        self.__SIZE = board.size
        self.__board_histories = []
        self.__playing = 1 if player is None else player
        self.__STONE_SIZE = board.stone_size
        self.__state: Reversi.State = Reversi.State.IN_GAME

        # whether place failed
        self.__place_failed = np.full(self.__STONE_SIZE, False)

        # create new game
        self.__board_histories.append(board)

    @property
    def now_board(self) -> Board:
        """

        Returns: 現在の盤面を取得

        """
        return self.__board_histories[-1]

    @property
    def state(self) -> State:
        """

        Returns: ゲームの現在の状態

        """
        return self.__state

    @property
    def turns(self) -> int:
        """

        Returns: スタートから何手進んだのか

        """
        return len(self.__board_histories)

    @property
    def playing(self) -> np.int8:
        """

        Returns: 現在のターンの石の種類を返す

        """
        return self.__playing

    def get_board(self, num: int = -1) -> Board:
        """

        Args:
            num: 取得する盤面のインデックス

        Returns: num番目の盤面

        """
        return self.__board_histories[num]

    def get_can_place(self, stone: int = 0) -> tuple[tuple[int, int], ...]:
        """

        Args:
            stone: 設置する石の番号

        Returns:現在の盤面で設置できる座標群 例: ( (0, 0), (0, 1) )

        """
        t = self.now_board.get_can_place(stone)

        if len(t) == 0:
            self.__place_failed[stone-1] = True

        if np.count_nonzero(self.__place_failed) == self.__STONE_SIZE:
            self.__state = Reversi.State.FINISHED

        return t

    def print(self, stone: int = 0, num: int = -1) -> None:
        """

        Args:
            stone: stone がおける場所を赤く表示 (0 で非表示)
            num: 何番目の盤面を print するか

        """
        self.__board_histories[num].print(stone)

    def place(self, pos: tuple[int, int], stone: np.int8) -> None:
        """

        Args:
            pos: 設置する位置 (x, y)
            stone: 設置する石の種類

        """
        x, y = pos
        f, l = self.now_board.get_reverses(stone, x, y)

        # ゲーム中ではなかったら終了
        if self.state != Reversi.State.IN_GAME:
            return

        # 設置できないときは終了
        if not f:
            print(f"Place failed (stone={stone}, (x, y) = ({x}, {y}))", file=sys.stderr)
            sys.exit(1)

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

        new_board = Board(b, self.__STONE_SIZE)
        self.__board_histories.append(new_board)
        self.__place_failed = np.full(self.__STONE_SIZE, False)

    def count(self, stone: int, num: int = -1) -> int:
        """

        Args:
            stone: 石の種類
            num: 盤面のインデックス

        Returns: numの石の数

        """
        return self.get_board(num).count(stone)

    def count_all(self, num: int = -1) -> tuple[int, ...]:
        """

        Args:
            num: 盤面のインデックス

        Returns: それぞれの石の数

        """
        r = []
        board: Board = self.get_board(num)
        for i in range(self.__STONE_SIZE+1):
            r.append(board.count(i))
        return tuple(r)

    def next_turn(self) -> int:
        """
        次のターンに進める

        Returns: 現在の石の種類

        """
        self.__playing += 1
        if self.__playing > self.__STONE_SIZE: self.__playing = 1
        return self.__playing

    def top_stones(self) -> tuple[int, ...]:
        """

        Returns: 一番数が多い石の種類

        """
        r = []
        t = self.count_all()
        m = max(t[1:])
        for i, c in enumerate(t):
            if m == c: r.append(i)
        return tuple(r)

    def auto_play(self) -> tuple[int, ...]:
        """
        現在の状態から終了までランダムプレイ

        Returns: 勝利した石の種類

        """
        while self.state == Reversi.State.IN_GAME:

            # 置ける場所の候補
            candidates = self.get_can_place(self.playing)

            if len(candidates) > 0:
                p = candidates[np.random.randint(len(candidates), size=1)[0]]
                self.place((p[0], p[1]), self.playing)

            self.next_turn()

        return self.top_stones()
