all:
	gcc -std=c99 chessai.c cjson.c main.c zeromq.c move.c finterface.c -o client -lm -lzmq
