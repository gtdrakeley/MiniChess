#ifndef CHESSAI_H_LOCK
#define CHESSAI_H_LOCK

#include <stdbool.h>

// #define NDEBUG



/****************************  MACROS  *********************************/
#define INDEX_TO_ROW(IDX) ((IDX) / 5)

#define INDEX_TO_COL(IDX) ((IDX) % 5)

#define RC_TO_INDEX(ROW, COL) ((ROW)*5 + (COL))

#define CHECK_BIT(VAR, POS) ((VAR) & (1 << (POS)))

#define SET_BIT(VAR, POS) ((VAR) |= (1 << (POS)))

#define CHECK_BITS(VAR, NUM) (((VAR) ^ (~((~0) << (NUM)))) == 0)


/****************************  STRUCTS  ********************************/
typedef struct ChessAI {
    int turn;
    char playing;
    char* board;
    int white_score;
    int black_score;
} ChessAI;


/********************  CONSTRUCTORS/DESTRUCTOR  ************************/
void    ChessAI_init(ChessAI* self);
void    ChessAI_destroy(ChessAI* self);


/*****************************  METHODS  *******************************/
void    ChessAI_sync(ChessAI* self, ChessAI* other);
void    ChessAI_reset(ChessAI* self);
void    ChessAI_getBoard(ChessAI* self, char* out);
void    ChessAI_setBoard(ChessAI* self, char* in);
char    ChessAI_winner(ChessAI* self);
bool    ChessAI_isEnemy(ChessAI* self, int row, int col);
bool    ChessAI_isOwn(ChessAI* self, int row, int col);
bool    ChessAI_isNothing(ChessAI* self, int row, int col);
int     ChessAI_eval(ChessAI* self);
void    ChessAI_evalBoard(ChessAI* self);
void    ChessAI_move(ChessAI* self, int move);
void    ChessAI_undo(ChessAI* self);
int     ChessAI_kingMoves(ChessAI* self, int* out, int start);
int     ChessAI_queenMoves(ChessAI* self, int* out, int start);
int     ChessAI_bishopMoves(ChessAI* self, int* out, int start);
int     ChessAI_knightMoves(ChessAI* self, int* out, int start);
int     ChessAI_rookMoves(ChessAI* self, int* out, int start);
int     ChessAI_pawnMoves(ChessAI* self, int* out, int start);
int     ChessAI_moves(ChessAI* self, int* out);
int     ChessAI_movesShuffled(ChessAI* self, int* out);
int     ChessAI_movesEvaluated(ChessAI* self, int* out);
int     ChessAI_moveRandom(ChessAI* self);
int     ChessAI_moveGreedy(ChessAI* self);
int     ChessAI_moveNegamax(ChessAI* self, int depth, int duration);
int     ChessAI_negamax(ChessAI* self, int depth, int duration);
int     ChessAI_moveAlphabeta(ChessAI* self, int depth, int duration);
int     ChessAI_alphabeta(ChessAI* self, int depth, int duration, int alpha, int beta);


/**************************  STATIC METHODS  ***************************/
bool    isValid(int row, int col);


#endif
