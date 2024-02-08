"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 28, 2022
"""

import random

def is_empty(board):
    counter = 0

    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == " ":
                counter += 1

    if counter == 64:
        return True
    else:
        return False


def is_bounded(board, y_end, x_end, length, d_y, d_x):

    y_before = y_end - length * d_y
    x_before = x_end - length * d_x
    y_after = y_end + d_y
    x_after = x_end + d_x

    before, after = True, True
    if not (0 <= x_before < len(board) and
            0 <= y_before < len(board)):
        before = False
    else:
        if board[y_before][x_before] != " ":
            before = False

    if not (0 <= y_after < len(board) and
            0 <= x_after < len(board)):
        after = False
    else:
        if board[y_after][x_after] != " ":
            after = False

    if board[y_after][x_after] != " ":
        after = False
    if board[y_before][x_before] != " ":
        before = False

    if before and after:
        return "OPEN"
    elif before or after:
        return "SEMIOPEN"
    else:
        return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count = 0, 0
    y = y_start
    x = x_start
    current_length = 0

    while True:
        if not (0 <= y < len(board) and
                0 <= x < len(board)):
            break

        if board[y][x] == col:
            current_length += 1
        else:
            current_length = 0

        if current_length == length:
            bound = is_bounded(board, y, x, length, d_y, d_x)
            if bound == "OPEN":
                open_seq_count += 1
            elif bound == "SEMIOPEN":
                semi_open_seq_count += 1

        y += d_y
        x += d_x

    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
    open_count, semi_count = 0, 0

    for i in range(len(board)):
        detect_row_output = detect_row(board, col, i, 0, length, 0, 1)
        open_count += detect_row_output[0]
        semi_count += detect_row_output[1]

    for j in range(len(board)):
        detect_row_output = detect_row(board, col, 0, j, length, 1, 0)
        open_count += detect_row_output[0]
        semi_count += detect_row_output[1]

    for k in range(len(board) - length - 1):
        detect_row_output = detect_row(board, col, 0, k, length, 1, 1)
        open_count += detect_row_output[0]
        semi_count += detect_row_output[1]

    for l in range(len(board) - length - 1):
        detect_row_output = detect_row(board, col, 0, l, length, 1, -1)
        open_count += detect_row_output[0]
        semi_count += detect_row_output[1]

    for n in range(len(board) - length):
        detect_row_output = detect_row(board, col, n, len(board) - 1, length, 1, -1)
        open_count += detect_row_output[0]
        semi_count += detect_row_output[1]

    return open_count, semi_count

def search_max(board):

    move_y, move_x = 0, 0
    prev_max_score = score(board)


    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == " ":
                board[i][j] = "b"
                cur_score = score(board)
                if cur_score >= prev_max_score:
                    prev_max_score = cur_score
                    move_y = i
                    move_x = j
                board[i][j] = " "

    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4]) +
            500 * open_b[4] +
            50 * semi_open_b[4] +
            -100 * open_w[3] +
            -30 * semi_open_w[3] +
            50 * open_b[3] +
            10 * semi_open_b[3] +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    temp_string = ""

    for c in range(4):
        for r in range(8):
            if board[r][c] == "b" and board[r][c + 1] == "b" and board[r][c + 2] == "b" and board[r][c + 3] == "b" and board[r][c + 4] == "b":
                return "Black won"
            elif board[r][c] == "w" and board[r][c + 1] == "w" and board[r][c + 2] == "w" and board[r][c + 3] == "w" and board[r][c + 4] == "w":
                return "White won"


    for c in range(8):
        for r in range(4):
            if board[r][c] == "b" and board[r + 1][c] == "b" and board[r + 2][c] == "b" and board[r + 3][c] == "b" and board[r + 4][c] == "b":
                return "Black won"
            elif board[r][c] == "w" and board[r + 1][c] == "w" and board[r + 2][c] == "w" and board[r + 3][c] == "w" and board[r + 4][c] == "w":
                return "White won"

    for i in range(4, 8):
        r = 0
        c = i

        while r < len(board()) and c > -1:
            temp_string += board[r][c]
            r += 1
            c -= 1

    for i in range(1, 3):
        r = 7
        c = i

        while r > 0 and c < 8:
            temp_string += board[r][c]
            r -= 1
            c += 1

    if "bbbbb" in temp_string:
        return "Black wins"
    elif "wwwww" in temp_string:
        return "White wins"

    string_two = ""

    for i in range(0, 4):
        r = 0
        c = i

        while r < len(board()) and c > -1:
            string_two += board[r][c]
            r += 1
            c += 1

    for i in range(4, 7):
        r = 4
        c = i

        while r > 0 and c > -1:
            string_two += board[r][c]
            r -= 1
            c -= 1

    if "bbbbb" in string_two:
        return "Black wins"
    elif "wwwww" in string_two:
        return "White wins"

    if is_empty(board) != True:
        return "Draw"

def print_board(board):
    s = "*"
    for i in range(len(board[0]) - 1):
        s += str(i % 10) + "|"
    s += str((len(board[0]) - 1) % 10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i % 10)
        for j in range(len(board[0]) - 1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0]) - 1])

        s += "*\n"
    s += (len(board[0]) * 2 + 1) * "*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "] * sz)
    return board


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


def test_is_bounded():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0, x, length, d_y, d_x) == (1, 0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")


def test_detect_rows():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3;
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col, length) == (1, 0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")


def test_search_max():
    board = make_empty_board(8)
    x = 5;
    y = 0;
    d_x = 0;
    d_y = 1;
    length = 4;
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6;
    y = 0;
    d_x = 0;
    d_y = 1;
    length = 4;
    col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4, 6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")


def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()


def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5;
    x = 2;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3;
    x = 5;
    d_x = -1;
    d_y = 1;
    length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5;
    x = 3;
    d_x = -1;
    d_y = 1;
    length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':
    # play_gomoku(8)
    # board = make_empty_board(8)
    #
    # board[0][5] = "w"
    # board[0][6] = "b"
    # y = 3;
    # x = 5;
    # d_x = -1;
    # d_y = 1;
    # length = 2
    # put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    # print_board(board)
    # analysis(board)
    # test_is_empty()
    # test_is_bounded()
    # test_detect_row()
    # test_detect_rows()
    test_search_max()