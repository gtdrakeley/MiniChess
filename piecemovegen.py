from boardeval import BoardEvaluator
from move import Move
from typing import List


class PieceMoveGenerator(BoardEvaluator):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def is_valid(int_r: int, int_c: int) -> bool:
        if 0 <= int_c <= 4 and 0 <= int_r <= 5:
            return True
        else:
            return False

    def piece_moves(self, piece: str, r: int, c: int) -> List[Move]:
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

    def axis_moves(self, r: int, c: int, max_dist=5) -> List[Move]:
        moves = list()
        ublocked = dblocked = lblocked = rblocked = False
        for offset in range(1, max_dist+1):
            if not ublocked and PieceMoveGenerator.is_valid(r-offset, c) and not self.is_own(self.board[r-offset][c]):
                moves.append(Move(r, c, r-offset, c))
            else:
                ublocked = True
            if not dblocked and PieceMoveGenerator.is_valid(r+offset, c) and not self.is_own(self.board[r+offset][c]):
                moves.append(Move(r, c, r+offset, c))
            else:
                dblocked = True
            if not lblocked and PieceMoveGenerator.is_valid(r, c-offset) and not self.is_own(self.board[r][c-offset]):
                moves.append(Move(r, c, r, c-offset))
            else:
                lblocked = True
            if not rblocked and PieceMoveGenerator.is_valid(r, c+offset) and not self.is_own(self.board[r][c+offset]):
                moves.append(Move(r, c, r, c+offset))
        return moves

    def diagonal_moves(self, r: int, c: int, max_dist=5) -> List[Move]:
        moves = list()
        ulblocked = urblocked = dlblocked = drblocked = False
        for offset in range(1, max_dist+1):
            if not ulblocked and PieceMoveGenerator.is_valid(r-offset, c-offset) and \
                    not self.is_own(self.board[r-offset][c-offset]):
                moves.append(Move(r, c, r-offset, c-offset))
            else:
                ulblocked = True
            if not urblocked and PieceMoveGenerator.is_valid(r-offset, c+offset) and \
                    not self.is_own(self.board[r-offset][c+offset]):
                moves.append(Move(r, c, r-offset, c+offset))
            else:
                urblocked = True
            if not dlblocked and PieceMoveGenerator.is_valid(r+offset, c-offset) and \
                    not self.is_own(self.board[r+offset][c-offset]):
                moves.append(Move(r, c, r+offset, c-offset))
            else:
                dlblocked = True
            if not drblocked and PieceMoveGenerator.is_valid(r+offset, c+offset) and \
                    not self.is_own(self.board[r+offset][c+offset]):
                moves.append(Move(r, c, r+offset, c+offset))
            else:
                drblocked = True
        return moves

    def bishop_moves(self, r: int, c: int) -> List[Move]:
        moves = list()
        if PieceMoveGenerator.is_valid(r-1, c) and self.is_nothing(self.board[r-1][c]):
            moves.append(Move(r, c, r-1, c))
        if PieceMoveGenerator.is_valid(r+1, c) and self.is_nothing(self.board[r+1][c]):
            moves.append(Move(r, c, r+1, c))
        if PieceMoveGenerator.is_valid(r, c-1) and self.is_nothing(self.board[r][c-1]):
            moves.append(Move(r, c, r, c-1))
        if PieceMoveGenerator.is_valid(r, c+1) and self.is_nothing(self.board[r][c+1]):
            moves.append(Move(r, c, r, c+1))
        return moves

    def knight_moves(self, r: int, c: int) -> List[Move]:
        moves = list()
        if PieceMoveGenerator.is_valid(r-2, c-1) and not self.is_own(self.board[r-2][c-1]):
            moves.append(Move(r, c, r-2, c-1))
        if PieceMoveGenerator.is_valid(r-2, c+1) and not self.is_own(self.board[r-2][c+1]):
            moves.append(Move(r, c, r-2, c+1))
        if PieceMoveGenerator.is_valid(r+2, c-1) and not self.is_own(self.board[r+2][c-1]):
            moves.append(Move(r, c, r+2, c-1))
        if PieceMoveGenerator.is_valid(r+2, c+1) and not self.is_own(self.board[r+2][c+1]):
            moves.append(Move(r, c, r+2, c+1))
        if PieceMoveGenerator.is_valid(r-1, c-2) and not self.is_own(self.board[r-1][c-2]):
            moves.append(Move(r, c, r-1, c-2))
        if PieceMoveGenerator.is_valid(r+1, c-2) and not self.is_own(self.board[r+1][c-2]):
            moves.append(Move(r, c, r+1, c-2))
        if PieceMoveGenerator.is_valid(r-1, c+2) and not self.is_own(self.board[r-1][c+2]):
            moves.append(Move(r, c, r-1, c+2))
        if PieceMoveGenerator.is_valid(r+1, c+2) and not self.is_own(self.board[r+1][c+2]):
            moves.append(Move(r, c, r+1, c+2))
        return moves

    def pawn_moves(self, r: int, c: int) -> List[Move]:
        moves = list()
        if self.playing == 'W':
            if PieceMoveGenerator.is_valid(r-1, c) and self.is_nothing(self.board[r-1][c]):
                moves.append(Move(r, c, r-1, c))
            if PieceMoveGenerator.is_valid(r-1, c-1) and self.is_enemy(self.board[r-1][c-1]):
                moves.append(Move(r, c, r-1, c-1))
            if PieceMoveGenerator.is_valid(r-1, c+1) and self.is_enemy(self.board[r-1][c+1]):
                moves.append(Move(r, c, r-1, c+1))
        else:
            if PieceMoveGenerator.is_valid(r+1, c) and self.is_nothing(self.board[r+1][c]):
                moves.append(Move(r, c, r+1, c))
            if PieceMoveGenerator.is_valid(r+1, c-1) and self.is_nothing(self.board[r+1][c-1]):
                moves.append(Move(r, c, r+1, c-1))
            if PieceMoveGenerator.is_valid(r+1, c+1) and self.is_nothing(self.board[r+1][c+1]):
                moves.append(Move(r, c, r+1, c+1))
        return moves
