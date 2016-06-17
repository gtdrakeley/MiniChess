#include "strmtok.h"

#include <stdlib.h>
#include <string.h>
#include <stdarg.h>



char**  BASES = NULL;
char**  CURRENTS = NULL;
int     NUM = 0;



int     compare(const void* a, const void* b) {
    return ((*(char**)a) - (*(char**)b));
}


int     find_current(char* base) {
    int low = 0;
    int high = NUM-1;
    int mid;

    while (low <= high) {
        mid = (low + high) / 2;
        if (BASES[mid] > base) {
            high = mid - 1;
        } else if (BASES[mid] < base) {
            low = mid + 1;
        } else {
            return mid;
        }

    }

    return -1;
}


void    strmtok_init(int num, ...) {
    BASES = calloc(num, sizeof(char*));
    CURRENTS = calloc(num, sizeof(char*));
    va_list v1;

    va_start(v1, num);
    for (int i=0; i<num; ++i) { BASES[i] = va_arg(v1, char*); }
    va_end(v1);
    qsort(BASES, num, sizeof(char*), compare);
    for (int i=0; i<num; ++i) { CURRENTS[i] = BASES[i]; }
    NUM = num;
}


char*   strmtok_token(char* base, char* delims) {
    int c_idx = find_current(base);
    char* current = CURRENTS[c_idx];
    
    for (;; ++(CURRENTS[c_idx])) {
        if (*(CURRENTS[c_idx]) == '\0') {
            return current;
        } else if (strchr(delims, *(CURRENTS[c_idx]))) {
            *((CURRENTS[c_idx])++) = '\0';
            return current;
        }
    }
}


void    strmtok_end() {
    free(BASES); BASES = NULL;
    free(CURRENTS); CURRENTS = NULL;
    NUM = 0;
}
