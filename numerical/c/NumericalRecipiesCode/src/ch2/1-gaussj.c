#include <math.h>

#define SWAP(a,b) {float temp=(a);(a)=(b);(b)=temp;}

void gaussj(a,n,b,m)
/******************************************************************************************************
Linear equation solution by Gauss-Jordan elimination, equation (2.1.1). 
a[1..n][1..n] is the input matrix. b[1..n][1..m] is input containing the m right-hand side vectors. 
On output, a is replaced by its matrix inverse, and b is replaced by the corresponding set of solution vectors.
*******************************************************************************************************/
float **a, **b;
int n, m;
{
	int *indxc, *indxr, *ipiv;
	int i, icol, irow, j, k, l, ll, *ivector();
	float big, dum, pivinv;
	void nrerror(), free_ivector();

	indxc = ivector(1,n); //These three are used for book keeping on pivoting
	indxr = ivector(1,n);
	ipiv = ivector(1,n);

	for (j=1; j <= n; j++) ipiv[j] = 0;

	for (i=1; i <= n; i++) //The main loop over the columns to be reduced.
	{
		big=0.0;
		for (j=1; j <= n; j++)
			if (ipiv[j] != 1)
				for (k=1; k <= n; k++) //The outer loop where we search for a pivot element.
				{
					if (ipiv[k] == 0)
					{
						if (fabs(a[j][k]) >= big)
						{
							big = fabs(a[j][k]);
							irow = j;
							icol = k;
						}
					}
					else if (ipiv[k] > 1) nrerror("GAUSSJ: Singular Matrix-1"); //This means we hit the same row as pivot twice. 
				}
		++(ipiv[icol]);
		//We now have the pivot element, so we interchange rows, if needed, to put the pivot 
		//element on the diagonal. The columns are not physically interchanged, only relabeled: 
		//indxc[i], the column of the ith pivot element, is the ith column that is reduced, 
		//while indxr[i] is the row in which that pivot element was originally located. 
		//If indxr[i] != indxc[i] there is an implied column interchange. With this form of bookkeeping, 
		//the solution b’s will end up in the correct order, and the inverse matrix will be scrambled by columns. 
		if (irow != icol)
		{
			for (l=1;l<=n;l++) SWAP(a[irow][l],a[icol][l])
			for (l=1;l<=m;l++) SWAP(b[irow][l],b[icol][l])
		}
		indxr[i] = irow; // We are now ready to divide the pivot row by the pivot element. located at irow, icol.
		indxc[i] = icol;
		
		if (a[icol][icol] == 0.0) nrerror("GAUSSJ: Singular Matrix-2");//Given that this is the index corresponding to max, it being zero means whole row was zero.
		
		pivinv = 1.0 / a[icol][icol];
		
		a[icol][icol]=1.0;
		
		for (l=1;l<=n;l++) a[icol][l] *= pivinv;
		for (l=1;l<=m;l++) b[icol][l] *= pivinv;
		
		for (ll=1; ll <= n; ll++) //Convert all rows except the one with the pivot to zeros above and below the pivot.
			if (ll != icol)
			{
				dum = a[ll][icol];
				a[ll][icol] = 0.0;
				for (l=1; l <= n; l++) a[ll][l] -= a[icol][l] * dum; //Loop through the columns and for the whole row, subtract dum times the pivot row. The pivot itself is by now, 1.
				for (l=1; l <= m; l++) b[ll][l] -= b[icol][l] * dum; 
			}
	}
	//This is the end of the main loop over columns of the reduction. It only remains to unscramble
	//the solution in view of the column interchanges. We do this by interchanging pairs of
	//columns in reverse order that the permutation was built up.
	for (l=n; l >= 1; l--)
	{
		if (indxr[l] != indxc[l])
			for (k=1;k<=n;k++)
				SWAP(a[k][indxr[l]],a[k][indxc[l]]);
	}

	free_ivector(ipiv,1,n);
	free_ivector(indxr,1,n);
	free_ivector(indxc,1,n);
}

#undef SWAP

