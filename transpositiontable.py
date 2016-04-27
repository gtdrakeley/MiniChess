import random

EXACT = 0
LOWER_BOUND = 1
UPPER_BOUND = 2


class TTEntry:
    def __init__(self, hash_key, score, move, depth, flag):
        self.hash_key = hash_key
        self.score = score
        self.move = move
        self.depth = depth
        self.flag = flag


class TTEntryAging(TTEntry):
    def __init__(self, hash_key, score, move, depth, flag):
        super().__init__(hash_key, score, move, depth, flag)
        self.hits = 1
        self.aging_factor = 1

    @staticmethod
    def fromttentry(entry):
        return TTEntryAging(entry.hash_key, entry.score, entry.move, entry.depth, entry.flag)

    def is_old(self):
        if self.hits <= 0:
            return True
        else:
            self.hits = max(0, self.hits - self.aging_factor)
            self.aging_factor *= 2
            return False

    def hit(self):
        self.hits += 1
        self.aging_factor = max(1, self.aging_factor // 2)


class TTBucket:
    def __init__(self, size):
        self.entries = [None] * size
        self.current = 0

    def lookup(self, hash_key):
        for offset in range(len(self.entries)):
            if hash_key == self.entries[(self.current + offset) % len(self.entries)].hash_key:
                self.current += offset
                return self.entries[self.current]
        else:
            return None

    def store(self, entry):
        self.entries[self.current % len(self.entries)] = entry
        self.current += 1


class TTBucketAging(TTBucket):
    def __init__(self, size):
        super().__init__(size)

    def lookup(self, hash_key):
        for offset in range(len(self.entries)):
            if hash_key == self.entries[(self.current + offset) % len(self.entries)].hash_key:
                self.current += offset
                self.entries[self.current].hit()
                return self.entries[self.current]
        else:
            return None

    def store(self, entry):
        for offset in range(len(self.entries)):
            if self.entries[self.current + offset].is_old():
                self.entries[self.current + offset] = entry
                self.current += offset + 1
                return True
            elif entry.depth > self.entries[self.current + offset].depth:
                self.entries[self.current + offset] = entry
                self.current += offset + 1
                return True
        else:
            return False


def generate_zobrist_hash_values(max_hash_value):
    piece_hash_values = dict.fromkeys(list('KQBNRkqbnr'))
    for key in piece_hash_values:
        piece_hash_values[key] = list()
        for row in range(6):
            piece_hash_values[key].append(list())
            for column in range(5):
                piece_hash_values[key][row].append(random.randint(0, max_hash_value))
    return piece_hash_values


class TranspositionTable:
    max_hash_value = 0xFFFFFFFFFFFFFFFF
    white_hash_value = random.randint(0, max_hash_value)
    black_hash_value = random.randint(0, max_hash_value)
    player_toggle_hash_value = white_hash_value ^ black_hash_value
    piece_hash_values = generate_zobrist_hash_values(max_hash_value)
    default = [[0] * 5] * 6

    def __init__(self, table_size, depth_bucket_size=2, bucket_size=1):
        self.hash = 0 ^ TranspositionTable.white_hash_value
        initial_board = [list('kqbnr'),
                         list('ppppp'),
                         list('.....'),
                         list('.....'),
                         list('PPPPP'),
                         list('RNBQK')]
        for row in initial_board:
            for column in row:
                self.hash ^= TranspositionTable.piece_hash_values[initial_board[row][column]][row][column]
        self.depth_buckets = list()
        self.buckets = list()
        for _ in range(table_size):
            self.depth_buckets.append(TTBucketAging(depth_bucket_size))
            self.buckets.append(TTBucket(bucket_size))

    def update_hash(self, move, start_piece, end_piece):
        self.hash ^= ((TranspositionTable.piece_hash_values.get(start_piece, TranspositionTable.default)
                       [move.start.row][move.start.column]) ^
                      (TranspositionTable.piece_hash_values.get(end_piece, TranspositionTable.default)
                       [move.end.row][move.end.column]) ^
                      (TranspositionTable.piece_hash_values.get(start_piece, TranspositionTable.default)
                       [move.end.row][move.end.column]) ^
                      TranspositionTable.player_toggle_hash_value)

