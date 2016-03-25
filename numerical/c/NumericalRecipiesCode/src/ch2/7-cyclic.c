#define NRANSI
#include "../../include/nrutil.h"

void cyclic(float a[], float b[], float c[], float alpha, float beta,
	float r[], float x[], unsigned long n)
/*************************************
Solves for a vector x[1..n] the "cyclic” set of linear equations given by equation (2.7.9). 
a, b, c, and r are input vectors, all dimensioned as [1..n], 
while alpha and beta are the corner entries in the matrix. The input is not modiﬁed.
*************************************/
{
	void tridag(float a[], float b[], float c[], float r[], float u[],
		unsigned long n);
	
	unsigned long i;
	
	float fact, gamma, *bb, *u, *z;

	if (n <= 2) nrerror("n too small in cyclic");

	bb = vector(1,n);
	u = vector(1,n);
	z = vector(1,n);
	gamma = -b[1];
	bb[1] = b[1]-gamma;
	bb[n] = b[n] - alpha * beta / gamma;
	for (i=2;i<n;i++) 
		bb[i]=b[i];
	
	tridag(a,bb,c,r,x,n); //y = A^-1.b, Stored in x.
	
	u[1]=gamma;
	u[n]=alpha;
	for (i=2;i<n;i++)
		u[i]=0.0;
	
	tridag(a,bb,c,u,z,n); //z = A^-1.u
	
	fact = (x[1] + beta * x[n] / gamma) / (1.0 + z[1] + beta * z[n] / gamma); //Form v.x/(1+v.z). Only first and last terms matter in the two dot products.
	
	for (i=1;i<=n;i++)
		x[i] -= fact*z[i];
	
	free_vector(z,1,n);
	free_vector(u,1,n);
	free_vector(bb,1,n);
}
#undef NRANSI