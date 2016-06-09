from move import Move
from history import History
from typing import List, Tuple
import time

import random


def milliseconds() -> int:
    return int(round(time.time() * 1000))


class ChessAIV2:
    white_pieces = 'KQBNRP'
    black_pieces = 'kqbnrp'
    # """
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
    # """
    """
    piece_position_values = {'K': [[3500, 3500, 2000, 3500, 3500],
                                   [10000, 10000, 5000, 10000, 10000],
                                   [16500, 13000, 10000, 13000, 16500],
                                   [19000, 16500, 14000, 16500, 19000],
                                   [32500, 32500, 20000, 32500, 32500],
                                   [32500, 50000, 20000, 50000, 32500]],
                             'Q': [[1200, 1300, 1700, 1300, 1200],
                                   [1300, 2000, 2500, 2000, 1300],
                                   [1500, 2000, 3000, 2000, 1500],
                                   [1500, 2000, 3000, 2000, 1500],
                                   [800, 1000, 1500, 1000, 800],
                                   [600, 800, 1000, 800, 600]],
                             'B': [[100, 200, 300, 200, 100],
                                   [400, 600, 700, 600, 400],
                                   [400, 700, 1000, 700, 400],
                                   [350, 600, 850, 600, 350],
                                   [300, 500, 700, 500, 300],
                                   [100, 150, 200, 150, 100]],
                             'N': [[75, 150, 250, 150, 75],
                                   [150, 450, 600, 450, 150],
                                   [150, 700, 1000, 700, 150],
                                   [150, 600, 800, 600, 150],
                                   [100, 300, 450, 300, 100],
                                   [75, 150, 150, 150, 75]],
                             'R': [[800, 600, 400, 800, 800],
                                   [1000, 800, 600, 800, 1000],
                                   [1200, 1000, 800, 1000, 1200],
                                   [1400, 1200, 1100, 1200, 1400],
                                   [1800, 1600, 1450, 1600, 1800],
                                   [2000, 1750, 1500, 1750, 2000]],
                             'P': [[0, 0, 0, 0, 0],
                                   [750, 750, 750, 750, 500],
                                   [150, 350, 500, 350, 150],
                                   [100, 150, 300, 150, 100],
                                   [150, 200, 100, 250, 150],
                                   [0, 0, 0, 0, 0]],
                             '.': [[0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0]]}
    # """
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

    def __init__(self):
        self.turn = 1
        self.playing = 'W'
        self.board = list()  # type: List[List[str]]
        self.board.extend([list('kqbnr'),
                           list('ppppp'),
                           list('.....'),
                           list('.....'),
                           list('PPPPP'),
                           list('RNBQK')])
        """
        self.board = list([list('kqbnr'),  # type: List[List[str]]
                           list('ppppp'),
                           list('.....'),
                           list('.....'),
                           list('PPPPP'),
                           list('RNBQK')])
        """
        self.white_score = 0
        self.black_score = 0
        self.board_history = list()  # type: List[History]
        self.eval_history = list()  # type: List[Tuple[int, int]]
        self.goal_depth = 0
        self.recur_calls = 0
        self.start_time = 0
        self.move_duration = -1
        self.evaluate_board()

    def reset(self) -> None:
        self.__init__()

    def get_board(self) -> str:
        return '{} {}\n{}\n'.format(self.turn, self.playing, '\n'.join(map(''.join, self.board)))

    def set_board(self, string: str) -> None:
        turn_state, *board_state = string.split('\n')
        self.turn, self.playing = turn_state.split()
        self.turn = int(self.turn)
        self.board = list(map(list, filter(None, board_state)))
        self.evaluate_board()

    def winner(self) -> str:
        cat_board = ''.join(map(''.join, self.board))
        if 'K' in cat_board and 'k' not in cat_board:
            return 'W'
        elif 'K' not in cat_board and 'k' in cat_board:
            return 'B'
        elif self.turn > 40:
            return '='
        else:
            return '?'

    def evaluation(self) -> int:
        return self.white_score - self.black_score if self.playing == 'W' else self.black_score - self.white_score

    def evaluate_board(self) -> None:
        self.white_score, self.black_score = 0, 0
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if piece in ChessAIV2.white_pieces:
                    self.white_score += ChessAIV2.piece_position_values[piece][r][c]
                elif piece in ChessAIV2.black_pieces:
                    self.black_score += ChessAIV2.piece_position_values[piece][5-r][4-c]

    def move(self, mv: Move) -> None:
        # Save board state
        self.board_history.append(History(self.board, mv))
        self.eval_history.append((self.white_score, self.black_score))
        # Begin updating evaluation
        src_piece = self.board[mv.src_row][mv.src_column]
        dest_piece = self.board[mv.dest_row][mv.dest_column]
        if src_piece in ChessAIV2.white_pieces:
            self.white_score -= ChessAIV2.piece_position_values[src_piece][mv.src_row][mv.src_column]
            self.black_score -= ChessAIV2.piece_position_values[dest_piece][5-mv.dest_row][4-mv.dest_column]
        else:
            self.white_score -= ChessAIV2.piece_position_values[dest_piece][mv.dest_row][mv.dest_column]
            self.black_score -= ChessAIV2.piece_position_values[src_piece][5-mv.src_row][4-mv.src_column]
        # Perform the move
        if self.playing == 'W':
            self.playing = 'B'
        else:
            self.playing = 'W'
            self.turn += 1
        src_piece = self.board[mv.src_row][mv.src_column]
        self.board[mv.src_row][mv.src_column] = '.'
        if src_piece == 'P' and mv.dest_row == 0:
            self.board[mv.dest_row][mv.dest_column] = 'Q'
        elif src_piece == 'p' and mv.dest_row == 5:
            self.board[mv.dest_row][mv.dest_column] = 'q'
        else:
            self.board[mv.dest_row][mv.dest_column] = src_piece
        # self.evaluate_board()
        # End updating evaluation
        src_piece = self.board[mv.dest_row][mv.dest_column]
        if src_piece in ChessAIV2.white_pieces:
            self.white_score += ChessAIV2.piece_position_values[src_piece][mv.dest_row][mv.dest_column]
        else:
            self.black_score += ChessAIV2.piece_position_values[src_piece][5-mv.dest_row][4-mv.dest_column]

    def undo(self) -> None:
        assert self.board_history, 'Attempted to undo with empty board history'
        assert self.eval_history, 'Attempted to undo with empty eval history'
        hist = self.board_history.pop()
        self.white_score, self.black_score = self.eval_history.pop()
        if self.playing == 'W':
            self.playing = 'B'
            self.turn -= 1
        else:
            self.playing = 'W'
        self.board[hist.src_row][hist.src_column] = hist.src_piece
        self.board[hist.dest_row][hist.dest_column] = hist.dest_piece

    @staticmethod
    def is_valid(int_r: int, int_c: int) -> bool:
        if 0 <= int_c <= 4 and 0 <= int_r <= 5:
            return True
        else:
            return False

    @staticmethod
    def is_nothing(piece: str) -> bool:
        return True if piece == '.' else False

    def is_enemy(self, piece: str) -> bool:
        if self.playing == 'W' and piece in ChessAIV2.black_pieces:
            return True
        elif self.playing == 'B' and piece in ChessAIV2.white_pieces:
            return True
        else:
            return False

    def is_own(self, piece: str) -> bool:
        if self.playing == 'W' and piece in ChessAIV2.white_pieces:
            return True
        elif self.playing == 'B' and piece in ChessAIV2.black_pieces:
            return True
        else:
            return False

    def piece_moves(self, piece: str, r: int, c: int) -> List[Move]:
        mvs = list()
        if piece == 'K' or piece == 'k':
            mvs.extend(self.axis_moves(r, c, 1))
            mvs.extend(self.diagonal_moves(r, c, 1))
        elif piece == 'Q' or piece == 'q':
            mvs.extend(self.axis_moves(r, c))
            mvs.extend(self.diagonal_moves(r, c))
        elif piece == 'R' or piece == 'r':
            mvs.extend(self.axis_moves(r, c))
        elif piece == 'B' or piece == 'b':
            mvs.extend(self.diagonal_moves(r, c))
            mvs.extend(self.bishop_moves(r, c))
        elif piece == 'N' or piece == 'n':
            mvs.extend(self.knight_moves(r, c))
        elif piece == 'P' or piece == 'p':
            mvs.extend(self.pawn_moves(r, c))
        return mvs

    def axis_moves(self, r: int, c: int, max_dist=5) -> List[Move]:
        mvs = list()
        ublocked = dblocked = lblocked = rblocked = False
        for offset in range(1, max_dist+1):
            if not ublocked and ChessAIV2.is_valid(r-offset, c) and not self.is_own(self.board[r-offset][c]):
                mvs.append(Move(r, c, r-offset, c))
                if self.is_enemy(self.board[r-offset][c]):
                    ublocked = True
            else:
                ublocked = True
            if not dblocked and ChessAIV2.is_valid(r+offset, c) and not self.is_own(self.board[r+offset][c]):
                mvs.append(Move(r, c, r+offset, c))
                if self.is_enemy(self.board[r+offset][c]):
                    dblocked = True
            else:
                dblocked = True
            if not lblocked and ChessAIV2.is_valid(r, c-offset) and not self.is_own(self.board[r][c-offset]):
                mvs.append(Move(r, c, r, c - offset))
                if self.is_enemy(self.board[r][c-offset]):
                    lblocked = True
            else:
                lblocked = True
            if not rblocked and ChessAIV2.is_valid(r, c+offset) and not self.is_own(self.board[r][c+offset]):
                mvs.append(Move(r, c, r, c+offset))
                if self.is_enemy(self.board[r][c+offset]):
                    rblocked = True
            else:
                rblocked = True
            if ublocked and dblocked and lblocked and rblocked:
                break
        return mvs

    def diagonal_moves(self, r: int, c: int, max_dist=5) -> List[Move]:
        mvs = list()
        ulblocked = urblocked = dlblocked = drblocked = False
        for offset in range(1, max_dist+1):
            if not ulblocked and ChessAIV2.is_valid(r-offset, c-offset) and \
                    not self.is_own(self.board[r-offset][c-offset]):
                mvs.append(Move(r, c, r-offset, c-offset))
                if self.is_enemy(self.board[r-offset][c-offset]):
                    ulblocked = True
            else:
                ulblocked = True
            if not urblocked and ChessAIV2.is_valid(r-offset, c+offset) and \
                    not self.is_own(self.board[r-offset][c+offset]):
                mvs.append(Move(r, c, r-offset, c+offset))
                if self.is_enemy(self.board[r-offset][c+offset]):
                    urblocked = True
            else:
                urblocked = True
            if not dlblocked and ChessAIV2.is_valid(r + offset, c - offset) and \
                    not self.is_own(self.board[r+offset][c-offset]):
                mvs.append(Move(r, c, r+offset, c-offset))
                if self.is_enemy(self.board[r+offset][c-offset]):
                    dlblocked = True
            else:
                dlblocked = True
            if not drblocked and ChessAIV2.is_valid(r+offset, c+offset) and \
                    not self.is_own(self.board[r+offset][c+offset]):
                mvs.append(Move(r, c, r+offset, c+offset))
                if self.is_enemy(self.board[r+offset][c+offset]):
                    drblocked = True
            else:
                drblocked = True
            if ulblocked and urblocked and dlblocked and drblocked:
                break
        return mvs

    def bishop_moves(self, r: int, c: int) -> List[Move]:
        mvs = list()
        if ChessAIV2.is_valid(r-1, c) and ChessAIV2.is_nothing(self.board[r-1][c]):
            mvs.append(Move(r, c, r-1, c))
        if ChessAIV2.is_valid(r+1, c) and ChessAIV2.is_nothing(self.board[r+1][c]):
            mvs.append(Move(r, c, r+1, c))
        if ChessAIV2.is_valid(r, c-1) and ChessAIV2.is_nothing(self.board[r][c-1]):
            mvs.append(Move(r, c, r, c-1))
        if ChessAIV2.is_valid(r, c+1) and ChessAIV2.is_nothing(self.board[r][c+1]):
            mvs.append(Move(r, c, r, c+1))
        return mvs

    def knight_moves(self, r: int, c: int) -> List[Move]:
        mvs = list()
        if ChessAIV2.is_valid(r-2, c-1) and not self.is_own(self.board[r-2][c-1]):
            mvs.append(Move(r, c, r-2, c-1))
        if ChessAIV2.is_valid(r-2, c+1) and not self.is_own(self.board[r-2][c+1]):
            mvs.append(Move(r, c, r-2, c+1))
        if ChessAIV2.is_valid(r+2, c-1) and not self.is_own(self.board[r+2][c-1]):
            mvs.append(Move(r, c, r+2, c-1))
        if ChessAIV2.is_valid(r+2, c+1) and not self.is_own(self.board[r+2][c+1]):
            mvs.append(Move(r, c, r+2, c+1))
        if ChessAIV2.is_valid(r-1, c-2) and not self.is_own(self.board[r-1][c-2]):
            mvs.append(Move(r, c, r-1, c-2))
        if ChessAIV2.is_valid(r+1, c-2) and not self.is_own(self.board[r+1][c-2]):
            mvs.append(Move(r, c, r+1, c-2))
        if ChessAIV2.is_valid(r-1, c+2) and not self.is_own(self.board[r-1][c+2]):
            mvs.append(Move(r, c, r-1, c+2))
        if ChessAIV2.is_valid(r+1, c+2) and not self.is_own(self.board[r+1][c+2]):
            mvs.append(Move(r, c, r+1, c+2))
        return mvs

    def pawn_moves(self, r: int, c: int) -> List[Move]:
        mvs = list()
        if self.playing == 'W':
            if ChessAIV2.is_valid(r-1, c) and ChessAIV2.is_nothing(self.board[r-1][c]):
                mvs.append(Move(r, c, r-1, c))
            if ChessAIV2.is_valid(r-1, c-1) and self.is_enemy(self.board[r-1][c-1]):
                mvs.append(Move(r, c, r-1, c-1))
            if ChessAIV2.is_valid(r-1, c+1) and self.is_enemy(self.board[r-1][c+1]):
                mvs.append(Move(r, c, r-1, c+1))
        else:
            if ChessAIV2.is_valid(r+1, c) and ChessAIV2.is_nothing(self.board[r+1][c]):
                mvs.append(Move(r, c, r+1, c))
            if ChessAIV2.is_valid(r+1, c-1) and self.is_enemy(self.board[r+1][c-1]):
                mvs.append(Move(r, c, r+1, c-1))
            if ChessAIV2.is_valid(r+1, c+1) and self.is_enemy(self.board[r+1][c+1]):
                mvs.append(Move(r, c, r+1, c+1))
        return mvs

    def moves(self) -> List[Move]:
        mvs = list()
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if piece == '.':
                    continue
                elif self.playing == 'W' and piece in ChessAIV2.white_pieces:
                    mvs.extend(self.piece_moves(piece, r, c))
                elif self.playing == 'B' and piece in ChessAIV2.black_pieces:
                    mvs.extend(self.piece_moves(piece, r, c))
        return mvs

    def moves_shuffled(self) -> List[Move]:
        mvs = self.moves()
        random.shuffle(mvs)
        return mvs

    def moves_evaluated(self) -> List[Move]:
        mvs = self.moves_shuffled()
        evals = list()  # type: List[int]
        for mv in mvs:
            self.move(mv)
            evals.append(self.evaluation())
            self.undo()
        zipped = list(zip(evals, mvs))
        zipped.sort(key=lambda e: e[0])
        evals, mvs = zip(*tuple(zipped))
        return list(mvs)

    def move_random(self) -> str:
        mv = self.moves_shuffled()[0]
        self.move(mv)
        return str(mv)

    def move_greedy(self) -> str:
        mv = self.moves_evaluated()[0]
        self.move(mv)
        return str(mv)

    def move_negamax(self, depth: int, duration: int) -> str:
        best = None
        score = -self.eval_bound
        for mv in self.moves_shuffled():
            self.move(mv)
            temp = -self.negamax(depth-1, duration)
            self.undo()
            if temp > score:
                best = mv
                score = temp
        self.move(best)
        return str(best)

    def negamax(self, depth: int, duration: int) -> int:
        if depth == 0 or self.winner() != '?':
            return self.evaluation()
        score = -self.eval_bound
        for mv in self.moves_shuffled():
            self.move(mv)
            score = max(score, -self.negamax(depth-1, duration))
            self.undo()
        return score

    """
    def move_alphabeta(self, depth: int, duration: int) -> Tuple[int, str]:
        best = None
        alpha = -ChessAIV2.eval_bound
        beta = ChessAIV2.eval_bound
        if depth < 0:
            temp_mv = None
            iter_depth = 1
            move_duration = (duration-1500) / (41-self.turn)
            self.start_time = milliseconds()
            try:
                while True:
                    self.goal_depth = iter_depth
                    for mv in self.moves_evaluated():
                        self.move(mv)
                        temp = -self.alphabeta(iter_depth-1, move_duration, -beta, -alpha)
                        self.undo()
                        if temp > alpha:
                            temp_mv = mv
                            alpha = temp
                    best = temp_mv
                    iter_depth += 1
                    if iter_depth > 80-(self.turn+self.turn-(2 if self.playing == 'W' else 1)):
                        raise TimeoutError(iter_depth)
            except TimeoutError as e:
                print(iter_depth-1)
                print(move_duration)
                for _ in range(iter_depth-e.args[0]):
                    self.undo()
                self.recur_calls = 0
                self.move(best)
                return self.goal_depth-1, str(best)
        else:
            for mv in self.moves_evaluated():
                self.move(mv)
                temp = -self.alphabeta(depth-1, duration, -beta, -alpha)
                self.undo()
                if temp > alpha:
                    best = mv
                    alpha = temp
                self.move(best)
                return depth, str(best)
        return 0, ''
    # """

    # """
    def move_alphabeta(self, depth: int, duration: int):
        if depth < 0:
            try:
                if self.move_duration < 0:
                    self.move_duration = (duration-1500) / (41-self.turn)
                    self.start_time = milliseconds()
                best = None
                temp_best = None
                alpha = -ChessAIV2.eval_bound
                beta = ChessAIV2.eval_bound
                iter_depth = 1
                max_depth = 80-(self.turn+self.turn-(2 if self.playing == 'W' else 1))
                while True:
                    for mv in self.moves_evaluated():
                        self.move(mv)
                        temp = -self.alphabeta(iter_depth - 1, self.move_duration, -beta, -alpha)
                        self.undo()
                        if temp > alpha:
                            temp_best = mv
                            alpha = temp
                    best = temp_best
                    iter_depth += 1
                    if iter_depth > max_depth:
                        raise TimeoutError(iter_depth)
            except TimeoutError as e:
                print(iter_depth - 1)
                print(self.move_duration)
                for _ in range(iter_depth - e.args[0]):
                    self.undo()
                self.move_duration = -1
                self.start_time = 0
                self.recur_calls = 0
                self.move(best)
                return iter_depth-1, str(best)
        else:
            best = None
            alpha = -ChessAIV2.eval_bound
            beta = ChessAIV2.eval_bound
            temp = 0
            for mv in self.moves_evaluated():
                self.move(mv)
                temp = -self.alphabeta(depth - 1, 0, -beta, -alpha)
                self.undo()
                if temp > alpha:
                    best = mv
                    alpha = temp
            self.move(best)
            return str(best)
        return 0, ''
    # """

    """
    def alphabeta(self, depth: int, duration: int, alpha: int, beta: int) -> int:
        self.recur_calls += 1
        if duration > 0 and self.recur_calls > 20000:
            self.recur_calls = 0
            if milliseconds()-self.start_time >= duration:
                raise TimeoutError(depth)
        if depth == 0 or self.winner() != '?':
            return self.evaluation()
        score = -ChessAIV2.eval_bound
        for mv in self.moves_evaluated():
            self.move(mv)
            score = max(score, -self.alphabeta(depth-1, duration, -beta, -alpha))
            self.undo()
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return score
    # """

    # """
    def alphabeta(self, depth: int, duration: int, alpha: int, beta: int):
        self.recur_calls += 1
        if duration > 0 and self.recur_calls > 20000:
            if milliseconds() - self.start_time >= duration:
                raise TimeoutError(depth)
            else:
                self.recur_calls = 0
        if depth == 0 or self.winner() != '?':
            return self.evaluation()
        score = -ChessAIV2.eval_bound
        for mv in self.moves_evaluated():
            self.move(mv)
            score = max(score, -self.alphabeta(depth - 1, duration, -beta, -alpha))
            self.undo()
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return score
    # """

    def fw_move(self, string: str):
        self.move(Move.fromstr(string[0:5]))

    def fw_moves(self):
        return list(map(str, self.moves()))

    def fw_moves_shuffled(self):
        mvs = self.moves_shuffled()
        return list(map(str, mvs))

    def fw_moves_evaluated(self):
        mvs = self.moves_evaluated()
        return list(map(str, mvs))
