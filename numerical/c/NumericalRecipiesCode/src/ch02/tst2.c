#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include "../../include/nrutil.h"
#include "../../include/fileio.h"

/********************************************************
*general matrix operations.
********************************************************/
void fillmatrix(float **a, float mat[5][5], int ros, int cols)
{
	int i,j;
	for(i=0;i<ros;i++)
		for(j=0;j<cols;j++)
			a[i+1][j+1] = mat[i][j];
}

void dfillmatrix(double **a, double mat[5][5], int ros, int cols)
{
	int i,j;
	for(i=0;i<ros;i++)
		for(j=0;j<cols;j++)
			a[i+1][j+1] = mat[i][j];
}

void printMatrix(float **a, int ros, int cols)
{
	int i,j;
	for(i=0;i<ros;i++)
		for(j=0;j<cols;j++)
			printf("%lf%s",a[i+1][j+1], j < cols-1 ? "\t" : "\n");
	printf("\n");
}

void mmult(float **a, int rowa, int cola, float **b, int rowb, int colb, float **c)
{
    if (cola != rowb) {
        printf("Matrix multiplication can not be performed.");
        return;
    }
    int i,j,k;
    for (i = 1; i <= rowa; i++) {
        for (j = 1; j <= colb; j++) {
            float temp = 0;
            for (k = 1; k <= rowa; k++) {
                temp += a[i][k]*b[k][j];
            }
            c[i][j] = temp;
        }
    }
}

/********************************************************
*ludcmp supplementary routines.
********************************************************/
//Convert the ind vector from ludcmp into a permutation matrix.
void convertIndToPermutationMatrix(int* ind, float **a, int n)
{
	int i,j;

	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			if(ind[i+1] == j+1)
				a[i+1][j+1] = 1;
			else
				a[i+1][j+1] = 0;

		}
		ind[ind[i+1]] = i+1;
	}
}

// Convert the compressed matrix returned by ludcmp into P, L and U.
void populatelu(float **mat, float **l, float **u, int ros) //Only makes sense for square matrices.
{
	int i, j;
	for(i=1;i<=ros;i++)
	{
		l[i][i] = 1;
		u[i][i] = mat[i][i];
		for(j=1;j<i;j++)
		{
			l[i][j] =  mat[i][j];
			u[i][j] = 0;
		}
		if(i != ros)
			for(j=i+1;j<=ros;j++)
			{
				u[i][j] = mat[i][j];
				l[i][j] = 0;
			}
	}
}

//For testing in python.
/*[
 	[ 0,  1,  0,  0],
    [ -1,  0,  0,  0],
    [ 0,  0,  1,  0],
    [ 0,  0,  0, 1]
]*/
int main()
{
	//Used to determine which section gets its results printed.
	int shouldiprint[] = 
	{
		1, // toy data
		1, // gauss jordan
		1, // lu decomposition
		0, // solve equations with lu
		0, // improvement of solution
		0, // singular value decomposition
		0, // sparse matrix
		0, // sove sparse matrix system of equations.
		0, // Vandermonde output
		0, // Toeplitz output
		0  // Cholesy output
	};
	int printindx = 0;
////////////////////////////////////////////
//Create toy data.
////////////////////////////////////////////
	int i, j;
	int dim = 4;
	float **a; a = matrix(1,4,1,4);
	double **da;
	da = dmatrix(1, 4, 1, 4);
	float matrixa[][5] = 
	{
		{3.0f, 0.0f, 2.0f, 0.0f, 0.0f},
		{0.0f, 4.0f, 0.0f, 0.0f, 0.0f},
		{0.0f, 7.0f, 5.0f, 9.0f, 0.0f},
		{0.0f, 0.0f, 0.0f, 0.0f, 2.0f},
		{0.0f, 0.0f, 0.0f, 6.0f, 5.0f}
	};
	
	double dmatrixa[][5] = 
	{
		{3.0, 0.0, 1.0, 0.0, 0.0},
		{0.0, 4.0, 0.0, 0.0, 0.0},
		{0.0, 7.0, 5.0, 9.0, 0.0},
		{0.0, 0.0, 0.0, 0.0, 2.0},
		{0.0, 0.0, 0.0, 6.0, 5.0}
	};

	float **b;
	b = matrix(1, 4, 1, 4);
	float matrixb[][5] =
	{
		{3.0f, 0.0f, 2.0f, 0.0f, 0.0f},
		{0.0f, 4.0f, 0.0f, 0.0f, 0.0f},
		{0.0f, 7.0f, 5.0f, 9.0f, 0.0f},
		{0.0f, 0.0f, 0.0f, 0.0f, 2.0f},
		{0.0f, 0.0f, 0.0f, 6.0f, 5.0f}
	};
	
	float *c;
	c = vector(1,4);

/////////////////////////////////////////////
//Read matrix from file instead of hard coding.
/////////////////////////////////////////////
	float **mat; mat = matrix(1, 4, 1, 4);
	fillmatrix(mat, matrixa, 4,4);
	//read_matrix(mat, "../../data/matrix_file", 4, 4);
	//read_matrix_from_file(mat, "../../data/matrix_file", 4, 4);
	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Read in matrix from a file\n###################\n");
		printMatrix(mat, 4, 4);
	}

	if(shouldiprint[printindx++])
	{
		fillmatrix(a, matrixa, 4, 4);
	}

}

//[1] http://stackoverflow.com/questions/3836519/reading-a-delimited-file-with-fscanf
//[2] https://github.com/githubapitest/githubapitest/tree/master/numerical-recipes-j/core/src/main/java/com/google/code/numericalrecipes

