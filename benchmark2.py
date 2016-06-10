from timeit import timeit
from sys import argv
import chessaiv2

n = int(eval(argv[1]))
depth = int(eval(argv[2]))

setup1 = '''
import chessai
ai = chessai.ChessAI()'''
setup2 = '''
import chessaiv2
ai = chessaiv2.ChessAIV2()'''
setup3 = '''
import cai
ai = cai.AI()'''
setup4 = '''
import chess'''

print('Generating random board state...', end='')
ai = chessaiv2.ChessAIV2()
while ai.turn < 20:
    ai.move_alphabeta(5, 0)
    if ai.winner() != '?':
        ai.reset()
board = ai.get_board()
print('Done')
loop1 = '''
ai.set_board(brd)
ai.move_alphabeta(depth, 0)'''.replace('brd', board).replace('depth', str(depth))
loop2 = '''
chess.set_board(brd)
chess.move_alphabeta(depth, 0)'''.replace('brd', board).replace('depth', str(depth))
print('Calculating time required to set the board for each AI...', end='')
chessai_set_time = timeit('ai.set_board(brd)'.replace('brd', board), setup=setup1, number=n)
chessaiv2_set_time = timeit('ai.set_board(brd)'.replace('brd', board), setup=setup2, number=n)
ai_set_time = timeit('ai.set_board(brd)'.replace('brd', board), setup=setup3, number=n)
chess_set_time = timeit('chess.set_board(brd)'.replace('brd', board), setup=setup4, number=n)
print('Done')
print('Benchmarking {} moves with depth {} ({} games max)...'.format(n, depth, n/80))
print('\tChessAI: {} seconds'.format(timeit(loop1, setup=setup1, number=n)-chess_set_time))
print('\tChessAIV2: {} seconds'.format(timeit(loop1, setup=setup2, number=n)-chessaiv2_set_time))
print('\tAI: {} seconds'.format(timeit(loop1, setup=setup3, number=n)-ai_set_time))
print('\tChess: {} seconds'.format(timeit(loop2, setup=setup4, number=n)-chess_set_time))
