#include <math.h>
#define NRANSI
#include "../include/nrutil.h"

void qrupdt(float **r, float **qt, int n, float u[], float v[])
{
	void rotate(float **r, float **qt, int n, int i, float a, float b);
	int i,j,k;

	for (k=n;k>=1;k--) {
		if (u[k]) break;
	}
	if (k < 1) k=1;
	for (i=k-1;i>=1;i--) {
		rotate(r,qt,n,i,u[i],-u[i+1]);
		if (u[i] == 0.0) u[i]=fabs(u[i+1]);
		else if (fabs(u[i]) > fabs(u[i+1]))
			u[i]=fabs(u[i])*sqrt(1.0+SQR(u[i+1]/u[i]));
		else u[i]=fabs(u[i+1])*sqrt(1.0+SQR(u[i]/u[i+1]));
	}
	for (j=1;j<=n;j++) r[1][j] += u[1]*v[j];
	for (i=1;i<k;i++)
		rotate(r,qt,n,i,r[i][i],-r[i+1][i]);
}


void rotate(float **r, float **qt, int n, int i, float a, float b) 
//Given matrices r[1..n][1..n] and qt[1..n][1..n], carry out a Jacobi rotation on rows i and i +1of each matrix. a and b are the parameters of the rotation: cos θ = a/√a2 + b2, sinθ = b/√a2 + b2. 
{ 
	int j; 
	float c,fact,s,w,y;
	if (a == 0.0) 
	{ //Avoid unnecessary overﬂow or underﬂow. 
		c=0.0; s=(b >= 0.0 ? 1.0 : -1.0); 
	} else if (fabs(a) > fabs(b)) 
	{ 
		fact=b/a; 
		c=SIGN(1.0/sqrt(1.0+(fact*fact)),a); s=fact*c; 
	} else 
	{ 
		fact=a/b; 
		s=SIGN(1.0/sqrt(1.0+(fact*fact)),b); 
		c=fact*s; 
	} 
	for (j=i;j<=n;j++) 
	{ //Premultiply r by Jacobi rotation. 
		y=r[i][j];
		w=r[i+1][j];
		r[i][j]=c*y-s*w;
		r[i+1][j]=s*y+c*w;
	}
	for (j=1;j<=n;j++)
	{ //Premultiply qt by Jacobi rotation.
		y=qt[i][j];
		w=qt[i+1][j];
		qt[i][j]=c*y-s*w;
		qt[i+1][j]=s*y+c*w;
	}
}

#undef NRANSI