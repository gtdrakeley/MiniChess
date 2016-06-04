import board
import move
import history
from typing import List


class BoardHistory(board.Board):
    def __init__(self):
        super().__init__()
        self.board_history = list()  # type: List[history.History]

    def save(self, mv: move.Move):
        self.board_history.append(history.History(self.board, mv))

    def undo(self):
        hist = self.board_history.pop()
        self.board[hist.src_row][hist.src_column] = hist.src_piece
        self.board[hist.dest_row][hist.dest_column] = hist.dest_piece

