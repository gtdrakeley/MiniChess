import itertools


class Move:
    char_to_column = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
    column_to_char = {v: k for k, v in char_to_column.items()}

    def __init__(self, src_row: int, src_column: int, dest_row: int, dest_column: int) -> None:
        if src_row < 0 or src_row > 5:
            raise ValueError('Source row is out of bounds')
        elif src_column < 0 or src_column > 4:
            raise ValueError('Source column is out of bounds')
        elif dest_row < 0 or dest_row > 5:
            raise ValueError('Destination row is out of bounds')
        elif dest_column < 0 or dest_column > 4:
            raise ValueError('Destination column is out of bounds')
        self.data = src_row | src_column << 3 | dest_row << 6 | dest_column << 9

    @staticmethod
    def fromstr(move: str) -> 'Move':
        coords = list(itertools.chain.from_iterable([list(pos) for pos in move.strip().split('-')]))
        return Move(6 - int(coords[1]), Move.char_to_column[coords[0]],
                    6 - int(coords[3]), Move.char_to_column[coords[2]])

    def __str__(self) -> str:
        return '{}{}-{}{}\n'.format(Move.column_to_char[self.src_column], 6 - self.src_row,
                                    Move.column_to_char[self.dest_column], 6 - self.dest_row)

    @property
    def src_row(self) -> int:
        return self.data & 0x7

    @property
    def src_column(self) -> int:
        return (self.data & 0x38) >> 3

    @property
    def dest_row(self) -> int:
        return (self.data & 0x1C0) >> 6

    @property
    def dest_column(self) -> int:
        return (self.data & 0xE00) >> 9
