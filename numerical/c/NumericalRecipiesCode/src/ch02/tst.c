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
int main(int argc, char *argv[])
{
	//Used to determine which section gets its results printed.
	int shouldiprint[] = 
	{
		1, // toy data
		1, // gauss jordan
		0, // lu decomposition
		0, // solve equations with lu
		0, // improvement of solution
		0, // singular value decomposition
		0, // sparse matrix
		0, // sove sparse matrix system of equations.
		1, // Vandermonde output
		1, // Toeplitz output
		1, // Cholesy output
		1  // QR decomposition.
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
		{3.0f, 5.5f, 2.0f, 0.0f, 0.0f},
		{2.0f, 4.0f, 0.0f, 0.0f, 0.0f},
		{1.0f, 7.0f, 5.0f, 9.0f, 0.0f},
		{4.0f, 0.0f, 0.0f, 0.0f, 2.0f},
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
	//fillmatrix(mat, matrixa, 4,4);
	read_matrix_from_file(mat, "../../data/matrix_file", 4, 4);
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
		
		ludcmp(mat, 4, ind, &d);
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
////////////////////////////////////////////
//Solving Vandermonde matrix
////////////////////////////////////////////
	if(shouldiprint[printindx++])
	{
		printf("\n###################\nSolving a Vandermonde matrix\n###################  \n");
		
		double *x_v;
		x_v = dvector(1,3);
		x_v[1] = 1; x_v[2] = 3; x_v[3] = 5;

		double *w;
		w = dvector(1,3);
		w[1] = 1; w[2] = 1; w[3] = 1;

		double *q; 
		q = dvector(1,3);
		q[1] = 1; q[2] = 4; q[3] = 1;
		

		vander(x_v, w, q, 3);
		for(i=1; i <= 3; i++)
			printf("%f\t", w[i]);
		printf("\n");

	}

	if(shouldiprint[printindx++])
	{
		printf("\n###################\nSolving a Toeplitz matrix\n###################  \n");
		int n_t = 3;
		float *r_t = vector(1, (2*n_t-1));
		r_t[1] = 2; r_t[2] = 3; r_t[3] = 3.2; r_t[4] = 3.5; r_t[5] = 4;

		float *x_t = vector(1,n_t);
		x_t[1] = 1; x_t[2] = 1; x_t[3] = 1;

		float *y_t = vector(1,n_t);
		y_t[1] = 1; y_t[2] = 1; y_t[3] = 1;

		toeplz(r_t, x_t, y_t, n_t);
		for(i=1; i <= 3; i++)
			printf("%f\t", x_t[i]);
		printf("\n");
	}

	if(shouldiprint[printindx++])
	{
		printf("\n###################\nSolving Cholesky\n###################  \n");
		int n_chol = 2;
		float **a_c = matrix(1,n_chol,1,n_chol);
		float *p = vector(1,n_chol);
		float matrixchol[][5] = 
		{
			{3.0f, 3.46f, 2.0f, 3.0f, 3.0f},
			{7.0f, 4.0f, 0.0f, 0.0f, 0.0f},
			{1.0f, 7.0f, 5.0f, 9.0f, 0.0f},
			{4.0f, 0.0f, 0.0f, 2.0f, 2.0f},
			{0.0f, 0.0f, 0.0f, 6.0f, 5.0f}
		};
		fillmatrix(a_c, matrixchol, n_chol, n_chol);

		printf("Input matrix given (should be covariance):\n");
		printMatrix(a_c, n_chol, n_chol);
		printf("After cholesky decomposition:\n");
		choldc(a_c, n_chol, p);
		printMatrix(a_c, n_chol, n_chol);

		printf("\nWe now use this to solve linear equation:\n");
		float *b_chol = vector(1,n_chol);
		b_chol[1] = 2; b_chol[2] = 1;
		float *x_chol = vector(1,n_chol);
		cholslvec(a_c, n_chol, p, b_chol, x_chol);

		printf("\nAnd here is the solution:\n");
		for(i=1; i <= n_chol; i++)
			printf("%f\t", x_chol[i]);
		printf("\n");
	}
	if(shouldiprint[printindx++])
	{
		printf("\n###################\nQR decomposition\n###################\n");
		
        int n_qr = 3;
        float **a_qr = matrix(1,n_qr,1,n_qr);
        float matrixqr[][5] = 
		{
			{3.0f, 3.5f, 2.0f, 3.0f, 3.0f},
			{7.0f, 4.0f, 0.0f, 0.0f, 0.0f},
			{1.0f, 7.0f, 5.0f, 9.0f, 0.0f},
			{4.0f, 0.0f, 0.0f, 2.0f, 2.0f},
			{0.0f, 0.0f, 0.0f, 6.0f, 5.0f}
		};
				
		fillmatrix(a_qr, matrixqr, n_qr, n_qr);

		float *c_qr = vector(1,n_qr);
		float *d_qr = vector(1,n_qr);
		int *sign;
		
		qrdcmp(a_qr,n_qr,c_qr,d_qr,&sign);
		printf("\nQR decomposition of matrix\n");
		printMatrix(a_qr,n_qr,n_qr);
		

		float *b_qr = vector(1,n_qr);
		b_qr[1] = 1; b_qr[2] = 5; b_qr[3] = 7;
		printf("\nNow using it to solve a system\n");
		qrsolv(a_qr, n_qr, c_qr, d_qr, b_qr);
		printf("\nAnd here is the solution:\n");
		for(i=1; i <= n_qr; i++)
			printf("%f\t", b_qr[i]);
		printf("\n");
	}


	//Freeze the console so I can look at the output.
	char str1[20];
	scanf("%s", str1);

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
//[3] http://stackoverflow.com/questions/21873048/getting-an-error-fopen-this-function-or-variable-may-be-unsafe-when-complin
