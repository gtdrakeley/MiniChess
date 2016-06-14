#include "chessai.h"

#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "main.h"
#include "move.h"
#include "debug.h"



/****************************  CONSTANTS  *****************************/
// char    WHITE_PIECES[] = "KQBNRP";

// char    BLACK_PIECES[] = "kqbnrp";

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
void    ChessAI_sync(ChessAI* self, ChessAI* other) {
    char board[42] = {'\0'};
    ChessAI_getBoard(self, board);
    ChessAI_setBoard(other, board);

}


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
        *(out+5) = '\n';
        out += 6;
    }
    *(out) = '\0';
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


bool    ChessAI_isEnemy(ChessAI* self, int row, int col) {
    char piece = self->board[RC_TO_INDEX(row, col)];

    if (piece == '.') {
        return false;
    } else if (self->playing == 'W' && piece >= 'b') {
        return true;
    } else if (self->playing == 'B' && piece <= 'R') {
        return true;
    } else {
        return false;
    }
}


bool    ChessAI_isOwn(ChessAI* self, int row, int col) {
    char piece = self->board[RC_TO_INDEX(row, col)];

    if (piece == '.') {
        return false;
    } else if (self->playing == 'W' && piece <= 'R') {
        return true;
    } else if (self->playing == 'B' && piece >= 'b') {
        return true;
    } else {
        return false;
    }
}


bool    ChessAI_isNothing(ChessAI* self, int row, int col) {
    if (self->board[RC_TO_INDEX(row, col)] == '.') {
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


void    ChessAI_move(ChessAI* self, int move) {
}


void    ChessAI_undo(ChessAI* self) {
}


int     ChessAI_kingMoves(ChessAI* self, int* out, int start) {
    int* l_out = out;
    int row = INDEX_TO_ROW(start);
    int col = INDEX_TO_COL(start);

    if (isValid(row-1, col) && !ChessAI_isOwn(self, row-1, col)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-1, col));
        debug("King Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row+1, col) && !ChessAI_isOwn(self, row+1, col)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+1, col));
        debug("King Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row, col-1) && !ChessAI_isOwn(self, row, col-1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row, col-1));
        debug("King Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row, col+1) && !ChessAI_isOwn(self, row, col+1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row, col+1));
        debug("King Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row-1, col-1) && !ChessAI_isOwn(self, row-1, col-1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-1, col-1));
        debug("King Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row-1, col+1) && !ChessAI_isOwn(self, row-1, col+1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-1, col+1));
        debug("King Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row+1, col-1) && !ChessAI_isOwn(self, row+1, col-1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+1, col-1));
        debug("King Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row+1, col+1) && !ChessAI_isOwn(self, row+1, col+1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+1, col+1));
        debug("King Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }

    return (l_out - out);
}


int     ChessAI_queenMoves(ChessAI* self, int* out, int start) {
    int* l_out = out;
    int row = INDEX_TO_ROW(start);
    int col = INDEX_TO_COL(start);
    char blocked = 0x0;

    for (int offset=1; offset<6; ++offset) {
        if (!CHECK_BIT(blocked, 0) && isValid(row-offset, col) && !ChessAI_isOwn(self, row-offset, col)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-offset, col));
            debug("Queen Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row-offset, col)) { SET_BIT(blocked, 0); }
        } else { SET_BIT(blocked, 0); }
        if (!CHECK_BIT(blocked, 1) && isValid(row+offset, col) && !ChessAI_isOwn(self, row+offset, col)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+offset, col));
            debug("Queen Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row+offset,  col)) { SET_BIT(blocked, 1); }
        } else { SET_BIT(blocked, 1); }
        if (!CHECK_BIT(blocked, 2) && isValid(row, col-offset) && !ChessAI_isOwn(self, row, col-offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row, col-offset));
            debug("Queen Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row, col-offset)) { SET_BIT(blocked, 2); }
        } else { SET_BIT(blocked, 2); }
        if (!CHECK_BIT(blocked, 3) && isValid(row, col+offset) && !ChessAI_isOwn(self, row, col+offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row, col+offset));
            debug("Queen Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row, col+offset)) { SET_BIT(blocked, 3); }
        } else { SET_BIT(blocked, 3); }
        if (!CHECK_BIT(blocked, 4) && isValid(row-offset, col-offset) && !ChessAI_isOwn(self, row-offset, col-offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-offset, col-offset));
            debug("Queen Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row-offset, col-offset)) { SET_BIT(blocked, 4); }
        } else { SET_BIT(blocked, 4); }
        if (!CHECK_BIT(blocked, 5) && isValid(row-offset, col+offset) && !ChessAI_isOwn(self, row-offset, col+offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-offset, col+offset));
            debug("Queen Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row-offset, col+offset)) { SET_BIT(blocked, 5); }
        } else { SET_BIT(blocked, 5); }
        if (!CHECK_BIT(blocked, 6) && isValid(row+offset, col-offset) && !ChessAI_isOwn(self, row+offset, col-offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+offset, col-offset));
            debug("Queen Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row+offset, col-offset)) { SET_BIT(blocked, 6); }
        } else { SET_BIT(blocked, 6); }
        if (!CHECK_BIT(blocked, 7) && isValid(row+offset, col+offset) && !ChessAI_isOwn(self, row+offset, col+offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+offset, col+offset));
            debug("Queen Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row+offset, col+offset)) { SET_BIT(blocked, 7); }
        } else { SET_BIT(blocked, 7); }
        if (CHECK_BITS(blocked, 8)) { break; }
    }

    return (l_out - out);
}


int     ChessAI_bishopMoves(ChessAI* self, int* out, int start) {
    int* l_out = out;
    int row = INDEX_TO_ROW(start);
    int col = INDEX_TO_COL(start);
    char blocked = 0x0;

    for (int offset=1; offset<6; ++offset) {
        if (!CHECK_BIT(blocked, 0) && isValid(row-offset, col-offset) && !ChessAI_isOwn(self, row-offset, col-offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-offset, col-offset));
            debug("Bishop Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row-offset, col-offset)) { SET_BIT(blocked, 0); }
        } else { SET_BIT(blocked, 0); }
        if (!CHECK_BIT(blocked, 1) && isValid(row-offset, col+offset) && !ChessAI_isOwn(self, row-offset, col+offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-offset, col+offset));
            debug("Bishop Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row-offset, col+offset)) { SET_BIT(blocked, 1); }
        } else { SET_BIT(blocked, 1); }
        if (!CHECK_BIT(blocked, 2) && isValid(row+offset, col-offset) && !ChessAI_isOwn(self, row+offset, col-offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+offset, col-offset));
            debug("Bishop Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row+offset, col-offset)) { SET_BIT(blocked, 2); }
        } else { SET_BIT(blocked, 2); }
        if (!CHECK_BIT(blocked, 3) && isValid(row+offset, col+offset) && !ChessAI_isOwn(self, row+offset, col+offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+offset, col+offset));
            debug("Bishop Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row+offset, col+offset)) { SET_BIT(blocked, 3); }
        } else { SET_BIT(blocked, 3); }
        if (CHECK_BITS(blocked, 4)) { break; }
    }
    if (isValid(row-1, col) && ChessAI_isNothing(self, row-1, col)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-1, col));
        debug("Bishop Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row+1, col) && ChessAI_isNothing(self, row+1, col)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+1, col));
        debug("Bishop Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row, col-1) && ChessAI_isNothing(self, row, col-1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row, col-1));
        debug("Bishop Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row, col+1) && ChessAI_isNothing(self, row, col+1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row, col+1));
        debug("Bishop Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }

    return (l_out - out);
}


int     ChessAI_knightMoves(ChessAI* self, int* out, int start) {
    int* l_out = out;
    int row = INDEX_TO_ROW(start);
    int col = INDEX_TO_COL(start);

    if (isValid(row-2, col-1) && !ChessAI_isOwn(self, row-2, col-1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-2, col-1));
        debug("Knight Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row-2, col+1) && !ChessAI_isOwn(self, row-2, col+1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-2, col+1));
        debug("Knight Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row+2, col-1) && !ChessAI_isOwn(self, row+2, col-1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+2, col-1));
        debug("Knight Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row+2, col+1) && !ChessAI_isOwn(self, row+2, col+1)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+2, col+1));
        debug("Knight Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row-1, col-2) && !ChessAI_isOwn(self, row-1, col-2)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-1, col-2));
        debug("Knight Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row+1, col-2) && !ChessAI_isOwn(self, row+1, col-2)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+1, col-2));
        debug("Knight Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row-1, col+2) && !ChessAI_isOwn(self, row-1, col+2)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-1, col+2));
        debug("Knight Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }
    if (isValid(row+1, col+2) && !ChessAI_isOwn(self, row+1, col+2)) {
        *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+1, col+2));
        debug("Knight Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
    }

    return (l_out - out);
}


int     ChessAI_rookMoves(ChessAI* self, int* out, int start) {
    int* l_out = out;
    int row = INDEX_TO_ROW(start);
    int col = INDEX_TO_COL(start);
    char blocked = 0x0;

    for (int offset=1; offset<6; ++offset) {
        if (!CHECK_BIT(blocked, 0) && isValid(row-offset, col) && !ChessAI_isOwn(self, row-offset, col)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-offset, col));
            debug("Rook Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row-offset, col)) { SET_BIT(blocked, 0); }
        } else { SET_BIT(blocked, 0); }
        if (!CHECK_BIT(blocked, 1) && isValid(row+offset, col) && !ChessAI_isOwn(self, row+offset, col)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+offset, col));
            debug("Rook Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row+offset,  col)) { SET_BIT(blocked, 1); }
        } else { SET_BIT(blocked, 1); }
        if (!CHECK_BIT(blocked, 2) && isValid(row, col-offset) && !ChessAI_isOwn(self, row, col-offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row, col-offset));
            debug("Rook Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row, col-offset)) { SET_BIT(blocked, 2); }
        } else { SET_BIT(blocked, 2); }
        if (!CHECK_BIT(blocked, 3) && isValid(row, col+offset) && !ChessAI_isOwn(self, row, col+offset)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row, col+offset));
            debug("Rook Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
            if (ChessAI_isEnemy(self, row, col+offset)) { SET_BIT(blocked, 3); }
        } else { SET_BIT(blocked, 3); }
        if (CHECK_BITS(blocked, 4)) { break; }
    }

    return (l_out - out);
}


int     ChessAI_pawnMoves(ChessAI* self, int* out, int start) {
    int* l_out = out;
    int row = INDEX_TO_ROW(start);
    int col = INDEX_TO_COL(start);

    if (self->playing == 'W') {
        if (isValid(row-1, col) && ChessAI_isNothing(self, row-1, col)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-1, col));
            debug("Pawn Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
        }
        if (isValid(row-1, col-1) && ChessAI_isEnemy(self, row-1, col-1)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-1, col-1));
            debug("Pawn Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
        }
        if (isValid(row-1, col+1) && ChessAI_isEnemy(self, row-1, col+1)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row-1, col+1));
            debug("Pawn Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
        }
    } else {
        if (isValid(row+1, col) && ChessAI_isNothing(self, row+1, col)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+1, col));
            debug("Pawn Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
        }
        if (isValid(row+1, col-1) && ChessAI_isEnemy(self, row+1, col-1)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+1, col-1));
            debug("Pawn Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
        }
        if (isValid(row+1, col+1) && ChessAI_isEnemy(self, row+1, col+1)) {
            *(l_out++) = MOVE_GEN(start, RC_TO_INDEX(row+1, col+1));
            debug("Pawn Move: %d -> %d", MOVE_SRC(*(l_out-1)), MOVE_DEST(*(l_out-1)));
        }
    }

    return (l_out - out);
}


int     ChessAI_moves(ChessAI* self, int* out) {
    int* l_out = out;

    if (self->playing == 'W') {
        for (int start=0; start<30; ++start) {
            switch(self->board[start]) {
                case 'K':
                    l_out += ChessAI_kingMoves(self, l_out, start);
                    break;
                case 'Q':
                    l_out += ChessAI_queenMoves(self, l_out, start);
                    break;
                case 'B':
                    l_out += ChessAI_bishopMoves(self, l_out, start);
                    break;
                case 'N':
                    l_out += ChessAI_knightMoves(self, l_out, start);
                    break;
                case 'R':
                    l_out += ChessAI_rookMoves(self, l_out, start);
                    break;
                case 'P':
                    l_out += ChessAI_pawnMoves(self, l_out, start);
                    break;
            }
        }
    } else {
        for (int start=0; start<30; ++start) {
            switch(self->board[start]) {
                case 'k':
                    l_out += ChessAI_kingMoves(self, l_out, start);
                    break;
                case 'q':
                    l_out += ChessAI_queenMoves(self, l_out, start);
                    break;
                case 'b':
                    l_out += ChessAI_bishopMoves(self, l_out, start);
                    break;
                case 'n':
                    l_out += ChessAI_knightMoves(self, l_out, start);
                    break;
                case 'r':
                    l_out += ChessAI_rookMoves(self, l_out, start);
                    break;
                case 'p':
                    l_out += ChessAI_pawnMoves(self, l_out, start);
                    break;
            }
        }
    }

    /*
    for (int i=0; i<200; ++i) {
        printf("Move: %d\n", out[i]);
        sleep(1);
    }
    */

    return (l_out - out);
}


int     ChessAI_movesShuffled(ChessAI* self, int* out) {
    return 0;
}


int     ChessAI_movesEvaluated(ChessAI* self, int* out) {
    return 0;
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
bool    isValid(int row, int col) {
    if (row < 0) {
        return false;
    } else if (row > 5) {
        return false;
    } else if (col < 0) {
        return false;
    } else if (col > 4) {
        return false;
    } else {
        return true;
    }
}
