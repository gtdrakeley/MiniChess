#include "chessai.h"

#include <stdlib.h>
#include <string.h>

#include "main.h"
#include "move.h"
#include "debug.h"


/****************************  CONSTANTS  *****************************/
char    WHITE_PIECES[] = "KQBNRP";
char    BLACK_PIECES[] = "kqbnrp";
int     KING_POS_VALUES[] = {
    20000, 20000, 20000, 20000, 20000,
    20000, 20000, 20000, 20000, 20000,
    20000, 20000, 20000, 20000, 20000,
    20000, 20000, 20000, 20000, 20000,
    20000, 20000, 20000, 20000, 20000,
    20000, 20000, 20000, 20000, 20000
};
int     QUEEN_POS_VALUES[] = {
    2000, 2000, 2000, 2000, 2000,
    2000, 2000, 2000, 2000, 2000,
    2000, 2000, 2000, 2000, 2000,
    2000, 2000, 2000, 2000, 2000,
    2000, 2000, 2000, 2000, 2000,
    2000, 2000, 2000, 2000, 2000
};
int     BISHOP_POS_VALUES[] = {
    300, 300, 300, 300, 300,
    300, 300, 300, 300, 300,
    300, 300, 300, 300, 300,
    300, 300, 300, 300, 300,
    300, 300, 300, 300, 300,
    300, 300, 300, 300, 300
};
int     KNIGHT_POS_VALUES[] = {
    300, 300, 300, 300, 300,
    300, 300, 300, 300, 300,
    300, 300, 300, 300, 300,
    300, 300, 300, 300, 300,
    300, 300, 300, 300, 300,
    300, 300, 300, 300, 300
};
int     ROOK_POS_VALUES[] = {
    500, 500, 500, 500, 500,
    500, 500, 500, 500, 500,
    500, 500, 500, 500, 500,
    500, 500, 500, 500, 500,
    500, 500, 500, 500, 500,
    500, 500, 500, 500, 500
};
int     PAWN_POS_VALUES[] = {
    100, 100, 100, 100, 100,
    100, 100, 100, 100, 100,
    100, 100, 100, 100, 100,
    100, 100, 100, 100, 100,
    100, 100, 100, 100, 100,
    100, 100, 100, 100, 100
};


/********************  CONSTRUCTORS/DESTRUCTOR  ************************/
void    ChessAI_init(ChessAI* self) {
    self->turn = 1;
    self->playing = 'W';
    self->board = (char*)malloc(31*sizeof(char));
    strcpy(self->board, "kwbnrppppp..........PPPPPRNBQK");
    self->white_score = 0;
    self->black_score = 0;
}

void    ChessAI_destroy(ChessAI* self) {
    if (self->board) {
        free(self->board);
    }
}


/*****************************  METHODS  *******************************/
void    ChessAI_reset(ChessAI* self) {
    self->turn = 1;
    self->playing = 'W';
    strcpy(self->board, "kqbnrppppp..........PPPPPRNBQK");
    ChessAI_evalBoard(self);
}

void    ChessAI_getBoard(ChessAI* self, char* out) {
    out += sprintf(out, "%d %c\n", self->turn, self->playing);
    for (int i=0; i<6; ++i) {
        strncpy(out, self->board+(i*5), 5);
        out[5] = '\n';
        out += 6;
    }
}

void    ChessAI_setBoard(ChessAI* self, char* in) {
    char* turn_state = strtok(in, "\n");
    char* l_board = self->board;
    for (int i=0; i<6; ++i) {
        l_board = strncpy(l_board, strtok(NULL, "\n"), 5) + 5;
    }
    self->turn = atoi(strtok(turn_state, " "));
    self->playing = strtok(NULL, " ")[0];
    ChessAI_evalBoard(self);
}

char    ChessAI_winner(ChessAI* self) {
    if (strchr(self->board, 'K') && !strchr(self->board, 'k')) {
        return 'W';
    } else if (strchr(self->board, 'k') && !strchr(self->board, 'K')) {
        return 'B';
    } else if (self->turn > 40) {
        return '=';
    } else {
        return '?';
    }
}

bool    ChessAI_isEnemy(ChessAI* self, char piece) {
    if (self->playing == 'W' && strchr(BLACK_PIECES, piece)) {
        return true;
    } else if (self->playing == 'B' && strchr(WHITE_PIECES, piece)) {
        return true;
    } else {
        return false;
    }
}

bool    ChessAI_isOwn(ChessAI* self, char piece) {
    if (self->playing == 'W' && strchr(WHITE_PIECES, piece)) {
        return true;
    } else if (self->playing == 'B' && strchr(BLACK_PIECES, piece)) {
        return true;
    } else {
        return false;
    }
}
int     ChessAI_eval(ChessAI* self) {
    return (self->playing == 'W') ? 
        (self->white_score - self->black_score) : 
        (self->black_score - self->white_score);
}
void    ChessAI_evalBoard(ChessAI* self) {
    self->white_score = 0;
    self->black_score = 0;
    for (int i=0; i<30; ++i) {
        switch (self->board[i]) {
            case 'K':
                self->white_score += KING_POS_VALUES[i];
                break;
            case 'Q':
                self->white_score += QUEEN_POS_VALUES[i];
                break;
            case 'B':
                self->white_score += BISHOP_POS_VALUES[i];
                break;
            case 'N':
                self->white_score += KNIGHT_POS_VALUES[i];
                break;
            case 'R':
                self->white_score += ROOK_POS_VALUES[i];
                break;
            case 'P':
                self->white_score += PAWN_POS_VALUES[i];
                break;
            case 'k':
                self->black_score += KING_POS_VALUES[29-i];
                break;
            case 'q':
                self->black_score += QUEEN_POS_VALUES[29-i];
                break;
            case 'b':
                self->black_score += BISHOP_POS_VALUES[29-i];
                break;
            case 'n':
                self->black_score += KNIGHT_POS_VALUES[29-i];
                break;
            case 'r':
                self->black_score += ROOK_POS_VALUES[29-i];
                break;
            case 'p':
                self->black_score += PAWN_POS_VALUES[29-i];
                break;
        }
    }
}

int     ChessAI_kingMoves(ChessAI* self, int* out, int start) {
    return 0;
}

int     ChessAI_queenMoves(ChessAI* self, int* out, int start) {
    return 0;
}

int     ChessAI_bishopMoves(ChessAI* self, int* out, int start) {
    return 0;
}

int     ChessAI_knightMoves(ChessAI* self, int* out, int start) {
    return 0;
}

int     ChessAI_rookMoves(ChessAI* self, int* out, int start) {
    return 0;
}

int     ChessAI_pawnMoves(ChessAI* self, int* out, int start) {
    return 0;
}

int     ChessAI_moves(ChessAI* self, int* out) {
    return 0;
}

int     ChessAI_movesShuffled(ChessAI* self, int* out) {
    return 0;
}

int     ChessAI_movesEvaluated(ChessAI* self, int* out) {
    return 0;
}

void    ChessAI_move(ChessAI* self, int move) {
}

void    ChessAI_undo(ChessAI* self) {
}

int     ChessAI_moveRandom(ChessAI* self) {
    return 0;
}

int     ChessAI_moveGreedy(ChessAI* self) {
    return 0;
}

int     ChessAI_moveNegamax(ChessAI* self, int depth, int duration) {
    return 0;
}

int     ChessAI_negamax(ChessAI* self, int depth, int duration) {
    return 0;
}

int     ChessAI_moveAlphabeta(ChessAI* self, int depth, int duration) {
    return 0;
}

int     ChessAI_alphabeta(ChessAI* self, int depth, int duration, int alpha, int beta) {
    return 0;
}


/**************************  STATIC METHODS  ***************************/
bool    isValid(int target) {
    if (target < 0) {
        return false;
    } else if (target > 29) {
        return false;
    } else {
        return true;
    }
}

bool    isNothing(char piece) {
    if (piece == '.') {
        return true;
    } else {
        return false;
    }
}
