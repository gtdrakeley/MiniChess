from movegen import MoveGenerator
from boardeval import BoardEvaluator


class AI(MoveGenerator):
    def __init__(self) -> None:
        super().__init__()

    def move_random(self) -> str:
        mv = self.moves_shuffled()[0]
        self.move(mv)
        return str(mv)

    def move_greedy(self) -> str:
        mv = self.moves_evaluated()[0]
        self.move(mv)
        return str(mv)

    def move_negamax(self, depth: int, duration: int) -> str:
        best = None
        score = -BoardEvaluator.max_eval
        for mv in self.moves_shuffled():
            self.move(mv)
            temp = -self.negamax(depth-1, duration)
            self.undo()
            if temp > score:
                best, score = mv, temp
        self.move(best)
        return str(best)

    def negamax(self, depth: int, duration: int) -> int:
        if depth == 0 or self.winner() != '?':
            return self.eval
        score = -BoardEvaluator.max_eval
        for mv in self.moves_shuffled():
            self.move(mv)
            score = max(score, -self.negamax(depth-1, duration))
            self.undo()
        return score

    def move_alphabeta(self, depth, duration) -> str:
        best = None
        alpha = -BoardEvaluator.max_eval
        beta = BoardEvaluator.max_eval
        # temp = 0
        for move in self.moves_evaluated():
            self.move(move)
            temp = -self.alphabeta(depth - 1, duration, -beta, -alpha)
            self.undo()
            if temp > alpha:
                best = move
                alpha = temp
        self.move(best)
        return str(best)

    def alphabeta(self, depth, duration, alpha: int, beta: int) -> int:
        if depth == 0 or self.winner() != '?':
            return self.eval
        score = -BoardEvaluator.max_eval
        for mv in self.moves_evaluated():
            self.move(mv)
            score = max(score, -self.alphabeta(depth - 1, duration, -beta, -alpha))
            self.undo()
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return score
