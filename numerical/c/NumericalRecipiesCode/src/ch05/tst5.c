#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include "../../include/nrutil.h"
#include "../../include/fileio.h"
#include "../../include/general_fns.h"
#include "ch5funcs.h"


float testFn(float x)
{
	return x*x*x;
	//return 1;
}

float testFn2(float x)
{
	//return x*x*x*x;
	return x*x*x;
}

int main(int argc, char *argv[])
{
	//Used to determine which section gets its results printed.
	int shouldiprint[] = 
	{
		0, // polynomial evaluation
		0, // divide polynomials
		0, // differentiate function
		1, // chebyshev
		1, //
		1, //
		1, //
		1, //
		1, //
		1, //
		1, //
		1  //
	};
	int printindx = 0;
	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Evaluate polynomial and calculate its derivatives\n###################\n");
		float c[] = {1,1,1,1,0};
		int nc = 3;
		float x = 2.0;
		float pd[] = {0,0,0,0,0};
		int nd = 4;
		ddpoly_debug(c,nc,x,pd,nd);
		int i;
		for(i=0; i < nd; i++)
			printf("%f%s", pd[i], i < nd - 1 ? "\t" : "\n");
	}
	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Divide two polynomials\n###################\n");
		float u[] = {-7,0,5,6};
		int n = 3;
		float v[] = {-1,-2,3};
		int nv = 2;
		float q[] = {0,0,0,0};
		float r[] = {0,0,0,0};
		poldiv_debug(u,n,v,nv,q,r);
		printf("Quotient: "); pprint1d_float(q, n);
		printf("Remaindr: ");pprint1d_float(r, n);
	}
	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Differentiation of a function\n###################\n");
		float x = 6;
		float h = 2;
		float err = 0;

		float ans = dfridr(testFn, x, h, &err);
		printf("Derivative is: %f and error is: %f\n", ans, err);
		float ans2 = simplenumerical(testFn, x, 2e-2);
		printf("Derivative with standard method is: %f\n", ans2);
	}
	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Chebyshev polynomials\n###################\n");
		float a = 2.0, b = 7.0, x1 = 6.0;
		int n1 = 5;//Degree of polynomial for approximation
		float *c1; c1 = vector(0, n1);
		//pprint1d_float(c1,n1); //Will give garbage values since array not initialized.
		chebft(a, b, c1, n1, testFn2); //The function to be approximated
		printf("Chebyshev coefficients: \n");
		pprint1d_float(c1, n1);
		float chebyshev_val = chebev_debug(a, b, c1, 3, x1);
		float orig_val = testFn2(x1);
		printf("Original function: %.2f Chebyshev approximation: %.2f\n", orig_val, chebyshev_val);
		float prct_diff = (chebyshev_val - orig_val)/orig_val;
		printf("Fractional diff = %.2f\n", prct_diff);
	}
}

