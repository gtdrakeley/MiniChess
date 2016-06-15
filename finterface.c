#include "finterface.h"

#include <stdlib.h>
#include <stdio.h>

#include "main.h"
#include "chessai.h"
#include "move.h"
#include "debug.h"


void    frameworkInterface_reset(ChessAI* ai) {
    ChessAI_reset(ai);
}

void    frameworkInterface_getBoard(ChessAI* ai, char* out) {
    ChessAI_getBoard(ai, out);
}

void    frameworkInterface_setBoard(ChessAI* ai, char* in) {
    ChessAI_setBoard(ai, in);
}

char    frameworkInterface_winner(ChessAI* ai) {
    return ChessAI_winner(ai); 
}

bool    frameworkInterface_isValid(int row, int col) {
    return isValid(row, col);
}

bool    frameworkInterface_isEnemy(ChessAI* ai, char piece) {
    ChessAI temp;
    ChessAI_init(&temp);
    ChessAI_sync(ai, &temp);
    temp.board[0] = piece;
    bool ret = ChessAI_isEnemy(&temp, 0, 0);
    ChessAI_destroy(&temp);
    
    return ret;
}

bool    frameworkInterface_isOwn(ChessAI* ai, char piece) {
    ChessAI temp;
    ChessAI_init(&temp);
    ChessAI_sync(ai, &temp);
    temp.board[0] = piece;
    bool ret = ChessAI_isOwn(&temp, 0, 0);
    ChessAI_destroy(&temp);
    
    return ret;
}

bool    frameworkInterface_isNothing(ChessAI* ai, char piece) {
    ChessAI temp;
    ChessAI_init(&temp);
    ChessAI_sync(ai, &temp);
    temp.board[0] = piece;
    bool ret = ChessAI_isNothing(&temp, 0, 0);
    ChessAI_destroy(&temp);
    
    return ret;
}

int     frameworkInterface_eval(ChessAI* ai) {
    return ChessAI_eval(ai);
}

int     frameworkInterface_moves(ChessAI* ai, char* out) {
    int moves[MAX_MOVES] = {0};
    int count = ChessAI_moves(ai, moves);
    for (int i=0; i<count; ++i) {
        out += MOVE_TO_STR(out, moves[i]);
    }
    
    return count;
}

int     frameworkInterface_movesShuffled(ChessAI* ai, char* out) {
    int moves[MAX_MOVES] = {0};
    int count = ChessAI_movesShuffled(ai, moves);
    for (int i=0; i<count; ++i) {
        out += MOVE_TO_STR(out, moves[i]);
    }
    
    return count;
}

int     frameworkInterface_movesEvaluated(ChessAI* ai, char* out) {
    int moves[MAX_MOVES] = {0};
    int count = ChessAI_movesEvaluated(ai, moves);
    for (int i=0; i<count; ++i) {
        out += MOVE_TO_STR(out, moves[i]);
    }
    
    return count;
}

void    frameworkInterface_move(ChessAI* ai, char* in) {
    ChessAI_move(ai, STR_TO_MOVE(in));
}

void    frameworkInterface_moveRandom(ChessAI* ai, char* out) {
    int move = ChessAI_moveRandom(ai);
    MOVE_TO_STR(out, move);
}

void    frameworkInterface_moveGreedy(ChessAI* ai, char* out) {
    int move = ChessAI_moveGreedy(ai);
    MOVE_TO_STR(out, move);
}

void    frameworkInterface_moveNegamax(ChessAI* ai, char* out, int depth, int duration) {
    int move = ChessAI_moveNegamax(ai, depth, duration);
    MOVE_TO_STR(out, move);
}

void    frameworkInterface_moveAlphabeta(ChessAI* ai, char* out, int depth, int duration) {
    int move = ChessAI_moveAlphabeta(ai, depth, duration);
    MOVE_TO_STR(out, move);
}

void    frameworkInterface_undo(ChessAI* ai) {
    ChessAI_undo(ai);
}
