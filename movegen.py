from piecemovegen import PieceMoveGenerator
from panalyze import PieceAnalyzer
from move import Move
from typing import List

import random


class MoveGenerator(PieceMoveGenerator):
    def __init__(self) -> None:
        super().__init__()

    def moves(self) -> List[Move]:
        moves = list()
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if self.playing == 'W' and piece in PieceAnalyzer.white_pieces:
                    moves.extend(self.piece_moves(piece, r, c))
                elif self.playing == 'B' and piece in PieceAnalyzer.black_pieces:
                    moves.extend(self.piece_moves(piece, r, c))
        return moves

    def moves_shuffled(self) -> List[Move]:
        moves = self.moves()
        random.shuffle(moves)
        return moves

    def moves_evaluated(self) -> List[Move]:
        moves = self.moves_shuffled()
        evals = list()
        for mv in moves:
            self.move(mv)
            evals.append(self.eval)
            self.undo()
        zipped = list(zip(evals, moves))
        zipped.sort(key=lambda e: e[0])
        evals, moves = zip(*tuple(zipped))
        return list(moves)
