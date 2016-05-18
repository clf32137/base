#This makefile compiles only source files for lib functions.
IDIR =../include
CC=gcc
CFLAGS=-I$(IDIR)

ODIR=../obj
#LDIR =../lib

LIBS=-lm

_DEPS = nrutil.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = nrutil.o fileio.o general_fns.o tst_libfns.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

../bin/lib/tst_libfns: $(OBJ)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~

#[1] http://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/
#[2] http://stackoverflow.com/questions/5950395/makefile-to-compile-multiple-c-programs
