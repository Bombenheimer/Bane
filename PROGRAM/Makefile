CC=gcc
CFLAGS=-Wall -Wextra -std=c99 -pedantic -march=native -g
LDFLAGS=-lncurses -lcurl

all: bane

bane: bane.o
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

bane.o: bane.c
	$(CC) $(CFLAGS) -c $< -o $@
