from boardhistory import BoardHistory


class PieceAnalyzer(BoardHistory):
    white_pieces = 'KQBNRP'
    black_pieces = 'kqbnrp'

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def is_nothing(piece: str) -> bool:
        return True if piece == '.' else False

    def is_enemy(self, piece: str) -> bool:
        if self.playing == 'W' and piece in PieceAnalyzer.black_pieces:
            return True
        elif self.playing == 'B' and piece in PieceAnalyzer.white_pieces:
            return True
        else:
            return False

    def is_own(self, piece: str) -> bool:
        if self.playing == 'W' and piece in PieceAnalyzer.white_pieces:
            return True
        elif self.playing == 'B' and piece in PieceAnalyzer.black_pieces:
            return True
        else:
            return False
