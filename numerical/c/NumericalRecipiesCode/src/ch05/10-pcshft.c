//The routines in section 10 involve the problem of obtaining direct polynomial coefficients (of 1,x,x^2 and so on instead of the Chebyshev polynomials). 
//The authors recomment using them only when m < 8. This is a deal breaker for me and so, not much effort was spent in understanding them.

void pcshft(
	float a,
	float b,
	float d[],
	intn
	)
/*
*Polynomial coefficients shift. Given a coefficient array d[0..n-1], this routine generates a
*coefficient array g[0..n-1] such that \sum_{k=0}^{n-1}d_k.y^k = \sum_{k=0}^{n-1}g_k.x^k, where x and y are related
*by (5.8.10), i.e., the interval -1<y<1 is mapped to the interval a<x<b. The array g is returned in d.
*/
{
	int k,j;
	float fac,cnst;

	cnst = 2.0/(b-a);
	fac = cnst;
	for (j=1;j<n;j++) 
	{
		d[j] *= fac;
		fac *= cnst;
	}
	cnst = 0.5*(a+b);
	for (j=0;j<=n-2;j++)
		for (k=n-2;k>=j;k--)
			d[k] -= cnst*d[k+1];
}
