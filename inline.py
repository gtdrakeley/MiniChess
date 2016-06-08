from move import Move
from history import History
from typing import List, Tuple
from time import time

import random

# **************************************************  CONSTANTS  *******************************************************
white_pieces = 'KQBNRP'
black_pieces = 'kqbnrp'
"""
piece_position_values = {'K': [[20000, 20000, 20000, 20000, 20000],
                               [20000, 20000, 20000, 20000, 20000],
                               [20000, 20000, 20000, 20000, 20000],
                               [20000, 20000, 20000, 20000, 20000],
                               [20000, 20000, 20000, 20000, 20000],
                               [20000, 20000, 20000, 20000, 20000]],
                         'Q': [[2000, 2000, 2000, 2000, 2000],
                               [2000, 2000, 2000, 2000, 2000],
                               [2000, 2000, 2000, 2000, 2000],
                               [2000, 2000, 2000, 2000, 2000],
                               [2000, 2000, 2000, 2000, 2000],
                               [2000, 2000, 2000, 2000, 2000]],
                         'B': [[500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500]],
                         'N': [[300, 300, 300, 300, 300],
                               [300, 300, 300, 300, 300],
                               [300, 300, 300, 300, 300],
                               [300, 300, 300, 300, 300],
                               [300, 300, 300, 300, 300],
                               [300, 300, 300, 300, 300]],
                         'R': [[500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500]],
                         'P': [[100, 100, 100, 100, 100],
                               [100, 100, 100, 100, 100],
                               [100, 100, 100, 100, 100],
                               [100, 100, 100, 100, 100],
                               [100, 100, 100, 100, 100],
                               [100, 100, 100, 100, 100]],
                         '.': [[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0]]}
"""
piece_position_values = {'K': [[20000, 20000, 20000, 20000, 20000],
                               [20000, 20000, 20000, 20000, 20000],
                               [20000, 20000, 20000, 20000, 20000],
                               [20000, 20000, 20000, 20000, 20000],
                               [20000, 20000, 20000, 20000, 20000],
                               [20000, 20000, 20000, 20000, 20000]],
                         'Q': [[2000, 2000, 2000, 2000, 2000],
                               [2000, 2000, 2000, 2000, 2000],
                               [2000, 2000, 2000, 2000, 2000],
                               [2000, 2000, 2000, 2000, 2000],
                               [2000, 2000, 2000, 2000, 2000],
                               [2000, 2000, 2000, 2000, 2000]],
                         'B': [[500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500]],
                         'N': [[300, 300, 300, 300, 300],
                               [300, 300, 300, 300, 300],
                               [300, 300, 300, 300, 300],
                               [300, 300, 300, 300, 300],
                               [300, 300, 300, 300, 300],
                               [300, 300, 300, 300, 300]],
                         'R': [[500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500],
                               [500, 500, 500, 500, 500]],
                         'P': [[0, 0, 0, 0, 0],
                               [1000, 1000, 1000, 1000, 1000],
                               [100, 350, 600, 350, 100],
                               [50, 200, 400, 200, 50],
                               [20, 50, 10, 50, 20],
                               [0, 0, 0, 0, 0]],
                         '.': [[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0]]}
piece_position_values['k'] = piece_position_values['K']
piece_position_values['q'] = piece_position_values['Q']
piece_position_values['b'] = piece_position_values['B']
piece_position_values['n'] = piece_position_values['N']
piece_position_values['r'] = piece_position_values['R']
piece_position_values['p'] = piece_position_values['P']
eval_bound = (max(map(max, piece_position_values['K'])) +
              max(map(max, piece_position_values['Q'])) * 6 +
              max(map(max, piece_position_values['B'])) +
              max(map(max, piece_position_values['N'])) +
              max(map(max, piece_position_values['R'])) + 1)

# ***************************************************  GLOBALS  ********************************************************
turn = 1  # type: int
playing = 'W'  # type: str
board = list([list('kqbnr'),  # type: List[List[str]]
              list('ppppp'),
              list('.....'),
              list('.....'),
              list('PPPPP'),
              list('RNBQK')])
white_score = 0
black_score = 0
board_history = list()  # type: List[History]
eval_history = list()  # type: List[Tuple[int, int]]
goal_depth = 0
recur_calls = 0
start_time = 0

# ***************************************************  FUNCTIONS  ******************************************************


def initialize():
    evaluate_board()


def reset() -> None:
    global turn, playing, board, goal_depth, recur_calls, start_time
    turn = 1
    playing = 'W'
    board = list([list('kqbnr'),
                  list('ppppp'),
                  list('.....'),
                  list('.....'),
                  list('PPPPP'),
                  list('RNBQK')])
    goal_depth = 0
    recur_calls = 0
    start_time = 0
    evaluate_board()


def get_board() -> str:
    global turn, playing, board
    return '{} {}\n{}\n'.format(turn, playing, '\n'.join(map(''.join, board)))


def set_board(string: str) -> None:
    global turn, playing, board
    turn_state, *board_state = string.split('\n')
    turn, playing = turn_state.split()
    turn, playing = int(turn), playing
    board = list(map(list, filter(None, board_state)))
    evaluate_board()


def winner() -> str:
    global turn, board
    cat_board = ''.join(map(''.join, board))
    if 'K' in cat_board and 'k' not in cat_board:
        return 'W'
    elif 'K' not in cat_board and 'k' in cat_board:
        return 'B'
    elif turn > 40:
        return '='
    else:
        return '?'


def evaluation() -> int:
    global playing, white_score, black_score
    return white_score - black_score if playing == 'W' else black_score - white_score


def evaluate_board() -> None:
    global board, piece_position_values, white_score, black_score
    white_score, black_score = 0, 0
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece in white_pieces:
                white_score += piece_position_values[piece][r][c]
            elif piece in black_pieces:
                black_score += piece_position_values[piece][5 - r][c]


def move(mv: Move) -> None:
    global turn, playing, board, white_score, black_score, piece_position_values, white_pieces, black_pieces
    # Save board state
    board_history.append(History(board, mv))
    eval_history.append((white_score, black_score))
    # Begin updating evaluation
    src_piece = board[mv.src_row][mv.src_column]
    dest_piece = board[mv.dest_row][mv.dest_column]
    if src_piece in white_pieces:
        white_score -= piece_position_values[src_piece][mv.src_row][mv.src_column]
        black_score -= piece_position_values[dest_piece][5-mv.dest_row][4-mv.dest_column]
    else:
        white_score -= piece_position_values[dest_piece][mv.dest_row][mv.dest_column]
        black_score -= piece_position_values[src_piece][5-mv.src_row][4-mv.src_column]
    # Perform the move
    if playing == 'W':
        playing = 'B'
    else:
        playing = 'W'
        turn += 1
    src_piece = board[mv.src_row][mv.src_column]
    board[mv.src_row][mv.src_column] = '.'
    if src_piece == 'P' and mv.dest_row == 0:
        board[mv.dest_row][mv.dest_column] = 'Q'
    elif src_piece == 'p' and mv.dest_row == 5:
        board[mv.dest_row][mv.dest_column] = 'q'
    else:
        board[mv.dest_row][mv.dest_column] = src_piece
    # End updating evaluation
    src_piece = board[mv.dest_row][mv.dest_column]
    if src_piece in white_pieces:
        white_score += piece_position_values[src_piece][mv.dest_row][mv.dest_column]
    else:
        black_score += piece_position_values[src_piece][5-mv.dest_row][4-mv.dest_column]


def undo() -> None:
    global turn, playing, board, board_history, eval_history, white_score, black_score
    assert board_history, 'Attempted to undo with empty board history'
    assert eval_history, 'Attempted to undo with empty eval history'
    hist = board_history.pop()
    white_score, black_score = eval_history.pop()
    if playing == 'W':
        playing = 'B'
        turn -= 1
    else:
        playing = 'W'
    board[hist.src_row][hist.src_column] = hist.src_piece
    board[hist.dest_row][hist.dest_column] = hist.dest_piece


def is_valid(int_r: int, int_c: int) -> bool:
    if 0 <= int_c <= 4 and 0 <= int_r <= 5:
        return True
    else:
        return False


def is_nothing(piece: str) -> bool:
    return True if piece == '.' else False


def is_enemy(piece: str) -> bool:
    global playing, white_pieces, black_pieces
    if playing == 'W' and piece in black_pieces:
        return True
    elif playing == 'B' and piece in white_pieces:
        return True
    else:
        return False


def is_own(piece: str) -> bool:
    global playing, white_pieces, black_pieces
    if playing == 'W' and piece in white_pieces:
        return True
    elif playing == 'B' and piece in black_pieces:
        return True
    else:
        return False


def piece_moves(piece: str, r: int, c: int) -> List[Move]:
    mvs = list()
    if piece == 'K' or piece == 'k':
        mvs.extend(axis_moves(r, c, 1))
        mvs.extend(diagonal_moves(r, c, 1))
    elif piece == 'Q' or piece == 'q':
        mvs.extend(axis_moves(r, c))
        mvs.extend(diagonal_moves(r, c))
    elif piece == 'R' or piece == 'r':
        mvs.extend(axis_moves(r, c))
    elif piece == 'B' or piece == 'b':
        mvs.extend(diagonal_moves(r, c))
        mvs.extend(bishop_moves(r, c))
    elif piece == 'N' or piece == 'n':
        mvs.extend(knight_moves(r, c))
    elif piece == 'P' or piece == 'p':
        mvs.extend(pawn_moves(r, c))
    return mvs


def axis_moves(r: int, c: int, max_dist=5) -> List[Move]:
    global board
    mvs = list()
    ublocked = dblocked = lblocked = rblocked = False
    for offset in range(1, max_dist + 1):
        if not ublocked and is_valid(r - offset, c) and not is_own(board[r - offset][c]):
            mvs.append(Move(r, c, r - offset, c))
            if is_enemy(board[r - offset][c]):
                ublocked = True
        else:
            ublocked = True
        if not dblocked and is_valid(r + offset, c) and not is_own(board[r + offset][c]):
            mvs.append(Move(r, c, r + offset, c))
            if is_enemy(board[r + offset][c]):
                dblocked = True
        else:
            dblocked = True
        if not lblocked and is_valid(r, c - offset) and not is_own(board[r][c - offset]):
            mvs.append(Move(r, c, r, c - offset))
            if is_enemy(board[r][c - offset]):
                lblocked = True
        else:
            lblocked = True
        if not rblocked and is_valid(r, c + offset) and not is_own(board[r][c + offset]):
            mvs.append(Move(r, c, r, c + offset))
            if is_enemy(board[r][c + offset]):
                rblocked = True
        else:
            rblocked = True
    return mvs


def diagonal_moves(r: int, c: int, max_dist=5) -> List[Move]:
    global board
    mvs = list()
    ulblocked = urblocked = dlblocked = drblocked = False
    for offset in range(1, max_dist + 1):
        if not ulblocked and is_valid(r - offset, c - offset) and \
                not is_own(board[r - offset][c - offset]):
            mvs.append(Move(r, c, r - offset, c - offset))
            if is_enemy(board[r - offset][c - offset]):
                ulblocked = True
        else:
            ulblocked = True
        if not urblocked and is_valid(r - offset, c + offset) and \
                not is_own(board[r - offset][c + offset]):
            mvs.append(Move(r, c, r - offset, c + offset))
            if is_enemy(board[r - offset][c + offset]):
                urblocked = True
        else:
            urblocked = True
        if not dlblocked and is_valid(r + offset, c - offset) and \
                not is_own(board[r + offset][c - offset]):
            mvs.append(Move(r, c, r + offset, c - offset))
            if is_enemy(board[r + offset][c - offset]):
                dlblocked = True
        else:
            dlblocked = True
        if not drblocked and is_valid(r + offset, c + offset) and \
                not is_own(board[r + offset][c + offset]):
            mvs.append(Move(r, c, r + offset, c + offset))
            if is_enemy(board[r + offset][c + offset]):
                drblocked = True
        else:
            drblocked = True
    return mvs


def bishop_moves(r: int, c: int) -> List[Move]:
    global board
    mvs = list()
    if is_valid(r - 1, c) and is_nothing(board[r - 1][c]):
        mvs.append(Move(r, c, r - 1, c))
    if is_valid(r + 1, c) and is_nothing(board[r + 1][c]):
        mvs.append(Move(r, c, r + 1, c))
    if is_valid(r, c - 1) and is_nothing(board[r][c - 1]):
        mvs.append(Move(r, c, r, c - 1))
    if is_valid(r, c + 1) and is_nothing(board[r][c + 1]):
        mvs.append(Move(r, c, r, c + 1))
    return mvs


def knight_moves(r: int, c: int) -> List[Move]:
    global board
    mvs = list()
    if is_valid(r - 2, c - 1) and not is_own(board[r - 2][c - 1]):
        mvs.append(Move(r, c, r - 2, c - 1))
    if is_valid(r - 2, c + 1) and not is_own(board[r - 2][c + 1]):
        mvs.append(Move(r, c, r - 2, c + 1))
    if is_valid(r + 2, c - 1) and not is_own(board[r + 2][c - 1]):
        mvs.append(Move(r, c, r + 2, c - 1))
    if is_valid(r + 2, c + 1) and not is_own(board[r + 2][c + 1]):
        mvs.append(Move(r, c, r + 2, c + 1))
    if is_valid(r - 1, c - 2) and not is_own(board[r - 1][c - 2]):
        mvs.append(Move(r, c, r - 1, c - 2))
    if is_valid(r + 1, c - 2) and not is_own(board[r + 1][c - 2]):
        mvs.append(Move(r, c, r + 1, c - 2))
    if is_valid(r - 1, c + 2) and not is_own(board[r - 1][c + 2]):
        mvs.append(Move(r, c, r - 1, c + 2))
    if is_valid(r + 1, c + 2) and not is_own(board[r + 1][c + 2]):
        mvs.append(Move(r, c, r + 1, c + 2))
    return mvs


def pawn_moves(r: int, c: int) -> List[Move]:
    global board
    mvs = list()
    if playing == 'W':
        if is_valid(r - 1, c) and is_nothing(board[r - 1][c]):
            mvs.append(Move(r, c, r - 1, c))
        if is_valid(r - 1, c - 1) and is_enemy(board[r - 1][c - 1]):
            mvs.append(Move(r, c, r - 1, c - 1))
        if is_valid(r - 1, c + 1) and is_enemy(board[r - 1][c + 1]):
            mvs.append(Move(r, c, r - 1, c + 1))
    else:
        if is_valid(r + 1, c) and is_nothing(board[r + 1][c]):
            mvs.append(Move(r, c, r + 1, c))
        if is_valid(r + 1, c - 1) and is_enemy(board[r + 1][c - 1]):
            mvs.append(Move(r, c, r + 1, c - 1))
        if is_valid(r + 1, c + 1) and is_enemy(board[r + 1][c + 1]):
            mvs.append(Move(r, c, r + 1, c + 1))
    return mvs


def moves() -> List[Move]:
    global playing, board, white_pieces, black_pieces
    mvs = list()
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece == '.':
                continue
            elif playing == 'W' and piece in white_pieces:
                mvs.extend(piece_moves(piece, r, c))
            elif playing == 'B' and piece in black_pieces:
                mvs.extend(piece_moves(piece, r, c))
    return mvs


def moves_shuffled() -> List[Move]:
    mvs = moves()
    random.shuffle(mvs)
    return mvs


def moves_evaluated() -> List[Move]:
    mvs = moves_shuffled()
    evals = list()  # type: List[int]
    for mv in mvs:
        move(mv)
        evals.append(evaluation())
        undo()
    zipped = list(zip(evals, mvs))
    zipped.sort(key=lambda e: e[0])
    evals, mvs = zip(*tuple(zipped))
    return list(mvs)


def move_random() -> str:
    mv = moves_shuffled()[0]
    move(mv)
    return str(mv)


def move_greedy() -> str:
    mv = moves_evaluated()[0]
    move(mv)
    return str(mv)


def move_negamax(depth: int, duration: int) -> str:
    global eval_bound
    best = None
    score = -eval_bound
    for mv in moves_shuffled():
        move(mv)
        temp = -negamax(depth-1, duration)
        undo()
        if temp > score:
            best = mv
            score = temp
    move(best)
    return str(best)


def negamax(depth: int, duration: int) -> int:
    global eval_bound
    if depth == 0 or winner() != '?':
        return evaluation()
    score = -eval_bound
    for mv in moves_shuffled():
        move(mv)
        score = max(score, -negamax(depth-1, duration))
        undo()
    return score


def move_alphabeta(depth, duration) -> str:
    global turn, eval_bound, goal_depth, recur_calls, start_time
    best = None
    alpha = -eval_bound
    beta = eval_bound
    if depth < 0:
        temp_mv = None
        iter_depth = 2
        move_duration = (duration - 1500) / (41 - turn)
        start_time = milliseconds()
        try:
            while True:
                goal_depth = iter_depth
                for mv in moves_evaluated():
                    move(mv)
                    temp = -alphabeta(iter_depth-1, move_duration, -beta, -alpha)
                    undo()
                    if temp > alpha:
                        temp_mv = mv
                        alpha = temp
                best = temp_mv
                iter_depth += 1
                if iter_depth > 64:
                    raise TimeoutError(iter_depth)
        except TimeoutError as e:
            print(iter_depth-1)
            print(move_duration)
            for _ in range(iter_depth-e.args[0]):
                undo()
    else:
        for mv in moves_evaluated():
            move(mv)
            temp = -alphabeta(depth-1, duration, -beta, -alpha)
            undo()
            if temp > alpha:
                best = mv
                alpha = temp
    recur_calls = 0
    move(best)
    return str(best)


def alphabeta(depth, duration, alpha: int, beta: int) -> int:
    global eval_bound, goal_depth, recur_calls, start_time
    if depth == 0 or winner() != '?':
        return evaluation()
    recur_calls += 1
    if duration > 0 and recur_calls >= 20000:
        if milliseconds()-start_time >= duration:
            raise TimeoutError(depth)
        else:
            recur_calls = 0
    score = -eval_bound
    for mv in moves_evaluated():
        move(mv)
        score = max(score, -alphabeta(depth-1, duration, -beta, -alpha))
        undo()
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return score


def fw_move(string: str):
    move(Move.fromstr(string[0:5]))


def fw_moves():
    return list(map(str, moves()))


def fw_moves_shuffled():
    mvs = moves_shuffled()
    return list(map(str, mvs))


def fw_moves_evaluated():
    mvs = moves_evaluated()
    return list(map(str, mvs))


def milliseconds() -> int:
    return int(round(time() * 1000))
