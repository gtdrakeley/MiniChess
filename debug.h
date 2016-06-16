#ifndef DEBUG_H_LOCK
#define DEBUG_H_LOCK

#include <stdio.h>
#include <errno.h>
#include <string.h>

#ifdef NODEBUG
#define debug(S, ...)
#else
#define debug(S, ...) fprintf(stderr, "DEBUG %s:%d: " S "\n", __FILE__, __LINE__, ##__VA_ARGS__)
#endif

#ifdef NOOUTPUT
// #define OUTPUT(S, ...)
#define OUTPUT(OUT)
#else
// #define OUTPUT(S, ...) printf((S), ##__VA_ARGS__)
#define OUTPUT(OUT) OUT
#endif

#ifdef NOERR
#define strerr()
#define log_error(S, ...)
#define log_warning(S, ...)
#define log_info(S, ...)
#define verify(C, S, ...)
#define guard(S, ...)
#define verify_mem(M, ...)
#define verify_debug(C, S, ...)
#else
#define strerr() (errno == 0 ? "None" : strerror(errno))
#define log_error(S, ...) fprintf(stderr, "[ERROR] (%s:%d: %s) " S "\n", __FILE__, __LINE__, strerr(), ##__VA_ARGS__)
#define log_warning(S, ...) fprintf(stderr, "[WARNING] (%s:%d: %s) " S "\n", __FILE__, __LINE__, strerr(), ##__VA_ARGS__)
#define log_info(S, ...) fprintf(stderr, "[INFO] (%s:%d) " S "\n", __FILE__, __LINE__, ##__VA_ARGS__)
#define verify(C, S, ...) if(!(C)) { log_error(S, ##__VA_ARGS__); errno=0; goto error; }
#define sentry(S, ...) { log_error(S, ##__VA_ARGS__); errno=0; goto error; }
#define verify_mem(M, ...) verify((M), "Memory error.")
#define verify_debug(C, S, ...) if(!(C)) { debug(S, ##__VA_ARGS__); errno=0; goto error; }
#endif

#define noop ((void)0)
#define terminate fprintf(stderr, "TERMINATING\n"); exit(EXIT_FAILURE)

#endif
