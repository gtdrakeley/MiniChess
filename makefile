client:
	gcc -std=c99 -Wall chessai.c cjson.c main.c zeromq.c move.c finterface.c history.c slavesort.c -o client -lm -lzmq

test: test.h test.c chessai.h chessai.c move.h move.c history.h history.c slavesort.h slavesort.c debug.h
	gcc -std=c99 -Wall test.c chessai.c move.c history.c slavesort.c -o test
