#include "main.h"

int main_intZeromq = 54361; // CHANGE THIS - OPTIONAL
char* main_charName = "Arathanis"; // CHANGE THIS - REQUIRED

void main_sigint() {
    {
        zeromq_stop();
    }
}

int main(int argc, char** argv) {
    {
        assert(main_intZeromq > 1024);
        assert(main_intZeromq < 65535);
        
        assert(strlen(main_charName) > 2);
        assert(strlen(main_charName) < 16);
        assert(strstr(main_charName, " ") == NULL);
    }
    
    {
        srand(milliseconds());
    }
    
    {
        signal(SIGINT, main_sigint);
    }
    
    {
        char* fname = NULL;

        if (argc == 2) { fname = argv[1]; }
        ChessAI ai;
        ChessAI_init(&ai, fname);
        zeromq_start(&ai);
        ChessAI_destroy(&ai);
    }
    
    return 0;
}
