all:

client: chessai.h chessai.c cjson.h cjson.c main.h main.c zeromq.h zeromq.c finterface.h finterface.c history.h history.c slavesort.h slavesort.c strmtok.h strmtok.c debug.h
	gcc -std=c99 -Wall chessai.c cjson.c main.c zeromq.c move.c finterface.c history.c slavesort.c strmtok.c -o client -lm -lzmq

test: test.h test.c chessai.h chessai.c move.h move.c history.h history.c slavesort.h slavesort.c strmtok.h strmtok.c debug.h
	gcc -std=c99 -Wall test.c chessai.c move.c history.c slavesort.c strmtok.c -o test
