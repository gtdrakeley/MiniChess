# CHANGES - functions naming convention changed to remove 'zeromq'.  As we are now using imports, functions will be
# be called using [filename].[function] style so instead of 'zeromq_start()' we will have 'zeromq.start()'.  Variable
# and function naming also changed to conform to PEP8 standards (no camelcase, underscores separating words when
# appropriate)

import json
import zmq
import chess

zeromq_bool_running = False


def start(main_int_zeromq, main_str_name):
    global zeromq_bool_running

    zeromq_bool_running = True

    context_handle = zmq.Context()
    socket_handle = context_handle.socket(zmq.PAIR)

    socket_handle.bind('tcp://*:' + str(main_int_zeromq))

    # CHANGES - json_out has a static number of fields that it modifies as needed to pass information back to the
    # framework.  For this reason, it never needs to be deleted and instead can be set up with all required keys before
    # entering the main loop.  This will save us some computation time as we never have to recreate the json_out
    # dictionary and dictionary assignment to already existing keys is very very fast.
    # After the below call to dict.fromkeys() all the values will be None.
    json_out = dict.fromkeys(['strOut', 'strReturn', 'boolReturn', 'intReturn', 'intOut'])

    while zeromq_bool_running:
        # CHANGES - json_in variable does not need to be set to None at the end of the file as this call will overwrite
        # the previous object and cause it to be garbage collected just the same.
        json_in = json.loads(socket_handle.recv())

        if json_in['strFunction'] == 'ping':
            json_out['strOut'] = main_str_name

        elif json_in['strFunction'] == 'chess_reset':
            chess.reset()

        elif json_in['strFunction'] == 'chess_boardGet':
            chess.board_get()

        elif json_in['strFunction'] == 'chess_boardSet':
            chess.board_set(json_in['strIn'])

        elif json_in['strFunction'] == 'chess_winner':
            json_out['strReturn'] = chess.winner()

        elif json_in['strFunction'] == 'chess_isValid':
            json_out['boolReturn'] = chess.is_valid(json_in['intX'], json_in['intY'])

        elif json_in['strFunction'] == 'chess_isEnemy':
            json_out['boolReturn'] = chess.is_enemy(json_in['strPiece'])

        elif json_in['strFunction'] == 'chess_isOwn':
            json_out['boolReturn'] == chess.is_own(json_in['strPiece'])

        elif json_in['strFunction'] == 'chess_isNothing':
            json_out['boolReturn'] = chess.is_nothing(json_in['strPiece'])

        elif json_in['strFunction'] == 'chess_eval':
            json_out['intReturn'] == chess.eval()

        elif json_in['strFunction'] == 'chess_moves':
            str_out = chess.moves()

            json_out['intOut'] = len(str_out)
            # CHANGES - this is a more Pythonic way of calling join
            json_out['strOut'] = ''.join(str_out)

        elif json_in['strFunction'] == 'chess_movesShuffled':
            str_out = chess.moves_shuffled()

            json_out['intOut'] = len(str_out)
            # CHANGES - this is a more Pythonic way of calling join
            json_out['strOut'] = ''.join(str_out)

        elif json_in['strFunction'] == 'chess_movesEvaluated':
            str_out = chess.moves_evaluated()

            json_out['intOut'] = len(str_out)
            # CHANGES - this is a more Pythonic way of calling join
            json_out['strOut'] = ''.join(str_out)

        elif json_in['strFunction'] == 'chess_move':
            chess.move(json_in['strIn'])

        elif json_in['strFunction'] == 'chess_moveRandom':
            json_out['strOut'] = chess.move_random()

        elif json_in['strFunction'] == 'chess_moveGreedy':
            json_out['strOut'] = chess.move_greedy()

        elif json_in['strFunction'] == 'chess_moveNegamax':
            json_out['strOut'] = chess.move_negamax(json_in['intDepth'], json_in['intDuration'])

        elif json_in['strFunction'] == 'chess_moveAlphabeta':
            json_out['strOut'] = chess.move_alphabeta(json_in['intDepth'], json_in['intDuration'])

        elif json_in['strFunction'] == 'chess_undo':
            chess.undo()

        socket_handle.send(json.dumps(json_out))

    socket_handle.close()
    context_handle.close()


def stop():
    global zeromq_bool_running

    zeromq_bool_running = False

