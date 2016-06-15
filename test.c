#include "test.h"

#include <stdlib.h>
#include <stdio.h>

#include "chessai.h"
#include "debug.h"


int main(int argc, char** argv) {
    int w_wins = 0;
    int b_wins = 0;
    int ties = 0;
    ChessAI white;
    ChessAI black;
    
    ChessAI_init(&white);
    ChessAI_init(&black);

    while ((w_wins + b_wins + ties) < 100) {
        ChessAI_reset(&white);
        ChessAI_reset(&black);
        while (true) {
            ChessAI_moveAlphabeta(&white, 4, 0);
            ChessAI_sync(&white, &black);
            if (ChessAI_winner(&white) != '?') { break; }
            ChessAI_moveAlphabeta(&black, -1, 2000);
            ChessAI_sync(&black, &white);
            if (ChessAI_winner(&black) != '?') { break; }
        }
        if (ChessAI_winner(&white) == 'W') {
            ++w_wins;
        } else if (ChessAI_winner(&white) == 'B') {
            ++b_wins;
        } else if (ChessAI_winner(&white) == '=') {
            ++ties;
        } else {
            sentry("Game exitied with winner \"?\"");
        }
    
        printf("%d : %d : %d\n", w_wins, b_wins, ties);
    }
    
    return 0;

error:
    return 1;
}
