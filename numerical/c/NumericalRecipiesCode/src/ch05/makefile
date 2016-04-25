#This makefile compiles only source files in chapter-2.
IDIR =../../include
CC=gcc
CFLAGS=-I$(IDIR)

ODIR=../../obj
LDIR =../../lib

LIBS=-lm

_DEPS = nrutil.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = nrutil.o fileio.o 3-ddpoly.o 3-poynomial.o 3-poldiv.o tst5.o

OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

../../bin/ch5/tst5: $(OBJ)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~

#[1] http://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/
#[2] http://stackoverflow.com/questions/5950395/makefile-to-compile-multiple-c-programs
