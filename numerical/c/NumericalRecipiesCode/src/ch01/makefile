#This makefile compiles only source files in chapter-1.
IDIR =../../include
CC=gcc
CFLAGS=-I$(IDIR)

ODIR=../../obj
LDIR =../../lib

LIBS=-lm

_DEPS = nrutil.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = nrutil.o flmoon.o julday.o friday13thFullMoon.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))


$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

../../bin/ch1/fullmoons: $(OBJ)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~

#[1] http://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/
#[2] http://stackoverflow.com/questions/5950395/makefile-to-compile-multiple-c-programs
