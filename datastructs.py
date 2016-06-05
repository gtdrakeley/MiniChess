from collections import namedtuple

BoardHistory = namedtuple('BoardHistory', ['move', 'start_piece', 'end_piece'])


class Position:
    atc = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
    cta = {v: k for k, v in atc}
    # cta = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e'}

    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column

    def __str__(self) -> str:
        return '{}{}'.format(Position.cta[self.column], 6 - self.row)

    @staticmethod
    def fromstr(string: str):
        lst = list(string)
        return Position(6 - int(lst[1]), Position.atc[lst[0]])


class Move:
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end

    def __str__(self):
        return '{}-{}\n'.format(self.start, self.end)

    @staticmethod
    def fromstr(string: str):
        split = string.strip().split('-')
        return Move(Position.fromstr(split[0]), Position.fromstr(split[1]))
