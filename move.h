#ifndef MOVE_H_LOCK
#define MOVE_H_LOCK

#include <stdio.h>

extern char* MOVE_TO_STR[];

#define moveCreate(SRC, DEST) (SRC | (DEST << 5))

#define moveSrc(MV) (MV & 0x1f)

#define moveDest(MV) ((MV >> 5) & 0x1f)

#define moveStr(OUT, MV) sprintf(OUT, "%s-%s\n", MOVE_TO_STR[moveSrc(MV)], MOVE_TO_STR[moveDest(MV)])

// int moveStr(char* out, int mv);

#endif
