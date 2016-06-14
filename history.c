#include "history.h"



void    History_init(History* self, int move, char src_piece, char dest_piece, int white_score, int black_score) {
    self->move = move;
    self->src_piece = src_piece;
    self->dest_piece = dest_piece;
    self->white_score = white_score;
    self->black_score = black_score;
}
