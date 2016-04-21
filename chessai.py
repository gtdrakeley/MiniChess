import random
from collections import namedtuple

Position = namedtuple('Position', ['row', 'column'])
BoardHistory = namedtuple('BoardHistory', ['move', 'start_piece', 'end_piece'])


class Move:
    cta = {0: 'a',
           1: 'b',
           2: 'c',
           3: 'd',
           4: 'e'}

    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end

    def __str__(self):
        return '{}{}-{}{}\n'.format(Move.cta[self.start.column], 6 - self.start.row,
                                    Move.cta[self.end.column], 6 - self.end.row)


# Move = namedtuple('Move', ['start', 'end'])
# BoardHistory = namedtuple('BoardHistory', ['move', 'start_piece', 'end_piece'])


class ChessAI:
    white_pieces = 'KQBNRP'
    black_pieces = 'kqbnrp'
    piece_values = {'k': 10000, 'K': 10000,
                    'q': 5000, 'Q': 5000,
                    'b': 3000, 'B': 3000,
                    'n': 3000, 'N': 3000,
                    'r': 4000, 'R': 4000,
                    'p': 1000, 'P': 1000}

    def __init__(self):
        self.turn = 1
        self.playing = 'W'
        self.history = list()
        self.board = [bytearray(b'kqbnr'),
                      bytearray(b'ppppp'),
                      bytearray(b'.....'),
                      bytearray(b'.....'),
                      bytearray(b'PPPPP'),
                      bytearray(b'RNBQK')]

    def reset(self):
        self.turn = 1
        self.playing = 'W'
        self.history = list()
        self.board = [bytearray(b'kqbnr'),
                      bytearray(b'ppppp'),
                      bytearray(b'.....'),
                      bytearray(b'.....'),
                      bytearray(b'PPPPP'),
                      bytearray(b'RNBQK')]

    def board_get(self):
        return '{} {}\n{}\n'.format(self.turn, self.playing, '\n'.join(map(bytearray.decode, self.board)))

    def board_set(self, board_str):
        turn_state, *board_state = board_str.split('\n')
        turn, playing = turn_state.split()
        self.turn, self.playing = int(turn), playing
        self.board = [bytearray(row.encode()) for row in board_state if len(row) > 0]

    def winner(self):
        board_concat = bytearray.join(bytearray(b''), self.board).decode()
        if 'K' in board_concat and 'k' not in board_concat:
            return 'W'
        elif 'K' not in board_concat and 'k' in board_concat:
            return 'B'
        elif self.turn > 40:
            return '='
        else:
            return '?'

    @staticmethod
    def is_valid(int_r: int, int_c: int):
        if int_c < 0:
            return False
        elif int_c > 4:
            return False
        elif int_r < 0:
            return False
        elif int_r > 5:
            return False
        else:
            return True

    def is_enemy(self, str_piece: str):
        if self.playing == 'W' and str_piece in ChessAI.black_pieces:
            return True
        elif self.playing == 'B' and str_piece in ChessAI.white_pieces:
            return True
        else:
            return False

    def is_own(self, str_piece: str):
        if self.playing == 'W' and str_piece in ChessAI.white_pieces:
            return True
        elif self.playing == 'B' and str_piece in ChessAI.black_pieces:
            return True
        else:
            return False

    @staticmethod
    def is_nothing(str_piece: str):
        if str_piece == '.':
            return True
        else:
            return False

    def eval(self):
        white_score, black_score = 0, 0
        for row in self.board:
            for piece in row:
                piece = chr(piece)
                if piece in ChessAI.white_pieces:
                    white_score += ChessAI.piece_values[piece]
                elif piece in ChessAI.black_pieces:
                    black_score += ChessAI.piece_values[piece]
        return white_score - black_score if self.playing == 'W' else black_score - white_score

    def fw_moves(self):
        return list(map(str, self.moves()))
        # moves_str = list()
        # calpha = {0: 'a',
        #          1: 'b',
        #          2: 'c',
        #          3: 'd',
        #          4: 'e'}
        # for move in moves:
        #    moves_str.append('{}{}-{}{}\n'.format(calpha[move.start.column], 6 - move.start.row,
        #                                           calpha[move.end.column], 6 - move.end.row))
        # return moves_str

    def moves(self):
        moves = list()
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                piece = chr(piece)
                if self.playing == 'W' and piece in ChessAI.white_pieces:
                    moves.extend(self.piece_moves(piece, r, c))
                elif self.playing == 'B' and piece in ChessAI.black_pieces:
                    moves.extend(self.piece_moves(piece, r, c))
        return moves

    def piece_moves(self,  piece: str, r: int, c: int):
        moves = list()
        if piece == 'K' or piece == 'k':
            moves.extend(self.axis_moves(r, c, 1))
            moves.extend(self.diagonal_moves(r, c, 1))
        elif piece == 'Q' or piece == 'q':
            moves.extend(self.axis_moves(r, c))
            moves.extend(self.diagonal_moves(r, c))
        elif piece == 'R' or piece == 'r':
            moves.extend(self.axis_moves(r, c))
        elif piece == 'B' or piece == 'b':
            moves.extend(self.diagonal_moves(r, c))
            moves.extend(self.bishop_moves(r, c))
        elif piece == 'N' or piece == 'n':
            moves.extend(self.knight_moves(r, c))
        elif piece == 'P' or piece == 'p':
            moves.extend(self.pawn_moves(r, c))
        return moves

    def axis_moves(self, r: int, c: int, max_dist=5):
        moves = list()
        ublocked = dblocked = lblocked = rblocked = False
        origin = Position(r, c)
        for offset in range(1, max_dist + 1):
            if not ublocked:
                if ChessAI.is_valid(r - offset, c):
                    if self.is_own(chr(self.board[r - offset][c])):
                        ublocked = True
                    else:
                        moves.append(Move(origin, Position(r - offset, c)))
                    if self.is_enemy(chr(self.board[r - offset][c])):
                        ublocked = True
                else:
                    ublocked = True
            if not dblocked:
                if ChessAI.is_valid(r + offset, c):
                    if self.is_own(chr(self.board[r + offset][c])):
                        dblocked = True
                    else:
                        moves.append(Move(origin, Position(r + offset, c)))
                    if self.is_enemy(chr(self.board[r + offset][c])):
                        dblocked = True
                else:
                    dblocked = True
            if not lblocked:
                if ChessAI.is_valid(r, c - offset):
                    if self.is_own(chr(self.board[r][c - offset])):
                        lblocked = True
                    else:
                        moves.append(Move(origin, Position(r, c - offset)))
                    if self.is_enemy(chr(self.board[r][c - offset])):
                        lblocked = True
                else:
                    lblocked = True
            if not rblocked:
                if ChessAI.is_valid(r, c + offset):
                    if self.is_own(chr(self.board[r][c + offset])):
                        rblocked = True
                    else:
                        moves.append(Move(origin, Position(r, c + offset)))
                    if self.is_enemy(chr(self.board[r][c + offset])):
                        rblocked = True
                else:
                    rblocked = True
        return moves

    def diagonal_moves(self, r: int, c: int, max_dist=5):
        moves = list()
        ulblocked = urblocked = dlblocked = drblocked = False
        origin = Position(r, c)
        for offset in range(1, max_dist + 1):
            if not ulblocked:
                if ChessAI.is_valid(r - offset, c - offset):
                    if self.is_own(chr(self.board[r - offset][c - offset])):
                        ulblocked = True
                    else:
                        moves.append(Move(origin, Position(r - offset, c - offset)))
                    if self.is_enemy(chr(self.board[r - offset][c - offset])):
                        ulblocked = True
                else:
                    ulblocked = True
            if not urblocked:
                if ChessAI.is_valid(r - offset, c + offset):
                    if self.is_own(chr(self.board[r - offset][c + offset])):
                        urblocked = True
                    else:
                        moves.append(Move(origin, Position(r - offset, c + offset)))
                    if self.is_enemy(chr(self.board[r - offset][c + offset])):
                        urblocked = True
                else:
                    urblocked = True
            if not dlblocked:
                if ChessAI.is_valid(r + offset, c - offset):
                    if self.is_own(chr(self.board[r + offset][c - offset])):
                        dlblocked = True
                    else:
                        moves.append(Move(origin, Position(r + offset, c - offset)))
                    if self.is_enemy(chr(self.board[r + offset][c - offset])):
                        dlblocked = True
                else:
                    dlblocked = True
            if not drblocked:
                if ChessAI.is_valid(r + offset, c + offset):
                    if self.is_own(chr(self.board[r + offset][c + offset])):
                        drblocked = True
                    else:
                        moves.append(Move(origin, Position(r + offset, c + offset)))
                    if self.is_enemy(chr(self.board[r + offset][c + offset])):
                        drblocked = True
                else:
                    drblocked = True
        return moves

    def bishop_moves(self, r: int, c: int):
        moves = list()
        origin = Position(r, c)
        if ChessAI.is_valid(r - 1, c):
            if self.is_nothing(chr(self.board[r - 1][c])):
                moves.append(Move(origin, Position(r - 1, c)))
        if ChessAI.is_valid(r + 1, c):
            if self.is_nothing(chr(self.board[r + 1][c])):
                moves.append(Move(origin, Position(r + 1, c)))
        if ChessAI.is_valid(r, c - 1):
            if self.is_nothing(chr(self.board[r][c - 1])):
                moves.append(Move(origin, Position(r, c - 1)))
        if ChessAI.is_valid(r, c + 1):
            if self.is_nothing(chr(self.board[r][c + 1])):
                moves.append(Move(origin, Position(r, c + 1)))
        return moves

    def knight_moves(self, r: int, c: int):
        moves = list()
        origin = Position(r, c)
        if ChessAI.is_valid(r - 2, c - 1):
            if not self.is_own(chr(self.board[r - 2][c - 1])):
                moves.append(Move(origin, Position(r - 2, c - 1)))
        if ChessAI.is_valid(r - 2, c + 1):
            if not self.is_own(chr(self.board[r - 2][c + 1])):
                moves.append(Move(origin, Position(r - 2, c + 1)))
        if ChessAI.is_valid(r + 2, c - 1):
            if not self.is_own(chr(self.board[r + 2][c - 1])):
                moves.append(Move(origin, Position(r + 2, c - 1)))
        if ChessAI.is_valid(r + 2, c + 1):
            if not self.is_own(chr(self.board[r + 2][c + 1])):
                moves.append(Move(origin, Position(r + 2, c + 1)))
        if ChessAI.is_valid(r - 1, c - 2):
            if not self.is_own(chr(self.board[r - 1][c - 2])):
                moves.append(Move(origin, Position(r - 1, c - 2)))
        if ChessAI.is_valid(r + 1, c - 2):
            if not self.is_own(chr(self.board[r + 1][c - 2])):
                moves.append(Move(origin, Position(r + 1, c - 2)))
        if ChessAI.is_valid(r - 1, c + 2):
            if not self.is_own(chr(self.board[r - 1][c + 2])):
                moves.append(Move(origin, Position(r - 1, c + 2)))
        if ChessAI.is_valid(r + 1, c + 2):
            if not self.is_own(chr(self.board[r + 1][c + 2])):
                moves.append(Move(origin, Position(r + 1, c + 2)))
        return moves

    def pawn_moves(self, r: int, c: int):
        moves = list()
        origin = Position(r, c)
        if self.playing == 'W':
            if ChessAI.is_valid(r - 1, c):
                if self.is_nothing(chr(self.board[r - 1][c])):
                    moves.append(Move(origin, Position(r - 1, c)))
            if ChessAI.is_valid(r - 1, c - 1):
                if self.is_enemy(chr(self.board[r - 1][c - 1])):
                    moves.append(Move(origin, Position(r - 1, c - 1)))
            if ChessAI.is_valid(r - 1, c + 1):
                if self.is_enemy(chr(self.board[r - 1][c + 1])):
                    moves.append(Move(origin, Position(r - 1, c + 1)))
        else:
            if ChessAI.is_valid(r + 1, c):
                if self.is_nothing(chr(self.board[r + 1][c])):
                    moves.append(Move(origin, Position(r + 1, c)))
            if ChessAI.is_valid(r + 1, c - 1):
                if self.is_enemy(chr(self.board[r + 1][c - 1])):
                    moves.append(Move(origin, Position(r + 1, c - 1)))
            if ChessAI.is_valid(r + 1, c + 1):
                if self.is_enemy(chr(self.board[r + 1][c + 1])):
                    moves.append(Move(origin, Position(r + 1, c + 1)))
        return moves

    def fw_move(self, move_str: str):
        print(move_str.encode())
        cnum = {'a': 0,
                'b': 1,
                'c': 2,
                'd': 3,
                'e': 4}
        start, end = move_str.strip().split('-')
        start, end = list(start), list(end)
        move = Move(Position(6 - int(start[1]), cnum[start[0]]), Position(6 - int(end[1]), cnum[end[0]]))
        self.move(move)
    
    def fw_moves_shuffled(self):
        moves = self.moves_shuffled()
        return list(map(str, moves))

    def moves_shuffled(self):
        moves = self.moves()
        random.shuffle(moves)
        return moves

    def move(self, move: Move):
        self.history.append(BoardHistory(move,
                                         self.board[move.start.row][move.start.column],
                                         self.board[move.end.row][move.end.column]))
        if self.playing == 'W':
            self.playing = 'B'
        else:
            self.playing = 'W'
            self.turn += 1
        self.board[move.end.row][move.end.column] = self.board[move.start.row][move.start.column]
        self.board[move.start.row][move.start.column] = ord('.')
        if move.end.row == 0 and self.board[move.end.row][move.end.column] == ord('P'):
            self.board[move.end.row][move.end.column] = ord('Q')
        elif move.end.row == 5 and self.board[move.end.row][move.end.column] == ord('p'):
            self.board[move.end.row][move.end.column] = ord('q')

    def undo(self):
        if self.history:
            prev = self.history.pop()
            if self.playing == 'W':
                self.playing = 'B'
                self.turn -= 1
            else:
                self.playing = 'W'
            self.board[prev.move.start.row][prev.move.start.column] = prev.start_piece
            self.board[prev.move.end.row][prev.move.end.column] = prev.end_piece

    def move_random(self):
        move = self.moves_shuffled()[0]
        self.move(move)
        return str(move)

    def fw_moves_evaluated(self):
        moves = self.moves_evaluated()
        return list(map(str, moves))

    def moves_evaluated(self):
        moves = self.moves_shuffled()
        evals = list()
        for move in moves:
            self.move(move)
            evals.append(self.eval())
            self.undo()
        zipped = list(zip(evals, moves))
        zipped.sort(key=lambda e: e[0])
        evals, moves = zip(*tuple(zipped))
        return list(moves)

    def move_greedy(self):
        move = self.moves_evaluated()[0]
        self.move(move)
        return str(move)

    def move_negamax(self, depth: int, duration: int):
        best = None
        score = -31001
        temp = 0
        for move in self.moves_shuffled():
            self.move(move)
            temp = -self.negamax(depth - 1, duration)
            self.undo()
            if temp > score:
                best = move
                score = temp
        self.move(best)
        return str(best)

    def negamax(self, depth: int, duration: int):
        if depth == 0 or self.winner() != '?':
            return self.eval()
        score = -31001
        for move in self.moves_shuffled():
            self.move(move)
            score = max(score, -self.negamax(depth - 1, duration))
            self.undo()
        return score

    def move_alphabeta(self, depth: int, duration: int):
        best = None
        alpha = -31001
        beta = 31001
        temp = 0
        for move in self.moves_evaluated():
            self.move(move)
            temp = -self.alphabeta(depth - 1, duration, -beta, -alpha)
            self.undo()
            if temp > alpha:
                best = move
                alpha = temp
        self.move(move)
        return str(best)

    def alphabeta(self, depth: int, duration: int, alpha: int, beta: int):
        if depth == 0 or self.winner() != '?':
            return self.eval()
        score = -31001
        for move in self.moves_evaluated():
            self.move(move)
            score = max(score, -self.alphabeta(depth - 1, duration, -beta, -alpha))
            self.undo()
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return score
