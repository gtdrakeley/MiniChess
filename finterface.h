#ifndef FRAMEWORK_INTERFACE_H_LOCK
#define FRAMEOWKR_INTERFACE_H_LOCK

#include <stdbool.h>

#include "chessai.h"


void    frameworkInterface_reset(ChessAI* ai);
void    frameworkInterface_getBoard(ChessAI* ai, char* out);
void    frameworkInterface_setBoard(ChessAI* ai, char* in);
char    frameworkInterface_winner(ChessAI* ai);
bool    frameworkInterface_isValid(int row, int col);
bool    frameworkInterface_isEnemy(ChessAI* ai, char piece);
bool    frameworkInterface_isOwn(ChessAI* ai, char piece);
bool    frameworkInterface_isNothing(ChessAI* ai, char piece);
int     frameworkInterface_eval(ChessAI* ai);
int     frameworkInterface_moves(ChessAI* ai, char* out);
int     frameworkInterface_movesShuffled(ChessAI* ai, char* out);
int     frameworkInterface_movesEvaluated(ChessAI* ai, char* out);
void    frameworkInterface_move(ChessAI* ai, char* in);
void    frameworkInterface_moveRandom(ChessAI* ai, char* out);
void    frameworkInterface_moveGreedy(ChessAI* ai, char* out);
void    frameworkInterface_moveNegamax(ChessAI* ai, char* out, int depth, int duration);
void    frameworkInterface_moveAlphabeta(ChessAI* ai, char* out, int depth, int duration);
void    frameworkInterface_undo(ChessAI* ai);

#endif
