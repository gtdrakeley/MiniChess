import panalyze
import move
from typing import List, Tuple


class BoardEvaluator(panalyze.PieceAnalyzer):
    piece_values = {'K': 200000,
                    'Q': 20000,
                    'B': 5000,
                    'N': 3000,
                    'R': 5000,
                    'P': 1000,
                    '.': 0}
    piece_values['k'] = piece_values['K']
    piece_values['q'] = piece_values['Q']
    piece_values['b'] = piece_values['B']
    piece_values['n'] = piece_values['N']
    piece_values['r'] = piece_values['R']
    piece_values['p'] = piece_values['P']
    position_value_modifiers = {'K': [[1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1]],
                                'Q': [[1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1]],
                                'B': [[1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1]],
                                'N': [[1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1]],
                                'R': [[1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1]],
                                'P': [[1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1]],
                                '.': [[0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0]]}
    position_value_modifiers['k'] = position_value_modifiers['K']
    position_value_modifiers['q'] = position_value_modifiers['Q']
    position_value_modifiers['b'] = position_value_modifiers['B']
    position_value_modifiers['n'] = position_value_modifiers['N']
    position_value_modifiers['r'] = position_value_modifiers['R']
    position_value_modifiers['p'] = position_value_modifiers['P']

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
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                piece = chr(piece)
                if piece in BoardEvaluator.white_pieces:
                    self.white_score += int(BoardEvaluator.piece_values[piece] *
                                            BoardEvaluator.position_value_modifiers[piece][r][c])
                elif piece in BoardEvaluator.black_pieces:
                    self.black_score += int(BoardEvaluator.piece_values[piece] *
                                            BoardEvaluator.position_value_modifiers[piece][5-r][c])

    def move(self, mv: move.Move) -> None:
        self.eval_history.append((self.white_score, self.black_score))
        src_piece = self.board[mv.src_row][mv.src_column]
        dest_piece = self.board[mv.dest_row][mv.dest_column]
        if src_piece in BoardEvaluator.white_pieces:
            self.white_score -= int(BoardEvaluator.piece_values[src_piece] *
                                    BoardEvaluator.position_value_modifiers[src_piece][mv.src_row][mv.src_column])
            self.black_score -= int(BoardEvaluator.piece_values[dest_piece] *
                                    BoardEvaluator.position_value_modifiers[dest_piece][5-mv.dest_row][mv.dest_column])
            super().move(mv)
            self.white_score += int(BoardEvaluator.piece_values[src_piece] *
                                    BoardEvaluator.position_value_modifiers[src_piece][mv.dest_row][mv.dest_column])
        else:
            self.white_score -= int(BoardEvaluator.piece_values[dest_piece] *
                                    BoardEvaluator.position_value_modifiers[dest_piece][mv.dest_row][mv.dest_column])
            self.black_score -= int(BoardEvaluator.piece_values[src_piece] *
                                    BoardEvaluator.position_value_modifiers[src_piece][5-mv.src_row][mv.src_column])
            super().move(mv)
            self.black_score += int(BoardEvaluator.piece_values[src_piece] *
                                    BoardEvaluator.position_value_modifiers[src_piece][mv.dest_row][mv.dest_column])

    def undo(self):
        super().undo()
        self.white_pieces, self.black_score = self.eval_history.pop()

    def set_board(self, board_string: str) -> None:
        super().set_board(board_string)
        self.evaluate_board()

