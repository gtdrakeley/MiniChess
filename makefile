all:
	gcc -std=c99 -Wall chessai.c cjson.c main.c zeromq.c move.c finterface.c history.c slavesort.c -o client -lm -lzmq
