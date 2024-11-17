CC=gcc
CFLAGS=-I./include
BUILDDIR=./build
SRCDIR=./src

all:
	$(CC) $(CFLAGS) -o $(BUILDDIR)/flyp $(SRCDIR)/*.c main.c

debug:
	$(CC) $(CFLAGS) -o $(BUILDDIR)/flyp-debug $(SRCDIR)/*.c main.c -Wall -fsanitize=address

clean:
	rm -f ./build/*
