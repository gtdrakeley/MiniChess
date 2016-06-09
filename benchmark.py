from timeit import timeit
from sys import argv


n = int(eval(argv[1]))
depth = int(eval(argv[2]))
setup1 = '''
import chessai
ai = chessai.ChessAI()
'''
setup2 = '''
import cai
ai = cai.AI()
'''
setup3 = '''
import chess
'''
setup4 = '''
import chessaiv2
ai = chessaiv2.ChessAIV2()
'''
loop1 = '''
ai.move_alphabeta(depth, 0)
if ai.winner() != '?':
 ai.reset()
'''.replace('depth', str(depth))
loop2 = '''
chess.move_alphabeta(depth, 0)
if chess.winner() != '?':
 chess.reset()
'''.replace('depth', str(depth))

print('Benchmarking {} moves with depth {} ({} games max)...'.format(n, depth, n/80))
print('\tChessAI: {} seconds'.format(timeit(loop1, setup=setup1, number=n)))
print('\tAI: {} seconds'.format(timeit(loop1, setup=setup2, number=n)))
print('\tChess: {} seconds'.format(timeit(loop2, setup=setup3, number=n)))
print('\tChessAIV2: {} seconds'.format(timeit(loop1, setup=setup4, number=n)))
