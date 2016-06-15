#include "test.h"

#include <stdlib.h>
#include <stdio.h>

#include "chessai.h"
#include "debug.h"


int main(int argc, char** argv) {
	int w_time;
	int b_time;
	unsigned long long start;
    int w_wins = 0;
    int b_wins = 0;
    int ties = 0;
    ChessAI white;
    ChessAI black;
    
    ChessAI_init(&white);
    ChessAI_init(&black);

    while ((w_wins + b_wins + ties) < 10) {
        ChessAI_reset(&white);
        ChessAI_reset(&black);
		w_time = 300000;
		b_time = 300000;
        while (true) {
			start = msec();
            ChessAI_moveAlphabeta(&white, -1, w_time);
			w_time -= msec() - start;
            ChessAI_sync(&white, &black);
            if (ChessAI_winner(&white) != '?' || w_time <= 0) { break; }
			start = msec();
            ChessAI_moveAlphabeta(&black, -1, b_time);
			b_time -= msec() - start;
            ChessAI_sync(&black, &white);
            if (ChessAI_winner(&black) != '?' || b_time <= 0) { break; }
        }
        if (ChessAI_winner(&white) == 'W') {
            ++w_wins;
        } else if (ChessAI_winner(&white) == 'B' ) {
            ++b_wins;
        } else if (ChessAI_winner(&white) == '=') {
            ++ties;
		} else if (w_time <= 0) {
			++b_wins;
		} else if (b_time <= 0) {
			++w_wins;
        } else {
            sentry("Game exited with winner \"?\"");
        }
    
        printf("%d : %d : %d\n", w_wins, b_wins, ties);
    }

    ChessAI_destroy(&white);
    ChessAI_destroy(&black);
    
    return 0;

error:
    return 1;
}
