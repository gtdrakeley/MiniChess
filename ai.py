import random
import textwrap


class ChessAI:
    white_pieces = 'KQBNR'
    black_pieces = 'kqbnr'

    def __init__(self):
        self.turn = 1
        self.playing = 'W'
        self.board = bytearray(b'kqbnr'
                               b'ppppp'
                               b'.....'
                               b'.....'
                               b'PPPPP'
                               b'RNBQK')

    def reset(self):
        self.__init__()

    def board_get(self):
        return '{} {}\n{}\n'.format(self.turn, self.playing, '\n'.join(textwrap.wrap(self.board.decode(), 5)))