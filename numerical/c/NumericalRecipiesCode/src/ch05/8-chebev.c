#include <stdio.h>
#include "../../include/general_fns.h"

float chebev(
	  float a, //Lower limit of range in which function is to be evaluated (must match output from chebft)
	  float b, //Upper limit of range.
	  float c[], //Coefficients gathered from Chebyshev
	  float x, //Value at which the function is to be evaluated.
	  int m //The maximum degree within c we are considering.
	     )
/*
*Chebyshev evaluation: All arguments are input. c[0..m-1] is an array of Chebyshev coefficients,
*the first m elements of c output from chebft (which must have been called with the same a and b).
*The Chebyshev polynomial $\sum_{k=0}^{m-1}c_kT_k(y)-c_0/2$ is evaluated at a point $y = \frac{x-(b+a)/2}{(b-a)/2}$,
*and the result is returned as the function value.
*/
{
	float d = 0.0, dd = 0.0, temp_d, y, y2; //Remember, x is between a and b while y is between 0 and 1.
											//y2 is literally 2 times y.
	int j;
	
	if ((x-a)*(x-b) > 0.0) //x is on the same side of a and b.
		nrerror("x not in range in routine CHEBEV");
	
	y2 = 2.0 * ( 
			y = (2.0*x - a - b) / (b-a)  //First, convert x into y.
		); //y2 is literally 2 times y.

	for (j = m-1; j >= 1; j--)
	{	//Clenshaws recurrence.
		temp_d = d;
		d = y2*d - dd + c[j]; //Initially, dd and d are both zero.
		dd = temp_d; //dd of next iteration is d of this iteration since the difference between their indices is 1.
	} //When we exit the loop, d is $d_1$ and dd is $d_2$.
	return y*d - dd + 0.5 * c[0]; //x.d_1 - d_2 + \frac{c_0}{2}
}


float chebev_debug(
	  float a, //Lower limit of range in which function is to be evaluated (must match output from chebft)
	  float b, //Upper limit of range.
	  float c[], //Coefficients gathered from Chebyshev
	  float x, //Value at which the function is to be evaluated.
	  int m //The maximum degree within c we are considering.
	     )
/*
*Chebyshev evaluation: All arguments are input. c[0..m-1] is an array of Chebyshev coefficients,
*the first m elements of c output from chebft (which must have been called with the same a and b).
*The Chebyshev polynomial $\sum_{k=0}^{m-1}c_kT_k(y)-c_0/2$ is evaluated at a point $y = \frac{x-(b+a)/2}{(b-a)/2}$,
*and the result is returned as the function value.
*/
{
	printf(ANSI_COLOR_LIGHTMAGENTA"\tInputs to chebev were: a = %.2f, b = %.2f, c[0] = %.2f, c[1] = %.2f, m = %d, x = %.2f\n",a, b, c[0], c[1], m, x);
	float d = 0.0, dd = 0.0, temp_d, y, y2; //Remember, x is between a and b while y is between 0 and 1.
											//y2 is literally 2 times y.
	int j;
	
	if ((x-a)*(x-b) > 0.0)
	{ //x is on the same side of a and b.
		printf(ANSI_COLOR_RESET);
		nrerror("x not in range in routine CHEBEV");
	}
	
	y2 = 2.0 * ( 
			y = (2.0*x - a - b) / (b-a)  //First, convert x into y.
		); //y2 is literally 2 times y.

	printf("\ty2 = %.2f\n", y2);
	printf(ANSI_COLOR_RESET);
	for (j = m-1; j >= 1; j--)
	{	//Clenshaws recurrence.
		temp_d = d;
		d = y2*d - dd + c[j]; //Initially, dd and d are both zero.
		dd = temp_d; //dd of next iteration is d of this iteration since the difference between their indices is 1.
	} //When we exit the loop, d is $d_1$ and dd is $d_2$.
	return y*d - dd + 0.5 * c[0]; //x.d_1 - d_2 + \frac{c_0}{2}
}