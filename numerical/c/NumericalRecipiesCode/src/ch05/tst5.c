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
}

float testFn2(float x)
{
	return exp(x);
}

//Needs to be manually set to the indefinite integral of testFn2
float testFn2Integrl(float x)
{
	return exp(x);
}

int main(int argc, char *argv[])
{
	//Used to determine which section gets executed.
	int shouldiprint[] = 
	{
		1, // polynomial evaluation
		1, // divide polynomials
		1, // differentiate function
		1, // chebyshev
		1, // chebyshev derivatives - will only make sense if chebyshev code has been executed
		1, // chebyshev integrals - will only make sense if chebyshev code (previous to previous) has been executed
		1, //
		1, //
		1, //
		1, //
		1, //
		1  //
	};
	int printindx = 0, n=0;
	float a, b, h, err, x, ans, chebyshevVal = 0;
	float *chebyshev = vector(0,n);

	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Evaluate polynomial and calculate its derivatives\n###################\n");
	//<Settings to play with>	
		float c[] = {1,1,1,1,0};
		int nc = 3;
		x = 2.0; 
		n = 4;
	//</Settings to play with>

		float pd[] = {0,0,0,0,0};
		
		ddpoly_debug(c,nc,x,pd,n);
		int i;
		for(i=0; i < n; i++)
			printf("%f%s", pd[i], i < n - 1 ? "\t" : "\n");
	}
	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Divide two polynomials\n###################\n");
	//<Settings to play with>
		float u[] = {-7,0,5,6};
		n = 3;
		float v[] = {-1,-2,3};
		int nv = 2;
	//</Settings to play with>

		float q[] = {0,0,0,0};
		float r[] = {0,0,0,0};
		poldiv_debug(u,n,v,nv,q,r);
		printf("Quotient: "); pprint1d_float(q, n);
		printf("Remaindr: ");pprint1d_float(r, n);
	}
	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Differentiation of a function\n###################\n");
	//<Settings to play with>	
		h = 2, err = 0, x = 6;
	//</Settings to play with>	
		
		ans = dfridr(testFn, x, h, &err);
		printf("Derivative is: %f and error is: %f\n", ans, err);
		float ans2 = simplenumerical(testFn, x, 2e-2);
		printf("Derivative with standard method is: %f\n", ans2);
	}
	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Chebyshev polynomials\n###################\n");
	//<Settings to play with>
		a = 2.0, b = 7.0; //Upper and lower bounds over which the function will be evaluated.
			x = 3.0;//The value at which the function will be evaluated.
		n = 8;//One more than degree of polynomial for approximation.
	//</Settings to play with>

	//<Evaluate Chebyshev coefficients>
		chebyshev = vector(0, n);//Chebyshev coefficients of function.
		chebft(a, b, chebyshev, n, testFn2); //The function to be approximated
		printf("Chebyshev coefficients: \n");
		pprint1d_float(chebyshev, n);
	//</Evaluate Chebyshev coefficients>
		
		float orig_val = testFn2(x);
	//<Evaluate function using Chebyshev>
		chebyshevVal = chebev_debug(a, b, chebyshev, x, n);		
		printf("Original function: %.2f Chebyshev approximation: %.2f\n", orig_val, chebyshevVal);
		//How close did we get?
		float prct_diff = (chebyshevVal - orig_val) / orig_val;
		printf("Fractional diff = %.2f\n", prct_diff);
	//</Evaluate function using Chebyshev>
	}
	if (shouldiprint[printindx++])//Will only make sense if previous, chebyshev coefficients code has been executed.
	{
		printf("\n###################\n Derivatives using Chebyshev polynomials\n###################\n");
		float *c1der; c1der = vector(0, n);//Chebyshev coefficients of derivatives.
		//First find the derivative using the method described earlier.
		ans = dfridr(testFn2, x, h, &err);
		printf("True derivative: %.2f\n", ans);
		//Now Chebyshev coefficients of the derivative.
		chder(a, b, chebyshev, c1der, n);
		chebyshevVal = chebev(a, b, c1der, x, n);
		printf("Chebyshev derivative:%.2f\n", chebyshevVal);	
	}
	if (shouldiprint[printindx++])//Will only make sense if previous to previous, chebyshev coefficients code has been executed.
	{
		printf("\n###################\n Integration using Chebyshev polynomials\n###################\n");
		ans = testFn2Integrl(x) - testFn2Integrl(a); //Chebyshev is set such that integral is evaluated to 0 at a.
		printf("True integral value: %.2f\n", ans);
		//Now integrate the Chebyshev polynomial.
		float *c1intgrl; c1intgrl = vector(0, n);
		chint(a, b, chebyshev, c1intgrl, n);
		chebyshevVal = chebev(a, b, c1intgrl, x, n);
		printf("Chebyshev integral:%.2f\n", chebyshevVal);
	}


	//Freeze the console so I can look at the output.
	char str1[20];
	scanf("%s", str1);
}

