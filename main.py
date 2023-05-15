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


def main_3():
    np.random.seed(30)

    b = default_board()
    r = Reversi(Board(b))

    black_pass = False
    white_pass = False
    stone = 1
    cnt = 0
    # r.print(stone)

    while not (black_pass and white_pass):

        candidate = r.get_can_place(stone)
        # print(f"placeable: {candidate}")

        if len(candidate) == 0:
            if stone == 1: black_pass = True
            else: white_pass = True

        else:
            p = candidate[np.random.randint(len(candidate), size=1)[0]]
            # print(f"place: {stone} at {p}")

            r.place(stone, p[0], p[1])

        if stone == 1: stone = 2
        else: stone = 1
        # r.print(stone)

    for i in range(r.turns):
        r.print(num=i)

    print(f"黒: {r.count(1)}, 白: {r.count(2)}")


if __name__ == '__main__':
    main_3()
