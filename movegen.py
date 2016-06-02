import boardeval
import panalyze
import move
import random


class MoveGenerator(boardeval.BoardEvaluator):
    def __init__(self):
        super().__init__()

    def moves(self) -> list[move.Move]:
        moves = list()
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if self.playing == 'W' and piece in panalyze.PieceAnalyzer.white_pieces:
                    moves.extend(self.piece_moves(piece, r, c))
                elif self.playing == 'B' and piece in panalyze.PieceAnalyzer.black_pieces:
                    moves.extend(self.piece_moves(piece, r, c))
        return moves

    def moves_shuffled(self) -> list[move.Move]:
        moves = self.moves()
        random.shuffle(moves)
        return moves

    def moves_evaluated(self):
        moves = self.moves_shuffled()
        evals = list()
        for mv in moves:
            self.move(mv)
            evals.append(self.eval())
            self.undo()
        zipped = list(zip(evals, moves))
        zipped.sort(key=lambda e: e[0])
        evals, moves = zip(*tuple(zipped))
        return list(moves)

