@echo off

echo "Compiling Numerical Recipies Code"

if exist .\obj\fileio.o (
	echo "lib already compiled"
)
if not exist .\obj\fileio.o (
	echo "lib not compiled, recompiling"
	cd lib
	make
	cd ..
)

::Now we can run the test program to test it.
bin\lib\tst_libfns.exe data\matrix_file

