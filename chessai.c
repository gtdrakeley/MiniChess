#include "chessai.h"

#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "main.h"
#include "move.h"
#include "slavesort.h"
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
    2000, 2000, 2000, 2000, 2000,
    100, 100, 100, 100, 100,
    100, 100, 100, 100, 100,
    100, 100, 100, 100, 100,
    100, 100, 100, 100, 100,
    100, 100, 100, 100, 100
};

int EVAL_BOUND = 20000 + 2000*6 + 500 + 300 + 300 + 1;



/********************  CONSTRUCTORS/DESTRUCTOR  ************************/
void    ChessAI_init(ChessAI* self) {
    self->turn = 1;
    self->playing = 'W';
    self->board = (char*)malloc(31*sizeof(char));
    strcpy(self->board, "kqbnrppppp..........PPPPPRNBQK");
    self->white_score = 0;
    self->black_score = 0;
    self->hidx = 0;
    self->history = (History**)malloc(HIST_SIZE*sizeof(History*));
    for (int i=0; i<HIST_SIZE; ++i) { self->history[i] = NULL; }
    self->recur_calls = 0;
}


void    ChessAI_destroy(ChessAI* self) {
    if (self->board) {
        free(self->board);
    }
    if (self->history) {
        for (int i=0; i<HIST_SIZE; ++i) {
            if (self->history[i]) {
                free(self->history[i]);
            } else { break; }
        }
        free(self->history);
    }
}



/*****************************  METHODS  *******************************/
void    ChessAI_sync(ChessAI* self, ChessAI* other) {
    char board[42] = {'\0'};
    ChessAI_getBoard(self, board);
    ChessAI_setBoard(other, board);

}


void    ChessAI_clearHistory(ChessAI* self) {
    self->hidx = 0;
    for (int i=0; i<HIST_SIZE; ++i) {
        if (self->history[i]) {
            free(self->history[i]);
            self->history[i] = NULL;
        } else { break; }
    }
}


void    ChessAI_reset(ChessAI* self) {
    self->turn = 1;
    self->playing = 'W';
    strcpy(self->board, "kqbnrppppp..........PPPPPRNBQK");
    self->recur_calls = 0;
    ChessAI_evalBoard(self);
    ChessAI_clearHistory(self);
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
    ChessAI_clearHistory(self);
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
    int src = MOVE_SRC(move);
    int dest = MOVE_DEST(move);
    char src_piece = self->board[src];
    char dest_piece = self->board[dest];

    debug("Preparing to allocate new history");
    self->history[self->hidx] = (History*)malloc(sizeof(History));
    debug("New history allocated at %p", self->history[self->hidx]);
    History_init(self->history[(self->hidx)++], move, src_piece, dest_piece, self->white_score, self->black_score);
    debug("History initialized");

    if (src_piece <= 'R') {
        switch (src_piece) {
            case 'K':
                self->white_score -= KING_POS_VALUES[src] - KING_POS_VALUES[dest];
                break;
            case 'Q':
                self->white_score -= QUEEN_POS_VALUES[src] - QUEEN_POS_VALUES[dest];
                break;
            case 'B':
                self->white_score -= BISHOP_POS_VALUES[src] - BISHOP_POS_VALUES[dest];
                break;
            case 'N':
                self->white_score -= KNIGHT_POS_VALUES[src] - KNIGHT_POS_VALUES[dest];
                break;
            case 'R':
                self->white_score -= ROOK_POS_VALUES[src] - ROOK_POS_VALUES[dest];
                break;
            case 'P':
                self->white_score -= PAWN_POS_VALUES[src] - PAWN_POS_VALUES[dest];
                break;
        }
        switch (dest_piece) {
            case 'k':
                self->black_score -= KING_POS_VALUES[29-dest];
                break;
            case 'q':
                self->black_score -= QUEEN_POS_VALUES[29-dest];
                break;
            case 'b':
                self->black_score -= BISHOP_POS_VALUES[29-dest];
                break;
            case 'n':
                self->black_score -= KNIGHT_POS_VALUES[29-dest];
                break;
            case 'r':
                self->black_score -= ROOK_POS_VALUES[29-dest];
                break;
            case 'p':
                self->black_score -= PAWN_POS_VALUES[29-dest];
                break;
        }
    } else {
        switch (src_piece) {
            case 'k':
                self->black_score -= KING_POS_VALUES[29-src] - KING_POS_VALUES[29-dest];
                break;
            case 'q':
                self->black_score -= QUEEN_POS_VALUES[29-src] - QUEEN_POS_VALUES[29-dest];
                break;
            case 'b':
                self->black_score -= BISHOP_POS_VALUES[29-src] - BISHOP_POS_VALUES[29-dest];
                break;
            case 'n':
                self->black_score -= KNIGHT_POS_VALUES[29-src] - KNIGHT_POS_VALUES[29-dest];
                break;
            case 'r':
                self->black_score -= ROOK_POS_VALUES[29-src] - ROOK_POS_VALUES[29-dest];
                break;
            case 'p':
                self->black_score -= PAWN_POS_VALUES[29-src] - PAWN_POS_VALUES[29-dest];
                break;
        }
        switch (dest_piece) {
            case 'K':
                self->white_score -= KING_POS_VALUES[dest];
                break;
            case 'Q':
                self->white_score -= QUEEN_POS_VALUES[dest];
                break;
            case 'B':
                self->white_score -= BISHOP_POS_VALUES[dest];
                break;
            case 'N':
                self->white_score -= KNIGHT_POS_VALUES[dest];
                break;
            case 'R':
                self->white_score -= ROOK_POS_VALUES[dest];
                break;
            case 'P':
                self->white_score -= PAWN_POS_VALUES[dest];
                break;
        }
    }
    
    if (self->playing == 'W') {
        self->playing = 'B';
    } else {
        self->playing = 'W';
        (self->turn)++;
    }
    self->board[src] = '.';
    if (src_piece == 'P' && dest <= 4) {
        self->board[dest] = 'Q';
    } else if (src_piece == 'p' && dest >= 25) {
        self->board[dest] = 'q';
    } else {
        self->board[dest] = src_piece;
    }
}


void    ChessAI_undo(ChessAI* self) {
    History* hist = self->history[--(self->hidx)];
    self->history[self->hidx] = NULL;

    if (self->playing == 'W') {
        self->playing = 'B';
        (self->turn)--;
    } else {
        self->playing = 'W';
    }
    self->board[MOVE_SRC(hist->move)] = hist->src_piece;
    self->board[MOVE_DEST(hist->move)] = hist->dest_piece;
    self->white_score = hist->white_score;
    self->black_score = hist->black_score;

    free(hist);
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

    return (l_out - out);
}


int     ChessAI_movesShuffled(ChessAI* self, int* out) {
    int count = ChessAI_moves(self, out);
    int r;
    int t;

    for (int i=0; i<count-1; ++i) {
        r = i + rand() / (RAND_MAX / (count - i) + 1);
        t = out[r];
        out[r] = out[i];
        out[i] = t;
    }

    /*
    for (int i=count-1; i>0; --i) {
        r = RAND_INT(0, i);
        if (r == i) { continue; }
        out[i] ^= out[r];
        out[r] ^= out[i];
        out[i] ^= out[r];

    }
    */

    return count;
}


int     ChessAI_movesEvaluated(ChessAI* self, int* out) {
    int count = ChessAI_movesShuffled(self, out);
    int* evals = (int*)malloc(count*sizeof(int));

    for (int i=0; i<count; ++i) {
        ChessAI_move(self, out[i]);
        evals[i] = ChessAI_eval(self);
        ChessAI_undo(self);
    }

    slavesort(evals, out, count);
    
    free(evals);

    return count;
}


int     ChessAI_moveRandom(ChessAI* self) {
    int moves[MAX_MOVES];
    
    ChessAI_movesShuffled(self, moves);
    ChessAI_move(self, moves[0]);
    
    return moves[0];
}


int     ChessAI_moveGreedy(ChessAI* self) {
    int moves[MAX_MOVES];
    
    ChessAI_movesEvaluated(self, moves);
    ChessAI_move(self, moves[0]);

    return moves[0];
}


int     ChessAI_moveNegamax(ChessAI* self, int depth, int duration) {
    int moves[MAX_MOVES];
    int count = ChessAI_movesShuffled(self, moves);
    int best = 0;
    int score = -EVAL_BOUND;
    int temp;

    for (int i=0; i<count; ++i) {
        ChessAI_move(self, moves[i]);
        temp = -ChessAI_negamax(self, depth-1, duration);
        ChessAI_undo(self);
        if (temp > score) {
            best = moves[i];
            score = temp;
        }
    }

    ChessAI_move(self, best);

    return best;
}


int     ChessAI_negamax(ChessAI* self, int depth, int duration) {
    if (depth == 0 || ChessAI_winner(self) != '?') { return ChessAI_eval(self); }

    int moves[MAX_MOVES];
    int count = ChessAI_movesShuffled(self, moves);
    int score = -EVAL_BOUND;
    
    for (int i=0; i<count; ++i) {
        ChessAI_move(self, moves[i]);
        score = max(score, -ChessAI_negamax(self, depth-1, duration));
        ChessAI_undo(self);
    }

    return score;
}


int     ChessAI_moveAlphabeta(ChessAI* self, int depth, int duration) {
    if (depth < 0) {
        return ChessAI_trnMoveAlphabeta(self, duration);
    } else {
        return ChessAI_stdMoveAlphabeta(self, depth);
    }
}


int     ChessAI_stdMoveAlphabeta(ChessAI* self, int depth) {
    int moves[MAX_MOVES];
    int count = ChessAI_movesEvaluated(self, moves);
    int best = 0;
    int alpha = -EVAL_BOUND;
    int beta = EVAL_BOUND;
    int temp;

    for (int i=0; i<count; ++i) {
        ChessAI_move(self, moves[i]);
        temp = -ChessAI_stdAlphabeta(self, depth-1, -beta, -alpha);
        ChessAI_undo(self);
        if (temp > alpha) {
            best = moves[i];
            alpha = temp;
        }
    }

    ChessAI_move(self, best);

    return best;
}


int     ChessAI_trnMoveAlphabeta(ChessAI* self, int duration) {
    debug("Creating locals variables...");
    int moves[MAX_MOVES];
    int count = ChessAI_movesEvaluated(self, moves);
    int best = 0;
    int t_best = 0;
    int alpha = -EVAL_BOUND;
    int beta = EVAL_BOUND;
    int temp;
    int iter_depth = 1;
    int max_depth = 80-(self->turn*2-((self->playing == 'W') ? 2 : 1));
    bool elapsed = false;
    int m_duration = (duration - 1500) / (41 - self->turn);
    // self->recur_calls = 0;
    unsigned long long start = msec();

    debug("Entering while loop...");
    while (true) {
        for (int i=0; i<count; ++i) {
            debug("Checking move...");
            ChessAI_move(self, moves[i]);
            if ((elapsed = ChessAI_trnAlphabeta(self, &temp, start, iter_depth-1, m_duration, -beta, -alpha))) { break; }
            temp *= (-1);
            ChessAI_undo(self);
            debug("Comparing eval...");
            if (temp > alpha) {
                debug("Found new best move during search...");
                t_best = moves[i];
                alpha = temp;
            }
        }
        if (elapsed) { break; }
        debug("Setting new best move...");
        best = t_best;
        alpha = -EVAL_BOUND;
        beta = EVAL_BOUND;
        if (++iter_depth > max_depth) {
            temp = iter_depth;
            break;
        }
    }

    debug("Undoing %d moves from history of size %d due to incomplete search ...", iter_depth-temp, self->hidx);
    for (int i=0; i<(iter_depth-temp); ++i) {
        ChessAI_undo(self);
    }
    ChessAI_move(self, best);
    debug("Clearing history...");
    ChessAI_clearHistory(self);

    OUTPUT(
        char boardstr[42];
        char movestr[7];
        ChessAI_getBoard(self, boardstr);
        MOVE_TO_STR(movestr, best); movestr[5] = '\0';
        printf("------  Tournament Move Statistics  ------\n");
        printf("    %-12sMove:             %s (%d -> %d)\n", strtok(boardstr, "\n"), movestr, MOVE_SRC(best), MOVE_DEST(best));
        printf("    %-12sDepth Reached:    %d\n", strtok(NULL, "\n"), iter_depth-1);
        // printf("    %-12sRecursive Calls:  %ld\n", strtok(NULL, "\n"), self->recur_calls);
        printf("    %-12sRecursive Calls:  NOT IMPLEMENTED\n", strtok(NULL, "\n"));
        printf("    %-12sTime Allotted:    %d ms\n", strtok(NULL, "\n"), m_duration);
        unsigned long long actual = msec()-start;
        printf("    %-12sTime Actual:      ~%lld ms\n", strtok(NULL, "\n"), actual);
        printf("    %-12sTime Remaining:   ~%lld ms\n", strtok(NULL, "\n"), duration-actual);
        printf("    %s\n", strtok(NULL, "\n"));
        printf("\n\n");
    );

    return best;
}


int     ChessAI_stdAlphabeta(ChessAI* self, int depth, int alpha, int beta) {
    if (depth == 0 || ChessAI_winner(self) != '?') { return ChessAI_eval(self); }

    int moves[MAX_MOVES];
    int count = ChessAI_movesEvaluated(self, moves);
    int score = -EVAL_BOUND;

    for (int i=0; i<count; ++i) {
        ChessAI_move(self, moves[i]);
        score = max(score, -ChessAI_stdAlphabeta(self, depth-1, -beta, -alpha));
        ChessAI_undo(self);
        alpha = max(alpha, score);
        if (alpha >= beta) { break; }
    }

    return score;
}


bool    ChessAI_trnAlphabeta(ChessAI* self, int* ret_score, unsigned long long start, int depth, int duration, int alpha, int beta) {
    static unsigned long recur_calls = 0;

    if (++recur_calls >= RECUR_CALLS_BOUND) {
        if ((msec()-start) >= duration) {
            // self->recur_calls += recur_calls;
            recur_calls = 0;
            *ret_score = depth; 
            return true;
        } else {
            // self->recur_calls += recur_calls;
            recur_calls = 0;
        }
    }

    if (depth == 0 || ChessAI_winner(self) != '?') {
        *ret_score = ChessAI_eval(self);
        return false;
    }

    int moves[MAX_MOVES];
    int count = ChessAI_movesEvaluated(self, moves);
    int score = -EVAL_BOUND;
    int temp = 0;

    for (int i=0; i<count; ++i) {
        ChessAI_move(self, moves[i]);
        if (ChessAI_trnAlphabeta(self, &temp, start, depth-1, duration, -beta, -alpha)) {
            *ret_score = temp;
            return true;
        }
        score = max(score, -temp);
        ChessAI_undo(self);
        alpha = max(alpha, score);
        if (alpha >= beta) { break; }
    }

    *ret_score = score;

    return false;
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



/************************  UTILITY FUNCTIONS  **************************/
int     max(int a, int b) {
    return (a > b) ? (a) : (b);
}


unsigned long long     msec() {
    struct timeval tval;

    gettimeofday(&tval, NULL);

    return (tval.tv_sec * 1000) + (tval.tv_usec / 1000);
}
