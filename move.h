#ifndef MOVE_H_LOCK
#define MOVE_H_LOCK

#include <stdio.h>

extern char* MOVE_CONV[];

#define MOVE_GEN(SRC, DEST) ((SRC) | ((DEST) << 5))

#define MOVE_SRC(MV) ((MV) & 0x1f)

#define MOVE_DEST(MV) (((MV) >> 5) & 0x1f)

#define MOVE_TO_STR(OUT, MV) sprintf((OUT), "%s-%s\n", MOVE_CONV[MOVE_SRC((MV))], MOVE_CONV[MOVE_DEST((MV))])

#define STR_TO_MOVE(STR) Move_fromStr((STR))

int     Move_fromStr(char* str);

#endif
