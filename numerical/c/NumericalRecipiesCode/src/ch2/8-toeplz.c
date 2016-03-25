#define NRANSI
#include "nrutil.h"
#define FREERETURN {free_vector(h,1,n);free_vector(g,1,n);return;}

//Toeplitz matrices tend to occur in deconvolution and signal processing.
void toeplz(float r[], float x[], float y[], int n)
{
	int j,k,m,m1,m2;
	float pp,pt1,pt2,qq,qt1,qt2,sd,sgd,sgn,shn,sxn;
	float *g,*h;

	if (r[n] == 0.0) nrerror("toeplz-1 singular principal minor");
	g = vector(1,n);
	h = vector(1,n);

//<Initialize x, g and h>
	x[1] = y[1]/r[n];
	if (n == 1) FREERETURN
	g[1] = r[n-1]/r[n];
	h[1] = r[n+1]/r[n];
//</Initialize x, g and h>

//<Main loop of the recursion>
	for (m=1; m <= n; m++)
	{
		m1 = m + 1;
	//<Compute numerator and denominator for x_{m+1} 2.8.19>
		sxn = -y[m1];
		sd = -r[n];
		
		for (j=1; j <= m; j++)
		{
			sxn += r[n+m1-j] * x[j];
			sd += r[n+m1-j] * g[m-j+1];
		}

		if (sd == 0.0) nrerror("toeplz-2 singular principal minor");
		
		x[m1] = sxn/sd;
	//</Compute numerator and denominator for x>

	//<Compute x_{j} 2.8.15>
		for (j=1; j <= m; j++)
			x[j] -= x[m1] * g[m-j+1];
	//<Compute x_{j} 2.8.15>

		//Exit dynaic programming now.
		if (m1 == n) FREERETURN
		
	//<Compute numerator and denominator for G and H, Equations 2.8.23 and 2.8.24>
		sgn = -r[n-m1];
		shn = -r[n+m1];
		sgd = -r[n];
		for (j=1;j<=m;j++)
		{
			sgn += r[n+j-m1]*g[j];
			shn += r[n+m1-j]*h[j];
			sgd += r[n+j-m1]*h[m-j+1];
		}
		if (sd == 0.0 || sgd == 0.0) nrerror("toeplz-3 singular principal minor");
		g[m1] = sgn/sgd;
		h[m1] = shn/sd;
	//</Compute numerator and denominator for G and H, Equations 2.8.23 and 2.8.24>

	//<Compute G_j and H_j for j = 1 to m Equation 2.8.25>
		k = m;
		m2 = (m+1) >> 1; //quotient when divided by 2. Comment in for loop explains why.
		pp = g[m1];
		qq = h[m1];

		for (j=1; j <= m2; j++)
		{//We split the two equations in 2.8.25 into 4 equations by replacing j by M+1-j. Double the equations mean half the iterations.
			pt1 = g[j];
			pt2 = g[k];
			qt1 = h[j];
			qt2 = h[k];
			g[j] = pt1 - pp * qt2;
			g[k] = pt2 - pp * qt1;
			h[j] = qt1 - qq * pt2;
			h[k--] = qt2 - qq * pt1;
		}
	//</Compute G_j and H_j for j = 1 to m Equation 2.8.25>
	}
//</Main loop of the recursion>
	nrerror("toeplz - should not arrive here!");
}
#undef FREERETURN
#undef NRANSI
/* (C) Copr. 1986-92 Numerical Recipes Software 'N;,5%. */

