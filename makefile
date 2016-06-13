all:
	gcc -std=c99 chess.c cjson.c main.c zeromq.c move.c -o client -lm -lzmq
