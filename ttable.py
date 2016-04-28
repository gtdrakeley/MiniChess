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
    def __init__(self, hash_key, score, move, depth, flag, ancient):
        super().__init__(hash_key, score, move, depth, flag)
        self.ancient = ancient
        self.hits = 1
        self.aging_factor = 1

    @staticmethod
    def fromttentry(entry, ancient):
        return TTEntryAging(entry.hash_key, entry.score, entry.move, entry.depth, entry.flag, ancient)

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
            if self.entries[(self.current + offset) % len(self.entries)] is None:
                continue
            if hash_key == self.entries[(self.current + offset) % len(self.entries)].hash_key:
                self.current += offset + 1
                return self.entries[(self.current - 1) % len(self.entries)]
        else:
            return None

    def store(self, entry):
        self.entries[self.current % len(self.entries)] = entry
        self.current += 1


class TTBucketAging:
    def __init__(self, size):
        self.entries = [None] * size
        self.current = 0

    def lookup(self, hash_key, ancient):
        for offset in range(len(self.entries)):
            if self.entries[(self.current + offset) % len(self.entries)] is None:
                continue
            elif hash_key == self.entries[(self.current + offset) % len(self.entries)].hash_key:
                self.current += offset + 1
                self.entries[(self.current - 1) % len(self.entries)].hit()
                self.entries[(self.current - 1) % len(self.entries)].ancient = ancient
                return self.entries[(self.current - 1) % len(self.entries)]
        else:
            return None

    def store(self, entry, ancient):
        for offset in range(len(self.entries)):
            if self.entries[(self.current + offset) % len(self.entries)] is None:
                self.entries[(self.current + offset) % len(self.entries)] = entry
                self.current += offset + 1
            elif self.entries[(self.current + offset) % len(self.entries)].ancient != ancient:
                self.entries[(self.current + offset) % len(self.entries)] = entry
                self.current += offset + 1
                return True
            elif self.entries[(self.current + offset) % len(self.entries)].is_old():
                self.entries[(self.current + offset) % len(self.entries)] = entry
                self.current += offset + 1
                return True
            elif entry.depth > self.entries[(self.current + offset) % len(self.entries)].depth:
                self.entries[(self.current + offset) % len(self.entries)] = entry
                self.current += offset + 1
                return True
        else:
            return False


def generate_zobrist_hash_values(max_hash_value):
    piece_hash_values = dict.fromkeys(list('KQBNRPkqbnrp'))
    for key in piece_hash_values:
        piece_hash_values[key] = list()
        for row in range(6):
            piece_hash_values[key].append(list())
            for column in range(5):
                piece_hash_values[key][row].append(random.randint(0, max_hash_value))
    return piece_hash_values


class TranspositionTable:
    max_hash_value = 0xFFFFFFFF
    white_hash_value = random.randint(0, max_hash_value)
    black_hash_value = random.randint(0, max_hash_value)
    player_toggle_hash_value = white_hash_value ^ black_hash_value
    piece_hash_values = generate_zobrist_hash_values(max_hash_value)
    default = [[0] * 5] * 6

    def __init__(self, table_size, depth_bucket_size=2, bucket_size=1):
        self.size = table_size
        self.index_mask = (1 << (self.size - 1).bit_length()) - 1
        self.hash_value = 0
        self.depth_buckets = list()
        self.buckets = list()
        self.history = list()
        self.ancient = 0
        for _ in range(table_size):
            self.depth_buckets.append(TTBucketAging(depth_bucket_size))
            self.buckets.append(TTBucket(bucket_size))

    def hash_board(self, playing, board):
        self.hash_value = 0
        if playing == 'W':
            self.hash_value ^= TranspositionTable.white_hash_value
        else:
            self.hash_value ^= TranspositionTable.black_hash_value
        for r, row in enumerate(board):
            for c, piece in enumerate(row):
                self.hash_value ^= (TranspositionTable.piece_hash_values.get(chr(piece), TranspositionTable.default)
                                    [r][c])

    def update(self, positions, pieces):
        self.history.append(self.hash_value)
        pairs = zip(positions, pieces)
        for pair in pairs:
            position, piece = pair
            self.hash_value ^= (TranspositionTable.piece_hash_values.get(piece, TranspositionTable.default)
                                [position.row][position.column])
        self.hash_value ^= TranspositionTable.player_toggle_hash_value

    def undo(self):
        self.hash_value = self.history.pop()

    def lookup(self):
        index = (self.hash_value & self.index_mask) % self.size
        entry = self.depth_buckets[index].lookup(self.hash_value, self.ancient)
        if not entry:
            entry = self.buckets[index].lookup(self.hash_value)
        return entry

    def store(self, score, move, depth, flag):
        index = (self.hash_value & self.index_mask) % self.size
        entry = TTEntry(self.hash_value, score, move, depth, flag)
        if not self.depth_buckets[index].store(TTEntryAging.fromttentry(entry, self.ancient), self.ancient):
            self.buckets[index].store(entry)

    def reset(self):
        self.ancient ^= 1

