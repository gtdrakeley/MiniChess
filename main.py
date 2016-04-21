import random
# CHANGE - Python 3 does not have an 'execfile' function, so we use imports instead
import chess
import zeromq


main_int_zeromq = 54361 # CHANGE THIS - OPTIONAL
main_str_name = 'gtdminichess' # CHANGE THIS - REQUIRED

if __name__ == '__main__':
    assert main_int_zeromq > 1024
    assert main_int_zeromq < 65535

    assert len(main_str_name) > 2
    assert len(main_str_name) < 16
    assert ' ' not in main_str_name

    random.seed()

    from time import sleep
    from chessai import ChessAI
    ai = ChessAI()
    while ai.winner() == '?':
        print('{} playing turn #{}'.format(ai.playing, ai.turn))
        for row in ai.board:
            print('\t' + row.decode())
        move = ai.moves_shuffled()[0]
        print('Taking move {}'.format(move))
        print()
        ai.move(move)
    print('{} wins!'.format(ai.winner()))
    print('Final board state:')
    for row in ai.board:
        print('\t' + row.decode())
    sleep(10)


    # CHANGE - Calling a function from an imported file that is going to use globals located in the 'importer' would
    # require circular imports, so instead we pass them as function parameters
    zeromq.start(main_int_zeromq, main_str_name)

