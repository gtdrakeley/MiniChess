# CHANGES - functions naming convention changed to remove 'chess'.  As we are now using imports, functions will be
# be called using [filename].[function] style so instead of 'chess_moves()' we will have 'chess.moves()'.  Variable
# and function naming also changed to conform to PEP8 standards (no camelcase, underscores separating words when
# appropriate)

import random


def reset():
    # reset the state of the game / your internal variables - note that this function is highly dependent on your
    # implementation

    pass


def board_get():
    # return the state of the game - one example is given below - note that the state has exactly 40 or 41 characters

    str_out = ''

    str_out += '1 W\n'
    str_out += 'kqbnr\n'
    str_out += 'ppppp\n'
    str_out += '.....\n' * 2
    str_out += 'PPPPP\n'
    str_out += 'RNBQK\n'

    return str_out


def board_set(str_in):
    # read the state of the game from the provided argument and set your internal variables accordingly - note that the
    # state has exactly 40 or 41 characters

    pass


def winner():
    # determine the winner of the current states of the game and return '?' or '=' or 'W' or 'B' - note that we are
    # returning a character and not a string
    
    return '?'
    pass


def is_valid(int_x, int_y):
    if int_x < 0:
        return False

    elif int_x > 4:
        return False

    elif int_y < 0:
        return False

    elif int_y > 5:
        return False

    return True


def is_enemy(str_piece):
    # with reference to the state of the game, return whether the provided argument is a piece from the side not on
    # move - note that we could but should not use the other is() functions in here but probably

    return False


def is_own(str_piece):
    # with reference to the state of the game, return whether the provided argument is a piece from the side on move -
    # note that we could but should not use the other is() functions in here but probably

    return False


def is_nothing(str_piece):
    # return whether the provided argument is not a piece / is an empty field - note that we could but should not use
    # the other is() functions in here but probably

    return False


def eval():
    # with reference to the state of the game, return the evaluation score of the side on move - note that positive
    # means an advantage while negative means a disadvantage

    return 0


def moves():
    # with reference to the state of the game and return the possible moves - one example is given below - note that a
    # move has exactly 6 characters

    str_out = list()

    str_out.append('a5-a4\n')
    str_out.append('b5-b4\n')
    str_out.append('c5-c4\n')
    str_out.append('d5-d4\n')
    str_out.append('e5-e4\n')
    str_out.append('b6-a4\n')
    str_out.append('b6-e4\n')

    return str_out


def moves_shuffled():
    # with reference to the state of the game, determine the possible moves and shuffle them before returning them- note
    # that you can call the chess_moves() function in here

    return []


def moves_evaluated():
    # with reference to the state of the game, determine the possible moves and sort them in order of an increasing
    # evaluation score before returning them - note that you can call the chess_moves() function in here

    return []


def move(str_in):
    # perform the supplied move (for example 'a5-a4\n') and update the state of the game / your internal variables
    # accordingly - note that it advised to do a sanity check of the supplied move

    pass


def move_random():
    # perform a random move and return it - one example output is given below - note that you can call the
    # chess_movesShuffled() function as well as the chess_move() function in here

    return 'c5-c4\n'


def move_greedy():
    # perform a greedy move and return it - one example output is given below - note that you can call the
    # chess_movesEvaluated() function as well as the chess_move() function in here

    return 'c5-c4\n'


def move_negamax(depth, duration):
    # perform a negamax move and return it - one example output is given below - note that you can call the the other
    # functions in here

    return 'c5-c4\n'


def move_alphabeta(depth, duration):
    # perform a alphabeta move and return it - one example output is given below - note that you can call the the other
    # functions in here

    return 'c5-c4\n'


def undo():
    # undo the last move and update the state of the game / your internal variables accordingly - note that you need to
    # maintain an internal variable that keeps track of the previous history for this

    pass

