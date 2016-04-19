# import random
from collections import namedtuple

Position = namedtuple('Position', ['row', 'column'])
Move = namedtuple('Move', ['start', 'end'])

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
        self.board = [bytearray(b'kqbnr'),
                      bytearray(b'ppppp'),
                      bytearray(b'.....'),
                      bytearray(b'.....'),
                      bytearray(b'PPPPP'),
                      bytearray(b'RNBQK')]

    def reset(self):
        self.turn = 1
        self.playing = 'W'
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

    def framework_moves(self):
        moves = self.moves()
        moves_strs = list()
        calpha = {0: 'a',
                  1: 'b',
                  2: 'c',
                  3: 'd',
                  4: 'e'}
        for move in moves:
            moves_strs.append('{}{}-{}{}\n'.format(calpha[move.start.colum], move.start.row,
                                                   calpha[move.end.colum], move.end.row))
        return '\n'.join(moves_strs) + '\n'

    def moves(self):
        moves = list()
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
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
        elif piece == 'P' or piece == 'p':
            moves.extend(self.pawn_moves(r, c))
        return moves

    def axis_moves(self, r: int, c: int, max_dist=5):
        moves = list()
        ublocked = dblocked = lblocked = rblocked = False
        origin = Position(r, c)
        for offset in range(1, max_dist + 1):
            if not ublocked:
                if ChessAI.is_valid(r + offset, c):
                    if self.is_own(self.board[r + offset][c]):
                        ublocked = True
                    else:
                        moves.append(Move(origin, Position(r + offset, c)))
                    if self.is_enemy(self.board[r + offset][c]):
                        ublocked = True
                else:
                    ublocked = True
            if not dblocked:
                if ChessAI.is_valid(r - offset, c):
                    if self.is_own(self.board[r - offset][c]):
                        dblocked = True
                    else:
                        moves.append(Move(origin, Position(r - offset, c)))
                    if self.is_enemy(self.board[r - offset][c]):
                        dblocked = True
                else:
                    dblocked = True
            if not lblocked:
                if ChessAI.is_valid(r, c - offset):
                    if self.is_own(self.board[r][c - offset]):
                        lblocked = True
                    else:
                        moves.append(Move(origin, Position(r, c - offset)))
                    if self.is_enemy(self.board[r][c - offset]):
                        lblocked = True
                else:
                    lblocked = True
            if not rblocked:
                if ChessAI.is_valid(r, c + offset):
                    if self.is_own(self.board[r][c + offset]):
                        rblocked = True
                    else:
                        moves.append(Move(origin, Position(r, c + offset)))
                    if self.is_enemy(self.board[r][c + offset]):
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
                    if self.is_own(self.board[r - offset][c - offset]):
                        ulblocked = True
                    else:
                        moves.append(Move(origin, Position(r - offset, c - offset)))
                    if self.is_enemy(self.board[r - offset][c - offset]):
                        ulblocked = True
                else:
                    ulblocked = True
            if not urblocked:
                if ChessAI.is_valid(r - offset, c + offset):
                    if self.is_own(self.board[r - offset][c + offset]):
                        urblocked = True
                    else:
                        moves.append(Move(origin, Position(r - offset, c + offset)))
                    if self.is_enemy(self.board[r - offset][c + offset]):
                        urblocked = True
                else:
                    urblocked = True
            if not dlblocked:
                if ChessAI.is_valid(r + offset, c - offset):
                    if self.is_own(self.board[r + offset][c - offset]):
                        dlblocked = True
                    else:
                        moves.append(Move(origin, Position(r + offset, c - offset)))
                    if self.is_enemy(self.board[r + offset][c - offset]):
                        dlblocked = True
                else:
                    dlblocked = True
            if not drblocked:
                if ChessAI.is_valid(r + offset, c + offset):
                    if self.is_own(self.board[r + offset][c + offset]):
                        drblocked = True
                    else:
                        moves.append(Move(origin, Position(r + offset, c + offset)))
                    if self.is_enemy(self.board[r + offset][c + offset]):
                        drblocked = True
                else:
                    drblocked = True
        return moves

    def bishop_moves(self, r: int, c: int):
        moves = list()
        origin = Position(r, c)
        if ChessAI.is_valid(r - 1, c - 1):
            if self.is_nothing(self.board[r - 1][c - 1]):
                moves.append(Move(origin, Position(r - 1, c - 1)))
        if ChessAI.is_valid(r - 1, c):
            if self.is_nothing(self.board[r - 1][c]):
                moves.append(Move(origin, Position(r - 1, c)))
        if ChessAI.is_valid(r - 1, c + 1):
            if self.is_nothing(self.board[r - 1][c + 1]):
                moves.append(Move(origin, Position(r - 1, c + 1)))
        if ChessAI.is_valid(r, c - 1):
            if self.is_nothing(self.board[r][c - 1]):
                moves.append(Move(origin, Position(r, c - 1)))
        if ChessAI.is_valid(r, c + 1):
            if self.is_nothing(self.board[r][c + 1]):
                moves.append(Move(origin, Position(r, c +1)))
        if ChessAI.is_valid(r + 1, c - 1):
            if self.is_nothing(self.board[r + 1][c - 1]):
                moves.append(Move(origin, Position(r + 1, c - 1)))
        if ChessAI.is_valid(r + 1, c):
            if self.is_nothing(self.board[r + 1][c]):
                moves.append(Move(origin, Position(r + 1, c)))
        if ChessAI.is_valid(r + 1, c + 1):
            if self.is_nothing(self.board[r + 1][c + 1]):
                moves.append(Move(origin, Position(r + 1, c + 1)))
        return moves

    def knight_moves(self, r: int, c: int):
        moves = list()
        origin = Position(r, c)
        if ChessAI.is_valid(r - 2, c - 1):
            if not self.is_own(self.board[r - 2][c - 1]):
                moves.append(Move(origin, Position(r - 2, c - 1)))
        if ChessAI.is_valid(r - 2, c + 1):
            if not self.is_own(self.board[r - 2][c + 1]):
                moves.append(Move(origin, Position(r - 2, c + 1)))
        if ChessAI.is_valid(r + 2, c - 1):
            if not self.is_own(self.board[r + 2][c - 1]):
                moves.append(Move(origin, Position(r + 2, c - 1)))
        if ChessAI.is_valid(r + 2, c + 1):
            if not self.is_own(self.board[r + 2][c + 1]):
                moves.append(Move(origin, Position(r + 2, c + 1)))
        if ChessAI.is_valid(r - 1, c - 2):
            if not self.is_own(self.board[r - 1][c - 2]):
                moves.append(Move(origin, Position(r - 1, c - 2)))
        if ChessAI.is_valid(r + 1, c - 2):
            if not self.is_own(self.board[r + 1][c - 2]):
                moves.append(Move(origin, Position(r + 1, c - 2)))
        if not ChessAI.is_valid(r - 1, c + 2):
            if not self.is_own(self.board[r - 1][c + 2]):
                moves.append(Move(origin, Position(r - 1, c + 2)))
        if not ChessAI.is_valid(r + 1, c + 2):
            if not self.is_own(self.board[r + 1][c + 2]):
                moves.append(Move(origin, Position(r + 1, c + 2)))
        return moves

    def pawn_moves(self,r: int, c: int):
        moves = list()
        origin = Position(r, c)
        if self.playing == 'W':
            if ChessAI.is_valid(r + 1, c):
                if self.is_nothing(self.board[r + 1][c]):
                    moves.append(Move(origin, Position(r + 1, c)))
            if ChessAI.is_valid(r + 1, c - 1):
                if self.is_enemy(self.board[r + 1][c - 1]):
                    moves.append(Move(origin, Position(r + 1, c - 1)))
            if ChessAI.is_valid(r + 1, c + 1):
                if self.is_enemy(self.board[r + 1][c + 1]):
                    moves.append(Move(origin, Position(r + 1, c + 1)))
        else:
            if ChessAI.is_valid(r - 1, c):
                if self.is_nothing(self.board[r - 1][c]):
                    moves.append(Move(origin, Position(r - 1, c)))
            if ChessAI.is_valid(r - 1, c - 1):
                if self.is_enemy(self.board[r - 1][c - 1]):
                    moves.append(Move(origin, Position(r - 1, c - 1)))
            if ChessAI.is_valid(r - 1, c + 1):
                if self.is_enemy(self.board[r - 1][c - 1]):
                    moves.append(Move(origin, Position(r - 1, c + 1)))

