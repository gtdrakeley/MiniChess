#include "finterface.h"

#include <stdlib.h>
#include <stdio.h>

#include "main.h"
#include "chessai.h"
#include "move.h"
#include "debug.h"


void	frameworkInterface_reset(ChessAI* ai) {
	ChessAI_reset(ai);
}

void	frameworkInterface_getBoard(ChessAI* ai, char* out) {
	ChessAI_getBoard(ai, out);
}

void	frameworkInterface_setBoard(ChessAI* ai, char* in) {
	ChessAI_setBoard(ai, in);
}

char	frameworkInterface_winner(ChessAI* ai) {
	return ChessAI_winner(ai); 
}

bool	frameworkInterface_isValid(int row, int column) {
	return isValid(row, column);
}

bool	frameworkInterface_isEnemy(ChessAI* ai, char piece) {
	return ChessAI_isEnemy(ai, piece);
}

bool	frameworkInterface_isOwn(ChessAI* ai, char piece) {
	return ChessAI_isOwn(ai, piece);
}

bool	frameworkInterface_isNothing(char piece) {
	return isNothing(piece);
}

int		frameworkInterface_eval(ChessAI* ai) {
	return ChessAI_eval(ai);
}

int		frameworkInterface_moves(ChessAI* ai, char* out) {
	int moves[200] = {0};
	int count = ChessAI_moves(ai, moves);
	for (int i=0; i<count; ++i) {
		out += MOVE_TO_STR(out, moves[i]);
	}
	return count;
}

int		frameworkInterface_movesShuffled(ChessAI* ai, char* out) {
	int moves[200] = {0};
	int count = ChessAI_movesShuffled(ai, moves);
	for (int i=0; i<count; ++i) {
		out += MOVE_TO_STR(out, moves[i]);
	}
	return count;
}

int		frameworkInterface_movesEvaluated(ChessAI* ai, char* out) {
	int moves[200] = {0};
	int count = ChessAI_movesEvaluated(ai, moves);
	for (int i=0; i<count; ++i) {
		out += MOVE_TO_STR(out, moves[i]);
	}
	return count;
}

void	frameworkInterface_move(ChessAI* ai, char* in) {
	ChessAI_move(ai, STR_TO_MOVE(in));
}

void	frameworkInterface_moveRandom(ChessAI* ai, char* out) {
	out += MOVE_TO_STR(out, ChessAI_moveRandom(ai));
}

void	frameworkInterface_moveGreedy(ChessAI* ai, char* out) {
	out += MOVE_TO_STR(out, ChessAI_moveGreedy(ai));
}

void	frameworkInterface_moveNegamax(ChessAI* ai, char* out, int depth, int duration) {
	out += MOVE_TO_STR(out, ChessAI_moveNegamax(ai, depth, duration));
}

void	frameworkInterface_moveAlphabeta(ChessAI* ai, char* out, int depth, int duration) {
	out += MOVE_TO_STR(out, ChessAI_moveAlphabeta(ai, depth, duration));
}

void	frameworkInterface_undo(ChessAI* ai) {
	ChessAI_undo(ai);
}