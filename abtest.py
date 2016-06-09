import chessai
import chessaiv2

ai = chessai.ChessAI()
ai2 = chessaiv2.ChessAIV2()

same = 0
diff = 0
for i in range(100):
    for j in range(100):
        ai.move_alphabeta(3, 0)
        if ai.winner() != '?':
            ai.reset()
    ai2.set_board(ai.get_board())
    mv1 = ai.move_alphabeta(5, 0)
    mv2 = ai2.move_alphabeta(5, 0)
    if mv1 == mv2:
        same += 1
    else:
        diff += 1
print('Same: {}'.format(same))
print('Diff: {}'.format(diff))