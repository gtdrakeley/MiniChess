from panalyze import PieceAnalyzer
from move import Move
from typing import List, Tuple


class BoardEvaluator(PieceAnalyzer):
    # piece_values = {'K': 200000,
    #                 'Q': 20000,
    #                 'B': 5000,
    #                 'N': 3000,
    #                 'R': 5000,
    #                 'P': 1000,
    #                 '.': 0}
    # piece_values['k'] = piece_values['K']
    # piece_values['q'] = piece_values['Q']
    # piece_values['b'] = piece_values['B']
    # piece_values['n'] = piece_values['N']
    # piece_values['r'] = piece_values['R']
    # piece_values['p'] = piece_values['P']
    piece_position_values = {'K': [[20000, 20000, 20000, 20000, 20000],
                                   [20000, 20000, 20000, 20000, 20000],
                                   [20000, 20000, 20000, 20000, 20000],
                                   [20000, 20000, 20000, 20000, 20000],
                                   [20000, 20000, 20000, 20000, 20000],
                                   [20000, 20000, 20000, 20000, 20000]],
                             'Q': [[2000, 2000, 2000, 2000, 2000],
                                   [2000, 2000, 2000, 2000, 2000],
                                   [2000, 2000, 2000, 2000, 2000],
                                   [2000, 2000, 2000, 2000, 2000],
                                   [2000, 2000, 2000, 2000, 2000],
                                   [2000, 2000, 2000, 2000, 2000]],
                             'B': [[500, 500, 500, 500, 500],
                                   [500, 500, 500, 500, 500],
                                   [500, 500, 500, 500, 500],
                                   [500, 500, 500, 500, 500],
                                   [500, 500, 500, 500, 500],
                                   [500, 500, 500, 500, 500]],
                             'N': [[300, 300, 300, 300, 300],
                                   [300, 300, 300, 300, 300],
                                   [300, 300, 300, 300, 300],
                                   [300, 300, 300, 300, 300],
                                   [300, 300, 300, 300, 300],
                                   [300, 300, 300, 300, 300]],
                             'R': [[500, 500, 500, 500, 500],
                                   [500, 500, 500, 500, 500],
                                   [500, 500, 500, 500, 500],
                                   [500, 500, 500, 500, 500],
                                   [500, 500, 500, 500, 500],
                                   [500, 500, 500, 500, 500]],
                             'P': [[100, 100, 100, 100, 100],
                                   [100, 100, 100, 100, 100],
                                   [100, 100, 100, 100, 100],
                                   [100, 100, 100, 100, 100],
                                   [100, 100, 100, 100, 100],
                                   [100, 100, 100, 100, 100]],
                             '.': [[0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0]]}
    piece_position_values['k'] = piece_position_values['K']
    piece_position_values['q'] = piece_position_values['Q']
    piece_position_values['b'] = piece_position_values['B']
    piece_position_values['n'] = piece_position_values['N']
    piece_position_values['r'] = piece_position_values['R']
    piece_position_values['p'] = piece_position_values['P']
    max_eval = (max(map(max, piece_position_values['K'])) +
                max(map(max, piece_position_values['Q'])) * 6 +
                max(map(max, piece_position_values['B'])) +
                max(map(max, piece_position_values['N'])) +
                max(map(max, piece_position_values['R'])))

    def __init__(self) -> None:
        super().__init__()
        self.white_score = 0
        self.black_score = 0
        self.eval_history = list()  # type: List[Tuple[int, int]]
        self.evaluate_board()

    @property
    def eval(self) -> int:
        return self.white_score - self.black_score if self.playing == 'W' else self.black_score - self.white_score

    def evaluate_board(self) -> None:
        self.white_score, self.black_score = 0, 0
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if piece in PieceAnalyzer.white_pieces:
                    self.white_score += BoardEvaluator.piece_position_values[piece][r][c]
                elif piece in PieceAnalyzer.black_pieces:
                    self.black_score += BoardEvaluator.piece_position_values[piece][5 - r][c]

    def move(self, mv: Move) -> None:
        self.eval_history.append((self.white_score, self.black_score))
        src_piece = self.board[mv.src_row][mv.src_column]
        dest_piece = self.board[mv.dest_row][mv.dest_column]
        if src_piece in PieceAnalyzer.white_pieces:
            self.white_score -= BoardEvaluator.piece_position_values[src_piece][mv.src_row][mv.src_column]
            self.black_score -= BoardEvaluator.piece_position_values[dest_piece][5-mv.dest_row][mv.dest_column]
            super().move(mv)
            src_piece = self.board[mv.dest_row][mv.dest_column]
            self.white_score += BoardEvaluator.piece_position_values[src_piece][mv.dest_row][mv.dest_column]
        else:
            self.white_score -= BoardEvaluator.piece_position_values[dest_piece][mv.dest_row][mv.dest_column]
            self.black_score -= BoardEvaluator.piece_position_values[src_piece][5-mv.src_row][mv.src_column]
            super().move(mv)
            src_piece = self.board[mv.dest_row][mv.dest_column]
            self.black_score += BoardEvaluator.piece_position_values[src_piece][5-mv.dest_row][mv.dest_column]

    def undo(self) -> None:
        super().undo()
        self.white_score, self.black_score = self.eval_history.pop()

    def set_board(self, board_string: str) -> None:
        super().set_board(board_string)
        self.evaluate_board()
