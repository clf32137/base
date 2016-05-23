#include <math.h>
#define NRANSI
#include "../../include/nrutil.h"
#define PI 3.141592653589793

void chebft(
	float a, //Lower limit for evaluating the function
	float b, //Upper limit for evaluating the function
	float c[], //OUTPUT: Coefficients computed by the routine
	int n, //Maximum degree polynomial we want to use to approximate function
	float (*func)(float) //The function to be approximated
	)
/*
*Chebyshev fit: Given a function func, lower and upper limits of the interval
*[a,b], and maximum degree n, this routine computes n coefficients c[0..n-1]
*such that $func(x) = [\sum_{k=0}^{n-1} c_k T_k(y)] - c_0/2$, where y and x are
*related by (5.8.10). This routine is to be used with moderately large n (30 or 50),
*the array of c's subsequently to be truncated at the smaller value of m such that
*c_m and subsequent elements are negligible.
*/
{
	int k,j;
	float fac, bpa, bma, *f;

	f = vector(0, n-1);
	bma = 0.5 * (b-a);
	bpa = 0.5 * (b+a);
	for (k=0; k < n; k++)
	{ //We evaluate the function at n points requred by 5.8.7
		float y = cos(PI * (k + 0.5) / n);
		f[k] = (*func)(y * bma + bpa); //y lies between 0 and 1 while x lies between a and b.
	}
	fac = 2.0 / n;
	for (j=0; j < n; j++)
	{
		double sum = 0.0;//We will accumulate the sum in double precision.
		for (k=0; k < n; k++)
			sum += f[k] * cos(PI * j * (k + 0.5)/n);
		c[j] = fac * sum;
	}
	free_vector(f, 0, n-1);
}



#undef PI
#undef NRANSI