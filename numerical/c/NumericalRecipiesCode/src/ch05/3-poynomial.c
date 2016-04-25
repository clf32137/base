#include <math.h>

//Special case of fourth degree polynomials. Won't need to use it since we have nth degree code.
float eval4thDeg(
	float *c, 
	float x
	)
{
	//         A M     A M     A M     A M => 4 multiplications and 4 additions.
	return c[0]+x*(c[1]+x*(c[2]+x*(c[3]+x*c[4])));
}

//Generalization of 4th degree code above. Also calculates the first derivative.
float evalnthDeg(
	float *c,//Coefficients of polynomial
	float x,//Evaluate polynomial at
	int n//Number of terms in the polynomial
	)
{
	int j;
	float p = c[j=n], dp = 0.0;
	while(j>0)
	{
		dp = dp * x + p; //Derivative
		p = p * x + c[--j]; //Polynomial
	}
}


