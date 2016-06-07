from timeit import timeit
from sys import argv


n = int(eval(argv[1:]))
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
ai.move_alphabeta(5, 0)
if ai.winner() != '?':
 ai.reset()
 '''
loop2 = '''
inline.move_alphabeta(5, 0)
if inline.winner() != '?':
 inline.reset()
 '''

print('Benchmarking {} moves ({} games)...'.format(n, 80/n))
print('\tChessAI: {} seconds'.format(timeit(loop1, setup=setup1, number=n)))
print('\tAI: {} seconds'.format(timeit(loop1, setup=setup2, number=n)))
print('\tInline: {} seconds'.format(timeit(loop2, setup=setup3, number=n)))
