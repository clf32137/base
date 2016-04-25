#include <math.h>

double snrm(unsigned long n, double sx[], int itol)
{
/*****************************
Compute one of two norms for a vector sx[1..n] as signaled by itol. Used by linbcg.
****************************/
	unsigned long i,isamax;
	double ans;

	if (itol <= 3)
	{
		ans = 0.0;
		for (i=1; i<=n; i++) 
			ans += sx[i]*sx[i]; //Vector magnitude norm.
		return sqrt(ans);
	}
	else
	{
		isamax=1;
		for (i=1; i<=n; i++)
		{ //Largest component norm
			if (fabs(sx[i]) > fabs(sx[isamax]))
				isamax=i;
		}
		return fabs(sx[isamax]);
	}
}