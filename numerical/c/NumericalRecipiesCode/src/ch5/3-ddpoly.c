#include <stdio.h>

//void ddpoly(
//	float c[], //Coefficients of polynomial
//	int nc, //Degree of polynomial. So, c will have nc+1 terms counting constant.
//	float x, //Point at which evaluation required
//	float pd[], //OUTPUT - Derivatives of polynomial
//	int nd //Number of derivatives to be calculated.
//	)

/*
*Given the nc+1 coefficients of a polynomial of degree nc as an array
*c[0..nc] with c[0] being the constant term, and given the value of x,
*and given nd>1, this routine returns the polynomial evaluated x as pd[0]
*and nd derivatives as pd[1..nd]
*/
void ddpoly(float c[], int nc, float x, float pd[], int nd)
{
	int nnd, j, i;
	float cnst = 1.0;
	printf("x inside : %f\n",x);
	printf("nc: %d\n",nc);
	printf("nd: %d\n",nd);

	pd[0] = c[nc];
	
	
	for (j=1; j<=nd; j++)//Derivatives to be calculated.
		pd[j]=0.0;

	for (i = nc-1; i >= 0; i--)
	{
		nnd = (nd < (nc-i) ? nd : nc-i); //MIN(nd,nc-i)
		for (j=nnd; j>=1; j--)
			pd[j] = pd[j]*x + pd[j-1];

		pd[0] = pd[0]*x + c[i];
	}
	for (i=2; i <= nd; i++) //After the first derivative, factorial constants come in.
	{
		cnst *= i;
		pd[i] *= cnst;
	}
}
/* (C) Copr. 1986-92 Numerical Recipes Software ?421.1-9. */