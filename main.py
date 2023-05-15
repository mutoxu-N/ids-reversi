from reversi import Reversi, Board, default_board
import numpy as np


def main_1():
    b = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 2, 2, 1, 0, 0],
        [0, 0, 2, 1, 1, 2, 0, 0],
        [0, 0, 1, 1, 1, 2, 0, 0],
        [0, 0, 2, 2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ])

    r = Reversi(Board(b))
    r.print(1)
    print(r.now_board.get_stone_position(1))
    print(r.now_board.get_reverses(1, 2, 6))
    r.place(1, 2, 6)
    r.print(1)
    print(r.now_board.get_stone_position(1))


def main_2():
    np.random.seed(20)

    b = default_board()
    r = Reversi(Board(b))

    # black
    stone = 1
    r.print(stone)
    candidate = r.get_can_place(stone)
    print(candidate)

    idx = np.random.randint(len(candidate), size=1)[0]
    print(idx)

    p = candidate[idx]
    print(p)

    r.place(stone, p[0], p[1])

    # white
    stone = 2
    r.print(stone)
    candidate = r.get_can_place(stone)
    print(candidate)

    idx = np.random.randint(len(candidate), size=1)[0]
    print(idx)

    p = candidate[idx]
    print(p)

    r.place(stone, p[0], p[1])

    r.print(0)


if __name__ == '__main__':
    main_2()
