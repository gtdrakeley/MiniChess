import panalyze
import move
from typing import List, Tuple


class BoardEvaluator(panalyze.PieceAnalyzer):
    piece_values = {'k': 200000, 'K': 200000,
                    'q': 20000, 'Q': 20000,
                    'b': 5000, 'B': 5000,
                    'n': 3000, 'N': 3000,
                    'r': 5000, 'R': 5000,
                    'p': 1000, 'P': 1000,
                    '.': 0}

    def __init__(self) -> None:
        super().__init__()
        self.white_score = 0  # type: int
        self.black_score = 0
        self.eval_history = list()  # type: List[Tuple[int, int]]
        self.evaluate_board()

    @property
    def eval(self):
        return self.white_score - self.black_score if self.playing == 'W' else self.black_score - self.white_score

    def evaluate_board(self) -> None:
        self.white_score, self.black_score = 0, 0
        for row in self.board:
            for piece in row:
                piece = chr(piece)
                if piece in BoardEvaluator.white_pieces:
                    self.white_score += BoardEvaluator.piece_values[piece]
                elif piece in BoardEvaluator.black_pieces:
                    self.black_score += BoardEvaluator.piece_values[piece]

    def save(self, mv: move.Move) -> None:
        super().save(mv)
        self.eval_history.append((self.white_score, self.black_score))
        src_piece = self.board[mv.src_row][mv.src_column]
        dest_piece = self.black_score[mv.dest_row][mv.dest_column]
        if src_piece in BoardEvaluator.white_pieces:
            self.black_score -= BoardEvaluator.piece_values[dest_piece]
            if src_piece == 'P':
                self.white_score -= BoardEvaluator.piece_values['P'] - BoardEvaluator.piece_values['Q']
        else:
            self.white_score -= BoardEvaluator.piece_values[dest_piece]
            if src_piece == 'p':
                self.black_score -= BoardEvaluator.piece_values['p'] - BoardEvaluator.piece_values['q']

    def undo(self):
        super().undo()
        self.white_pieces, self.black_score = self.eval_history.pop()

