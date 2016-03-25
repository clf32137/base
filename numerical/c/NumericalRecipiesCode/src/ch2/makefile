#This makefile compiles only source files in chapter-2.
IDIR =../../include
CC=gcc
CFLAGS=-I$(IDIR)

ODIR=../../obj
LDIR =../../lib

LIBS=-lm

_DEPS = nrutil.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = nrutil.o 1-gaussj.o 3-ludcmp.o 3-lubksb.o 5-mprove.o 4-tridag.o 6-svdcmp.o 7-cyclic.o 7-sprsin.o 7-dsprsin.o 7-dsprsax.o 7-dsprstx.o 7-sprsax.o 7-sprstx.o 7-linbcg.o 7-snrm.o 7-atimes.o 7-asolve.o tst.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

../../bin/ch2/tst: $(OBJ)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~

#[1] http://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/
#[2] http://stackoverflow.com/questions/5950395/makefile-to-compile-multiple-c-programs
