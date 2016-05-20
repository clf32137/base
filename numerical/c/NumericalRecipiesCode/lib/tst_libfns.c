#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include "../include/nrutil.h"
#include "../include/fileio.h"

int main(int argc, char **argv)
{
	char * fileToRead = "../../data/matrix_file";
	if(argc > 1)
		fileToRead = argv[1];

	printf("Reading matrix file %s\n", fileToRead);
	float **mat;
	mat = matrix(1, 4, 1, 4);
	read_matrix_from_file(mat, fileToRead, 4, 4);
	if(argc == 1)
	{ //Only pause the console if no arguments are given. Which means double-clicking the exe.
		char str1[20];
		scanf("%s", str1);
	}
}

