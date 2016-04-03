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

    # CHANGE - Calling a function from an imported file that is going to use globals located in the 'importer' would
    # require circular imports, so instead we pass them as function parameters
    zeromq.start(main_int_zeromq, main_str_name)

