void mprove(a, alud, n, indx, b, x)
/*************************************
Improves a solution vector x[1..n] of the linear set of equations A.X = B.
The matrix a[1..n][1..n] and the vectors b[1..n] and x[1..n] are input as is dimension n.
Also input is alud[1..n][1..n], the LU decomposition of a as returned by ludcmp and
indx[1..n] also returned by the routine. On output, only x[1..n] is modified to improved values.
************************************/

float **a, **alud, b[], x[];
int n, indx[];
{
	int j,i;
	double sdp;
	float *r, *vector();
	void lubksb(), free_vector();

	r = vector(1,n);
	for (i = 1; i <= n; i++) { //calculate the RHS of 2.5.4.
		sdp = -b[i];	 //Accumulating the residual in double precision.
		for (j = 1; j <= n; j++) sdp += a[i][j]*x[j]; //x is actual (x+\delta x) here.
		r[i] = sdp;
	}
	lubksb(alud, n, indx, r);	//Solve for the error term, \delta x. This is put into r.
	for (i = 1; i <= n; i++) x[i] -= r[i]; //And subtract it from the old solution.
	free_vector(r, 1, n);
}
