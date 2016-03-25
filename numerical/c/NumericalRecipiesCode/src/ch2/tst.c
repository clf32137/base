#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include "../../include/nrutil.h"


/********************************************************
*Gneral purpose C functions.
********************************************************/
int read_matrix(float** mat, char* filename, int rows, int cols)
{
	FILE *file;
	char *buffer;
	int ret, row = 0, i, j;

	// Set Field Separator here
	char delims[] = " ";
	char *result = NULL;
	// Memory allocation
	if ((file = fopen(filename, "r")) == NULL){
		fprintf(stdout, "Error: Can't open file !\n");
		return -1;
	}
	while(!feof(file))
	{
		//buffer = static_cast<char*>(malloc(sizeof(char) * 4096));
		buffer = (char*) malloc (sizeof(char)*4096);
		memset(buffer, 0, 4096);
		ret = fscanf(file, "%4095[^\n]\n", buffer);
		if (ret != EOF && row < rows) 
		{
			int field = 0;
			result = strtok(buffer,delims);
			while(result!=NULL)
			{
				 // Set no of fields according to your requirement
				if(field>cols)break;
				mat[row+1][field+1] = atof(result);
				result = strtok(NULL,delims);
				field++;
			}
			++row;
		}
		free(buffer);
	}
	fclose(file);
	return -1;
 }

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
		0, // toy data
		0, // gauss jordan
		0, // lu decomposition
		0, // solve equations with lu
		0, // improvement of solution
		0, // singular value decomposition
		1, // sparse matrix
		1  // sove sparse matrix system of equations.
	};
	int printindx = 0;
////////////////////////////////////////////
//Create toy data.
////////////////////////////////////////////
	int i, j;
	int dim = 4;
	float **a;
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
	read_matrix(mat, "../../data/matrix_file", 4, 4);
	
	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Read in matrix from a file\n###################\n");
		printMatrix(mat, 4, 4);
	}

/////////////////////////////////////////////
//Gauss Jordan on toy matrices.
/////////////////////////////////////////////
	

	if(shouldiprint[printindx++])
	{
		fillmatrix(a, matrixa, 4, 4);
		fillmatrix(b, matrixb, 4, 4);
		gaussj(a, 4, b, 4);

		printf("\n###################\n Gauss Jordan\n###################  \n");
		printMatrix(a, 4, 4);
		printMatrix(b, 4, 4);
	}

/////////////////////////////////////////////
//LU decomposition.
/////////////////////////////////////////////
	float *d;
	int *ind; ind = ivector(1,4);
	
	if(shouldiprint[printindx++])
	{
		
		ludcmp(mat, 4, ind, d);
		printf("\n###################\n LU decomposition\n###################\n");
		printMatrix(mat, 4, 4);
		printf("%1f\n",*d);
		for(i=0; i<4; i++)
			printf("%d\t",ind[i+1]);
	}

/////////////////////////////////////////////
//Recreate original matrix.
/////////////////////////////////////////////
	
	float **per;
	float **l; l = matrix(1, 4, 1, 4);
	float **u; u = matrix(1, 4, 1, 4);
	float **origmat; origmat = matrix(1, 4, 1, 4);
	float **temp1; temp1 = matrix(1, 4, 1, 4);

	if(shouldiprint[printindx - 1]) // We still want to check the lu decomposition flag and not increase the index.
	{
		per = matrix(1, 4, 1, 4);
		convertIndToPermutationMatrix(ind, per, 4);
	
		populatelu(mat, l, u, 4);	
		mmult(per, 4, 4, l, 4, 4, temp1); //temp1 = P.L
		mmult(temp1, 4, 4, u, 4, 4, origmat); //orig = temp1.U

		printf("\n###################\n Recreate original matrix\n###################\n");
		printMatrix(origmat, 4, 4);
	}

/////////////////////////////////////////////
//Now use backsubstitution to solve linear equations.
/////////////////////////////////////////////
	

	if(shouldiprint[printindx++])
	{
		for(i=1;i<=4;i++)
			c[i] = i;

		fillmatrix(a, matrixa, 4, 4);
		ludcmp(a, 4, ind, d);

		printf("\n###################\n Solve equations with LU\n###################\n");
		printMatrix(a, 4, 4);
		for(i=0; i < dim; i++)
			printf("%d%s", ind[i+1], i < dim-1 ? "\t" : "\n");
	}
	
	
	
	if(shouldiprint[printindx - 1])
	{
		lubksb(a, 4, ind, c);

		for(i=0; i < dim; i++)
			printf("%lf%s",c[i+1], i < dim-1 ? "\t" : "\n");
	}

/////////////////////////////////////////////
//Does the routine that improves solutions improve this one much?
/////////////////////////////////////////////
	float *b1; b1 = vector(1,4);
	if(shouldiprint[printindx++])
	{		
		for(i=1;i<=4;i++)
			b1[i] = i;
		fillmatrix(b, matrixa, 4, 4); // We need the original matrix as well as the ludecomposed version. So, we will fill the original into b.
		mprove(b, a, dim, ind, b1, c); // c contained the original solution from lubksb.

		printf("\n###################\n Improvement of solution\n###################\n");
		//I guess there is no improvement.
		for(i = 0; i < dim; i++)
			printf("%lf%s",c[i+1], i < dim-1 ? "\t" : "\n");
	}

////////////////////////////////////////////
//SVD on toy matrices.
////////////////////////////////////////////
		
	if(shouldiprint[printindx++])
	{
		fillmatrix(a, matrixa, 4, 4);
		fillmatrix(b, matrixb, 4, 4);
		svdcmp(a, dim, dim, c, b);

		printf("\n###################\nSingular Value Decomposition\n###################  \n");
		printMatrix(a, 4, 4);
		printMatrix(b, 4, 4);
		for(i=0; i < dim; i++)
			 printf("%lf%s",c[i+1], i < dim-1 ? "\t" : "\n");
	}

////////////////////////////////////////////
//Read in sparse matrix.
////////////////////////////////////////////
	
	unsigned long nmax = 50;
	float sa[50];
	unsigned long ija[50];
	float thresh = 0.01f;
	
	dim = 5;

	if(shouldiprint[printindx++])
	{
		a = matrix(1, 5, 1, 5);
		fillmatrix(a, matrixa, 5, 5);
		int sparseelements = sprsin(a, 5, thresh, nmax, sa, ija); //Somehow, 1.0 in the matrix is treated as less than the threshold.

		printf("\n###################\nSparse storage\n###################  \n");
		printMatrix(a, 5, 5);

		for(i=0; i < sparseelements; i++)
			 printf("%lf%s", sa[i+1], i < sparseelements - 1 ? "\t" : "\n");

		for(i=0; i < sparseelements; i++)
			 printf("%lu%s", ija[i+1], i < sparseelements - 1 ? "\t" : "\n");

		float *b;
		b = vector(1,5);
		float *x;
		x = vector(1,5);
		for(i=1; i<= 5; i++)
			x[i] = 1.0f;

		sprsax(sa, ija, x, b, 5);
		for(i=0; i < 5; i++)
			 printf("%lf%s",b[i+1], i < dim-1 ? "\t" : "\n");

		sprstx(sa, ija, x, b, 5);
		for(i=0; i < 5; i++)
			 printf("%lf%s",b[i+1], i < dim-1 ? "\t" : "\n");
	}

////////////////////////////////////////////
//Solve system of sparse equations.
////////////////////////////////////////////
	double dsa[50];
	if(shouldiprint[printindx++])
	{
		da = dmatrix(1, 5, 1, 5);
		dfillmatrix(da, dmatrixa, 5, 5);
		int sparseelements = dsprsin(da, 5, thresh, nmax, dsa, ija); //Somehow, 1.0 in the matrix is treated as less than the threshold.
		printf("\n###################\nSparse equation solver\n###################  \n");
		for(i = 0; i < sparseelements; i++)
			 printf("%f%s", dsa[i+1], i < sparseelements - 1 ? "\t" : "\n");
		for(i = 0; i < sparseelements; i++)
			 printf("%lu%s", ija[i+1], i < sparseelements - 1 ? "\t" : "\n");

		double * db1; db1 = dvector(1,5); for(i=0;i<5;i++)db1[i+1]=1;
		double * dx1; dx1 = dvector(1,5); for(i=0;i<5;i++)dx1[i+1]=1;
		int iter;
		double err;
		unsigned long n = 5;

		linbcg(ija, dsa, n, db1, dx1, 1, 1e-4, 20, &iter, &err);
		
		for(i = 0; i < n; i++)
			 printf("%f%s", dx1[i+1], i < n - 1 ? "\t" : "\n");

	}

	//Cleanup..
	free_matrix(a, 1, 4, 1, 4);
	free_dmatrix(da, 1, 5, 1, 5);
	free_matrix(b, 1, 4, 1, 4);
	free_matrix(mat, 1, 4, 1, 4);
	free_vector(c, 1, 4);
	free_ivector(ind, 1, 4);
}

//[1] http://stackoverflow.com/questions/3836519/reading-a-delimited-file-with-fscanf
//[2] https://github.com/githubapitest/githubapitest/tree/master/numerical-recipes-j/core/src/main/java/com/google/code/numericalrecipes

