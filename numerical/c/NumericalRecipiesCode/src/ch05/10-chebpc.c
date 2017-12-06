//The routines in section 10 involve the problem of obtaining direct polynomial coefficients (of 1,x,x^2 and so on instead of the Chebyshev polynomials). 
//The authors recomment using them only when m < 8. This is a deal breaker for me and so, not much effort was spent in understanding them.

#define NRANSI
#include "../../include/nrutil.h"

void chebpc(
	float c[],
	float d[],
	int n
	)
	/*
	*Given a coefficient array of Chebyshev polynomial coefficients, c[0..n-1], this routine generates a coefficient array 
	*d[0..n-1] such that \sum_{k=1}^{n-1}d_ky^k = \sum_{k=0}^{n-1}c_k.T_k(y)-c_0/2. The method is Clenshaws recurrencr (5.8.11), but 
	*now applied algebrically rather than arithemetically.
	*/
{
	int k,j;
	float sv,*dd;

	dd = vector(0,n-1);
	for (j=0; j<n; j++) d[j] = dd[j] = 0.0;
	d[0] = c[n-1];
	for (j=n-2; j>=1; j--)
	{
		for (k=n-j; k>=1; k--)
		{
			sv = d[k];
			d[k] = 2.0*d[k-1] - dd[k];
			dd[k] = sv;
		}
		sv = d[0];
		d[0] = -dd[0] + c[j];
		dd[0] = sv;
	}
	for (j=n-1; j>=1; j--)
		d[j] = d[j-1]-dd[j];

	d[0] = -dd[0] + 0.5*c[0];
	free_vector(dd,0,n-1);
}
#undef NRANSI

