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
import inline
'''
loop1 = '''
ai.move_alphabeta(depth, 0)
if ai.winner() != '?':
 ai.reset()
 '''.replace('depth', str(depth))
loop2 = '''
inline.move_alphabeta(depth, 0)
if inline.winner() != '?':
 inline.reset()
 '''.replace('depth', str(depth))

print('Benchmarking {} moves with depth {} ({} games max)...'.format(n, depth, n/80))
print('\tChessAI: {} seconds'.format(timeit(loop1, setup=setup1, number=n)))
print('\tAI: {} seconds'.format(timeit(loop1, setup=setup2, number=n)))
print('\tInline: {} seconds'.format(timeit(loop2, setup=setup3, number=n)))
