#ifndef CHESSAI_H_LOCK
#define CHESSAI_H_LOCK

#include <stdbool.h>


/****************************  STRUCTS  ********************************/
typedef struct ChessAI {
	int turn;
	char playing;
	char* board;
	int white_score;
	int black_score;
} ChessAI;


/********************  CONSTRUCTORS/DESTRUCTOR  ************************/
void	ChessAI_init(ChessAI* self);
void	ChessAI_destroy(ChessAI* self);


/*****************************  METHODS  *******************************/
void	ChessAI_reset(ChessAI* self);
void	ChessAI_getBoard(ChessAI* self, char* out);
void	ChessAI_setBoard(ChessAI* self, char* in);
char	ChessAI_winner(ChessAI* self);
bool	ChessAI_isEnemy(ChessAI* self, char piece);
bool	ChessAI_isOwn(ChessAI* self, char piece);
int		ChessAI_eval(ChessAI* self);
void	ChessAI_evalBoard(ChessAI* self);
int		ChessAI_kingMoves(ChessAI* self, int* out);
int		ChessAI_queenMoves(ChessAI* self, int* out);
int		ChessAI_bishopMoves(ChessAI* self, int* out);
int		ChessAI_knightMoves(ChessAI* self, int* out);
int		ChessAI_rookMoves(ChessAI* self, int* out);
int		ChessAI_pawnMoves(ChessAI* self, int* out);
int		ChessAI_moves(ChessAI* self, int* out);
int		ChessAI_movesShuffled(ChessAI* self, int* out);
int		ChessAI_movesEvaluated(ChessAI* self, int* out);
void	ChessAI_move(ChessAI* self, int move);
void	ChessAI_undo(ChessAI* self);
int		ChessAI_moveRandom(ChessAI* self);
int		ChessAI_moveGreedy(ChessAI* self);
int		ChessAI_moveNegamax(ChessAI* self, int depth, int duration);
int		ChessAI_negamax(ChessAI* self, int depth, int duration);
int		ChessAI_moveAlphabeta(ChessAI* self, int depth, int duration);
int		ChessAI_alphabeta(ChessAI* self, int depth, int duration, int alpha, int beta);


/**************************  STATIC METHODS  ***************************/
bool	isValid(int row, int column);
bool	isNothing(char piece);


#endif
