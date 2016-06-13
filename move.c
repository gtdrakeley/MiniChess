#include "move.h"

#include <string.h>


/*********************************  CONSTANTS  **********************************/
char* MOVE_CONV[] = {
	"a6", "b6", "c6", "d6", "e6",
	"a5", "b5", "c5", "d5", "e5",
	"a4", "b4", "c4", "d4", "e4",
	"a3", "b3", "c3", "d3", "e3",
	"a2", "b2", "c2", "d2", "e2",
	"a1", "b1", "c1", "d1", "e1"
};


/**********************************  METHODS  ***********************************/
int		Move_fromStr(char* str) {
	char** src = MOVE_CONV;
	char** dest = MOVE_CONV;
	char* src_str = strtok(str, "-\n");
	char* dest_str = strtok(NULL, "-\n");
	for (int i=0; i<30; ++i) {
		if (strncmp(src_str, MOVE_CONV[i], 2) == 0) {
			src += i;
		} else if (strncmp(dest_str, MOVE_CONV[i], 2) == 0) {
			dest += i;
		}
	}
	return MOVE_GEN(src-MOVE_CONV, dest-MOVE_CONV);
}
