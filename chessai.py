import random
import textwrap


class ChessAI:
    white_pieces = 'KQBNR'
    black_pieces = 'kqbnr'
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
        self.__init__()

    def board_get(self):
        return '{} {}\n{}\n'.format(self.turn, self.playing, '\n'.join(map(bytearray.decode, self.board)))

    def board_set(self, board_str):
        turn_state, *board_state = board_str.split('\n')
        turn, playing = turn_state.split()
        self.turn, self.playing = int(turn), playing
        self.board = [bytearray(row.encode()) for row in board_state if len(row) > 0]

    def winner(self):
        if self.turn > 40:
            return '='
        else:
            board_concat = bytearray.join(bytearray(b''), self.board)
            if ord('k') in board_concat and ord('K') in board_concat:
                return '?'
            elif ord('k') in board_concat:
                return 'W'
            elif ord('K') in board_concat:
                return 'B'
            else:
                return '='

    @staticmethod
    def is_valid(int_x: int, int_y: int):
        if int_x < 0:
            return False
        elif int_x > 4:
            return False
        elif int_y < 0:
            return False
        elif int_y > 5:
            return False
        else:
            return True

    def is_enemy(self, str_piece: str):
        if self.playing == 'W' and str_piece in ChessAI.white_pieces:
            return False
        elif self.playing == 'B' and str_piece in ChessAI.black_pieces:
            return False
        else:
            return True

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

