from board import Board
from move import Move
from history import History
from typing import List


class BoardHistory(Board):
    def __init__(self) -> None:
        super().__init__()
        self.board_history = list()  # type: List[History]

    def move(self, mv: Move) -> None:
        self.board_history.append(History(self.board, mv))
        super().move(mv)

    def undo(self) -> None:
        hist = self.board_history.pop()
        self.board[hist.src_row][hist.src_column] = hist.src_piece
        self.board[hist.dest_row][hist.dest_column] = hist.dest_piece
