#include <math.h>
#define NRANSI
#include "../../include/nrutil.h"

void qrsolv(float **a, int n, float c[], float d[], float b[]) 
//Solves the set of n linear equations A·x = b. a[1..n][1..n], c[1..n], and d[1..n] are input 
//as the output of the routine qrdcmp and are not modiﬁed. b[1..n] is input as the right-hand side vector, 
//and is overwritten with the solution vector on output. 
{ 
	void rsolv(float **a, int n, float d[], float b[]); 
	int i,j; 
	float sum,tau;

	for(j=1;j<n;j++){
		for(sum=0.0,i=j;i<=n;i++)
			sum+=a[i][j]*b[i];
		tau = sum/c[j];
		for(i=j;i<=n;i++)
			b[i]-=tau*a[i][j];
	}
	rsolv(a,n,d,b);
}


void rsolv(float **a, int n, float d[], float b[])
{
	int i,j;
	float sum;
	b[n] /= d[n];
	for(i=n-1;i>=1;i--){
		for(sum=0.0,j=i+1;j<=n;j++)
			sum+=a[i][j]*b[j];
		b[i] = (b[i]-sum)/d[i];
	}
}
