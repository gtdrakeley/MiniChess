import panalyze


class BoardEvaluator(panalyze.PieceAnalyzer):
    piece_values = {'k': 200000, 'K': 200000,
                    'q': 20000, 'Q': 20000,
                    'b': 5000, 'B': 5000,
                    'n': 3000, 'N': 3000,
                    'r': 5000, 'R': 5000,
                    'p': 1000, 'P': 1000}

    def __init__(self):
        super().__init__()

    def eval(self):
        white_score, black_score = 0, 0
        for row in self.board:
            for piece in row:
                piece = chr(piece)
                if piece in BoardEvaluator.white_pieces:
                    white_score += BoardEvaluator.piece_values[piece]
                elif piece in BoardEvaluator.black_pieces:
                    black_score += BoardEvaluator.piece_values[piece]
        return white_score - black_score if self.playing == 'W' else black_score - white_score

