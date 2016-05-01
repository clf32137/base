#include <stdio.h>

void ddpoly(
	float c[], //Coefficients of polynomial
	int nc, //Degree of polynomial. So, c will have nc+1 terms counting constant.
	float x, //Point at which evaluation required
	float pd[], //OUTPUT - Derivatives of polynomial
	int nd //Number of derivatives to be calculated.
	)

/*
*Given the nc+1 coefficients of a polynomial of degree nc as an array
*c[0..nc] with c[0] being the constant term, and given the value of x,
*and given nd>1, this routine returns the polynomial evaluated x as pd[0]
*and nd derivatives as pd[1..nd]
*/
{
	int nnd, j, i;
	float cnst = 1.0;

	pd[0] = c[nc];

	for (j=1; j <= nd; j++)//Derivatives to be calculated.
		pd[j]=0.0;

	for (i = nc-1; i >= 0; i--)
	{
		nnd = (nd < (nc-i) ? nd : nc-i); //MIN(nd,nc-i): Since we are required to find nd derivatives, we won't go further.
										 //But if someone asks us to calculate more derivatives than is possible,
										 //we will go as far as we can.
		for (j=nnd; j>=1; j--)
			pd[j] = pd[j]*x + pd[j-1]; //Similar to dynamic programming style in Vandermonde.
									   //d/dx (x.g(x)) = x.g'(x) + g(x).1
									   //See 4/27/16 notes and also output of debugging version below.

		pd[0] = pd[0]*x + c[i]; //See eval4thDeg in 3-polynomial.c to understand why.
	}
	for (i=2; i <= nd; i++) //After the first derivative, factorial constants come in.
	{
		cnst *= i;
		pd[i] *= cnst;
	}
}


#include "../../include/general_fns.h"

void ddpoly_debug(
	float c[], //Coefficients of polynomial
	int nc, //Degree of polynomial. So, c will have nc+1 terms counting constant.
	float x, //Point at which evaluation required
	float pd[], //OUTPUT - Derivatives of polynomial
	int nd //Number of derivatives to be calculated.
	)
{
	printf(ANSI_COLOR_GREEN"\n############# Debugging ddpoly function ###############\n"ANSI_COLOR_RESET);
	int debug = 1;
	int nnd, j, i, k;
	float cnst = 1.0;
	
	pd[0] = c[nc];//Degree of polynomial

	for (j=1; j <= nd; j++)//Derivatives to be calculated.
		pd[j]=0.0;

	for (i = nc-1; i >= 0; i--)
	{
		nnd = (nd < (nc-i) ? nd : nc-i);
		printf(ANSI_COLOR_RED "i = %d", i);
		printf(" pd[0] = %.2f\n",pd[0]);
		printf(ANSI_COLOR_RESET);
		for (j = nnd; j>=1; j--)
		{
			printf("\tpd[%d]",j);
			printf(ANSI_COLOR_YELLOW " (%.2f) ",pd[j]);
			printf(ANSI_COLOR_RESET " = pd[%d] * x",j);
			printf(ANSI_COLOR_YELLOW " (%.2f) ",x);
			printf(ANSI_COLOR_RESET " + pd[%d]",j-1);
			printf(ANSI_COLOR_YELLOW " (%.2f) ", pd[j-1]);
			printf(ANSI_COLOR_RESET);

			pd[j] = pd[j]*x + pd[j-1];

			printf(ANSI_COLOR_YELLOW" = (%.2f)\n",pd[j]);
			printf(ANSI_COLOR_RESET);
		}
		pd[0] = pd[0]*x + c[i]; //See eval4thDeg in 3-polynomial.c to understand why.
	}
	for (i=2; i <= nd; i++) //After the first derivative, factorial constants come in.
	{
		cnst *= i;
		pd[i] *= cnst;
	}
	printf("\n");
}


/* (C) Copr. 1986-92 Numerical Recipes Software ?421.1-9. */