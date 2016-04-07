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

    def board_set(self, board_str):
        turn_state, *board_state = board_str.split('\n')
        turn_state_split = turn_state.split()
        self.turn, self.playing = int(turn_state_split[0]), turn_state_split[1]
        self.board = bytearray(''.join(board_state).encode())

