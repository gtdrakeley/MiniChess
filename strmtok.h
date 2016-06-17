#ifndef STRMTOK_H_LOCK
#define STRMTOK_H_LOCK

void    strmtok_init(int num, ...);
char*   strmtok(char* base, char* delims);
void    strmtok_end();

#endif
