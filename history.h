#ifndef HISTORY_H_LOCK
#define HISTORY_H_LOCK

typedef struct History {
    int move;
    int white_score;
    int black_score;
    char src_piece;
    char dest_piece;
} History;

void    History_init(History* self, int move, char src_piece, char dest_piece, int white_score, int black_score);

#endif
