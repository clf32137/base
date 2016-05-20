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
	//return x*x*x*x + x*x*(x-2*x*x) + 2*x*x + 34*x;
	return exp(x);
}

int main(int argc, char *argv[])
{
	//Used to determine which section gets its results printed.
	int shouldiprint[] = 
	{
		1, // polynomial evaluation
		1, // divide polynomials
		1, // differentiate function
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
	int printindx = 0, n;
	float h, err, x, ans;

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
		float a = 2.0, b = 7.0; //Upper and lower bounds over which the function will be evaluated.
			x = 3.0;//The value at which the function will be evaluated.
		n = 8;//One more than degree of polynomial for approximation.
	//</Settings to play with>

		//Let the evaluations begin!!
	//<Evaluate Chebyshev coefficients>
		float *c1; c1 = vector(0, n);//Chebyshev coefficients of function.
		float *c1der; c1der = vector(0, n);//Chebyshev coefficients of derivatives.
		//pprint1d_float(c1,n1); //Will give garbage values since array not initialized.
		chebft(a, b, c1, n, testFn2); //The function to be approximated
		printf("Chebyshev coefficients: \n");
		pprint1d_float(c1, n);
	//</Evaluate Chebyshev coefficients>
		
	//<Evaluate function using Chebyshev>
		float chebyshev_val = chebev_debug(a, b, c1, x, n);
		float orig_val = testFn2(x);
		printf("Original function: %.2f Chebyshev approximation: %.2f\n", orig_val, chebyshev_val);
		//How close did we get?
		float prct_diff = (chebyshev_val - orig_val) / orig_val;
		printf("Fractional diff = %.2f\n", prct_diff);
	//</Evaluate function using Chebyshev>

	//<Evaluate derivatives using Chebyshev>
		printf("\n#Now for derivatives#\n");
		//First find the derivative using above method.
		ans = dfridr(testFn2, x, h, &err);
		printf("True derivative: %.2f\n",ans);
		//Now Chebyshev coefficients of the derivative.
		chder(a, b, c1, c1der, n);
		chebyshev_val = chebev(a, b, c1der, x, n);
		printf("Chebyshev derivative:%.2f\n",chebyshev_val);
	//</Evaluate derivatives using Chebyshev>
	}

	//Freeze the console so I can look at the output.
	char str1[20];
	scanf("%s", str1);
}

