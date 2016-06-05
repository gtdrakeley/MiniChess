from typing import List
import move


class History(move.Move):
    def __init__(self, board: List[List[str]], mv: move.Move) -> None:
        super().__init__(mv.src_row, mv.src_column, mv.dest_row, mv.dest_column)
        self.data |= (ord(board[mv.src_row][mv.src_column]) << 12 |
                      ord(board[mv.dest_row][mv.dest_column]) << 19)

    @property
    def src_piece(self) -> str:
        return chr((self.data & 0x7f000) >> 12)

    @property
    def dest_piece(self) -> str:
        return chr((self.data & 0x3f80000) >> 19)
