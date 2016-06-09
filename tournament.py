import chessai
import chess
import chessaiv2
from random import random
from sys import argv


p1_time = p2_time = int(argv[1])
ai = chessai.ChessAI()
ai2 = chessaiv2.ChessAIV2()

if random() <= 0.5:
    print('ChessAI is W')
    print()
    print()
    print()
    while True:
        print()
        print()
        print(ai.board_get()[:-1])
        start = chess.milliseconds()
        ai.move_alphabeta(-1, p1_time)
        delta = chess.milliseconds() - start
        if p1_time < 0:
            print('B-ChessAIV2 wins via time!')
            break
        elif ai.winner() == '=':
            print('Tie game!')
            break
        elif ai.winner() != '?':
            print('W-ChessAI wins by taking the king!')
            break
        p1_time -= delta
        print('W Remaining Time: {}'.format(p1_time))
        ai2.set_board(ai.board_get())
        assert ai.eval() == ai2.evaluation(), 'Eval mismatch - AI: {} vs AI2: {}'.format(ai.eval(), ai2.evaluation())
        print()
        print()
        print(ai2.get_board()[:-1])
        start = chess.milliseconds()
        ai2.move_alphabeta(-1, p2_time)
        delta = chess.milliseconds() - start
        if p2_time < 0:
            print('W-ChessAI wins via time!')
            break
        elif ai2.winner() == '=':
            print('Tie game!')
            break
        elif ai2.winner() != '?':
            print('B-ChessAIV2 wins by taking the king!')
            break
        p2_time -= delta
        print('B Remaining Time: {}'.format(p2_time))
        ai.board_set(ai2.get_board())
        assert ai.eval() == ai2.evaluation(), 'Eval mismatch - AI: {} vs AI2: {}'.format(ai.eval(), ai2.evaluation())
else:
    print('ChessAIV2 is W')
    print()
    print()
    print()
    while True:
        print()
        print()
        print(ai2.get_board()[:-1])
        start = chess.milliseconds()
        ai2.move_alphabeta(-1, p2_time)
        delta = chess.milliseconds() - start
        if p2_time < 0:
            print('B-ChessAI wins via time!')
            break
        elif ai2.winner() == '=':
            print('Tie game!')
            break
        elif ai2.winner() != '?':
            print('W-Inline wins by taking the king!')
            break
        p2_time -= delta
        print('W Remaining Time: {}'.format(p2_time))
        ai.board_set(ai2.get_board())
        assert ai.eval() == ai2.evaluation(), 'Eval mismatch - AI: {} vs AI2: {}'.format(ai.eval(), ai2.evaluation())
        print()
        print()
        print(ai.board_get()[:-1])
        start = chess.milliseconds()
        ai.move_alphabeta(-1, p1_time)
        delta = chess.milliseconds() - start
        if p1_time < 0:
            print('W-Inline wins via time!')
            break
        elif ai.winner() == '=':
            print('Tie game!')
            break
        elif ai.winner() != '?':
            print('B-ChessAI wins by taking the king!')
            break
        p1_time -= delta
        print('B Remaining Time: {}'.format(p1_time))
        ai2.set_board(ai.board_get())
        assert ai.eval() == ai2.evaluation(), 'Eval mismatch - AI: {} vs AI2: {}'.format(ai.eval(), ai2.evaluation())
"""
if random() <= 0.5:
    print('ChessAI is W')
    print()
    print()
    print()
    while True:
        print()
        print()
        print(ai.board_get()[:-1])
        start = chess.milliseconds()
        ai.move_alphabeta(-1, p1_time)
        p1_time -= chess.milliseconds() - start
        if p1_time < 0:
            print('B-Inline wins via time!')
            break
        elif ai.winner() == '=':
            print('Tie game!')
            break
        elif ai.winner() != '?':
            print('W-ChessAI wins by taking the king!')
            break
        chess.set_board(ai.board_get())
        print()
        print()
        print(chess.get_board()[:-1])
        start = chess.milliseconds()
        chess.move_alphabeta(-1, p2_time)
        p2_time -= chess.milliseconds() - start
        if p2_time < 0:
            print('W-ChessAI wins via time!')
            break
        elif chess.winner() == '=':
            print('Tie game!')
            break
        elif chess.winner() != '?':
            print('B-Inline wins by taking the king!')
            break
        ai.board_set(chess.get_board())
else:
    print('Inline is W')
    print()
    print()
    print()
    while True:
        print()
        print()
        print(chess.get_board()[:-1])
        start = chess.milliseconds()
        chess.move_alphabeta(-1, p2_time)
        p2_time -= chess.milliseconds() - start
        if p2_time < 0:
            print('B-ChessAI wins via time!')
            break
        elif chess.winner() == '=':
            print('Tie game!')
            break
        elif chess.winner() != '?':
            print('W-Inline wins by taking the king!')
            break
        ai.board_set(chess.get_board())
        print()
        print()
        print(ai.board_get()[:-1])
        start = chess.milliseconds()
        ai.move_alphabeta(-1, p1_time)
        p1_time -= chess.milliseconds() - start
        if p1_time < 0:
            print('W-Inline wins via time!')
            break
        elif ai.winner() == '=':
            print('Tie game!')
            break
        elif ai.winner() != '?':
            print('B-ChessAI wins by taking the king!')
            break
        chess.set_board(ai.board_get())
"""
print()
print()
print('W Time Remaining: {}'.format(p1_time))
print('B Time Remaining: {}'.format(p2_time))
print('Difference (W minus B): {}'.format(p1_time-p2_time))
