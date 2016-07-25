#include <math.h>
#include "../../include/nrutil.h"
#include "../../include/general_fns.h"
#include "ch5funcs.h"
#define BIG 1.0e30
//Pade takes a truncated Taylors series expansion of a function and using the same truncated coefficients,
//comes up with another approximation that many times, follows the function a lot more closely.
void pade(
	float cof[], //The 2n coefficients approximating the function.
	int n, //2*n term-approximation of a function.
	float *resid //Norm  of residual vector. Small means good convergence.
	)
/*
*Given cof[0..2*n], the leading terms in the power series expansion of a function, solve the 
*linear Pade equations to return the coefficients of a diagonal rational function approximation to 
*The same function, namely (cof[0] + cof[1].x + ... + cof[n].x^N)/(1+cof[n+1].x + ... + cof[2*n].x^N).
*The value resid is the norm of the residual vector; a small value indicates a well-converged solution.
*/
{
	void lubksb(float **a, int n, int *indx, float b[]);
	void ludcmp(float **a, int n, int *indx, float *d);
	void mprove(float **a, float **alud, int indx[], float b[], float x[]);
	int j, k = 0, *indx;
	float d, rr, rrold, sum, **q, **qlu, *x, *y, *z;

	indx = ivector(1, n);
	q = matrix(1, n, 1, n);
	qlu = matrix(1, n, 1, n);
	x = vector(1, n);
	y = vector(1, n);
	z = vector(1, n);
	for (j = 1; j <= n; j++) //Set up matrix for solving.
	{
		y[j] = x[j] = cof[n + j];
		for(k=1; k<=n; k++)
		{
			q[j][k] = cof[j - k + n];
			qlu[j][k] = q[j][k];
		}
	}
	ludcmp(qlu, n, indx, &d); //Solve by LU decomposition and backsubstitution.
	lubksb(qlu, n, indx, x);//c_{n+k} becomes the RHS of the linear system.
	rr = BIG;
	do //Important to use iterative improvement since Pade approximations tend to be ill-conditioned.
	{
		rrold = rr;
		for (j = 1; j <= n; j++) z[j] = x[j];
		mprove(q, qlu, n, indx, y, x);
		for (rr = 0.0, j = 1; j <= n; j++)//Calculate residual.
			rr += SQR(z[j] - x[j]);		
	} while (rr < rrold);//If we are no longer improving, we can quit.
	*resid = sqrt(rr);
	for (k = 1; k <= n; k++) //Calculate the remaining coefficients.
	{
		//See May29th notes. Once the b_m's are calculated from the second set of equations, they are used to find the a's from the first set via a matrix multiplication.
		sum = cof[k]; //Corresponding to m = 0.
		for (j = 1; j <= k; j++) 
			sum -= x[j] * cof[k - j];//Replace j with m to get the equations in the notes. 
									 //Remember that the second set of equations has negative sign on RHS. This is why we need to -= here which is equivalent to +=.
		y[k] = sum;
	}
	for (j = 1; j <= n; j++) //Copy answers to output.
	{
		cof[j] = y[j];
		cof[j + n] = -x[j];
	}
	free_vector(z, 1, n);
	free_vector(y, 1, n);
	free_vector(x, 1, n);
	free_matrix(qlu, 1, n, 1, n);
	free_matrix(q, 1, n, 1, n);
	free_ivector(indx, 1, n);
}

void pade_debug(
	float cof[], //The 2n coefficients approximating the function.
	int n, //2*n term-approximation of a function.
	float *resid //Norm  of residual vector. Small means good convergence.
	)
/*
*Given cof[0..2*n], the leading terms in the power series expansion of a function, solve the
*linear Pade equations to return the coefficients of a diagonal rational function approximation to
*The same function, namely (cof[0] + cof[1].x + ... + cof[n].x^N)/(1+cof[n+1].x + ... + cof[2*n].x^N).
*The value resid is the norm of the residual vector; a small value indicates a well-converged solution.
*/
{
	void lubksb(float **a, int n, int *indx, float b[]);
	void ludcmp(float **a, int n, int *indx, float *d);
	void mprove(float **a, float **alud, int indx[], float b[], float x[]);
	int j, k = 0, *indx;
	float d, rr, rrold, sum, **q, **qlu, *x, *y, *z;

	indx = ivector(1, n);
	q = matrix(1, n, 1, n);
	qlu = matrix(1, n, 1, n);
	x = vector(1, n);
	y = vector(1, n);
	z = vector(1, n);
	printf("Input coefficients:\n");
	pprint1d_float(cof, 6);
	for (j = 1; j <= n; j++) //Set up matrix for solving.
	{
		y[j] = x[j] = cof[n + j];
		for (k = 1; k <= n; k++)
		{
			q[j][k] = cof[j - k + n];
			qlu[j][k] = q[j][k];
		}
	}
	printf("LU matrix:\n");
	pprint2d_float(qlu,3,3);
	printf("\n");
	ludcmp(qlu, n, indx, &d); //Solve by LU decomposition and backsubstitution.
	lubksb(qlu, n, indx, x);
	rr = BIG;
	do //Important to use iterative improvement since Pade approximations tend to be ill-conditioned.
	{
		rrold = rr;
		for (j = 1; j <= n; j++) z[j] = x[j];
		mprove(q, qlu, n, indx, y, x);
		for (rr = 0.0, j = 1; j <= n; j++)//Calculate residual.
			rr += SQR(z[j] - x[j]);
	}
	while (rr < rrold);//If we are no longer improving, we can quit.
	*resid = sqrt(rr);
	for (k = 1; k <= n; k++) //Calculate the remaining coefficients.
	{
		for (sum = cof[k], j = 1; j <= k; j++) 
			sum -= x[j] * cof[k - j];
		y[k] = sum;
	}
	for (j = 1; j <= n; j++) //Copy answers to output.
	{
		cof[j] = y[j];
		cof[j + n] = -x[j];
	}
	free_vector(z, 1, n);
	free_vector(y, 1, n);
	free_vector(x, 1, n);
	free_matrix(qlu, 1, n, 1, n);
	free_matrix(q, 1, n, 1, n);
	free_ivector(indx, 1, n);
}
