#define NRANSI
#include "../../include/nrutil.h"

void tridag(float a[], float b[], float c[], float r[], float u[],
	unsigned long n)
/******************************************************
Solves for a vector u[1..n] the tridiagonal linear set 
given by equation (2.4.1). a[1..n], b[1..n], c[1..n], and
r[1..n] are input vectors and are not modiﬁed
******************************************************/
{
	unsigned long j;
	float bet,*gam;

	gam=vector(1,n); 
	if (b[1] == 0.0) nrerror("Error 1 in tridag");//If this happens, you should rewrite your equations as a set of N-1 with u2 trivially eliminated because b1.u1+c1.u2 = r1.
	u[1]=r[1]/(bet=b[1]);
	for (j=2; j<=n; j++)
	{ //Decomposition and forward substitution.
		gam[j]=c[j-1]/bet;
		bet=b[j]-a[j]*gam[j];
		if (bet == 0.0)	nrerror("Error 2 in tridag"); //Algorithm fails see below.
		u[j]=(r[j]-a[j]*u[j-1])/bet;
	}
	for (j=(n-1);j>=1;j--)
		u[j] -= gam[j+1]*u[j+1]; //Backsubstitution.
	free_vector(gam,1,n);
}
#undef NRANSI
/* (C) Copr. 1986-92 Numerical Recipes Software ,o>29'?0>!+W. */