#include <stdio.h>
#include "ch5funcs.h"
#include "../../include/general_fns.h"

void poldiv(
	float u[], //Numerator polynomial
	int n, //The degree of the numerator
	float v[], //Denominator polynomial
	int nv, //Degree of denominator
	float q[], //OUTPUT Quotiend polynomial
	float r[]  //OUTPUT Remainder polynomial
	)
/*
*Given the n+1 coefficients of a polynomial of degree n in u[0..n], and
*the nv+1 coefficients of another polynomial of degree nv in v[0..nv],
*divide polynomial u by polynomial v, giving a quotient whose coefficients
*are returned in q[0..n] and remainder in r[0..n]. The elements r[nv..n]
*and q[n-nv+1..n] are returned as 0.
*/
{
	int k, j;

	for (j = 0; j <= n; j++)
	{
		r[j] = u[j];//Remainder equals numerator
		q[j] = 0.0;
	}
	for (k = n - nv; k >= 0; k--)
	{
		q[k] = r[nv + k] / v[nv];
		for (j = nv + k - 1; j >= k; j--)
		{
			r[j] -= q[k] * v[j - k];			
		}
	}
	for (j = nv; j <= n; j++)
		r[j] = 0.0;
}


void poldiv_debug(
	float u[], //Numerator polynomial
	int n, //The degree of the numerator
	float v[], //Denominator polynomial
	int nv, //Degree of denominator
	float q[], //OUTPUT Quotiend polynomial
	float r[]  //OUTPUT Remainder polynomial
	)
{
	printf("See non monic divisors example here: https://en.wikipedia.org/wiki/Synthetic_division");
	printf(ANSI_COLOR_GREEN"\n############# Debugging poldiv function ###############\n"ANSI_COLOR_RESET);
	int k, j, i=0;
	printf("u = ");
	pprint1d_float(u,n+1);
	printf("v = ");
	pprint1d_float(v,nv+1);
	for (j = 0; j <= n; j++)
	{
		r[j] = u[j];
		q[j] = 0.0;
	}
	for (k = n - nv; k >= 0; k--)
	{		
		printf("k = %d; q[%d]" , k, k);
		printf(ANSI_COLOR_YELLOW" (%.2f)",q[k]);
		printf(ANSI_COLOR_RESET" = r[%d] ", n-i);
		printf(ANSI_COLOR_YELLOW" (%.2f)",r[n-i]);
		printf(ANSI_COLOR_RESET"/ v[%d]", nv);
		printf(ANSI_COLOR_YELLOW" (%.2f)",v[nv]);
		q[k] = r[n - i] / v[nv]; i++;
		printf(" = (%.2f)", q[k]);
		printf(ANSI_COLOR_RESET"\n");

		for (j = k; j <= nv+k-1; j++)
		{
			printf("\tj = %d;", j);
			printf(ANSI_COLOR_RESET"\tr[%d] ",j);
			printf(ANSI_COLOR_YELLOW"(%.2f)", r[j]);
			printf(ANSI_COLOR_RESET" = r[%d] - q[%d]", j, k);
			printf(ANSI_COLOR_YELLOW" (%.2f)", q[k]);
			printf(ANSI_COLOR_RESET" * v[%d]", j-k);
			printf(ANSI_COLOR_YELLOW" (%.2f) = ", v[j-k]);

			r[j] -= q[k] * v[j - k];
			printf("%.2f",r[j]);
			printf(ANSI_COLOR_RESET"\n");
		}
	}
	for (j = nv; j <= n; j++)
		r[j] = 0.0;
}
