import chessai
import inline
from random import random


p1_time = p2_time = 300000
ai = chessai.ChessAI()

if random() <= 0.5:
    print('ChessAI is W')
    print()
    print()
    print()
    while True:
        print()
        print()
        print(ai.board_get()[:-1])
        start = inline.milliseconds()
        ai.move_alphabeta(-1, p1_time)
        p1_time -= inline.milliseconds() - start
        if p1_time < 0:
            print('B wins via time!')
            break
        elif ai.winner() == '=':
            print('Tie game!')
            break
        elif ai.winner() != '?':
            print('W wins by taking the king!')
            break
        inline.set_board(ai.board_get())
        print()
        print()
        print(inline.get_board()[:-1])
        start = inline.milliseconds()
        inline.move_alphabeta(-1, p2_time)
        p2_time -= inline.milliseconds() - start
        if p2_time < 0:
            print('W wins via time!')
            break
        elif inline.winner() == '=':
            print('Tie game!')
            break
        elif inline.winner() != '?':
            print('B wins by taking the king!')
            break
        ai.board_set(inline.get_board())
else:
    print('Inline is W')
    print()
    print()
    print()
    while True:
        print()
        print()
        print(inline.get_board()[:-1])
        start = inline.milliseconds()
        inline.move_alphabeta(-1, p2_time)
        p2_time -= inline.milliseconds() - start
        if p2_time < 0:
            print('W wins via time!')
            break
        elif inline.winner() == '=':
            print('Tie game!')
            break
        elif inline.winner() != '?':
            print('B wins by taking the king!')
            break
        ai.board_set(inline.get_board())
        print()
        print()
        print(ai.board_get()[:-1])
        start = inline.milliseconds()
        ai.move_alphabeta(-1, p1_time)
        p1_time -= inline.milliseconds() - start
        if p1_time < 0:
            print('B wins via time!')
            break
        elif ai.winner() == '=':
            print('Tie game!')
            break
        elif ai.winner() != '?':
            print('W wins by taking the king!')
            break
        inline.set_board(ai.board_get())
