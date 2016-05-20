void chint(
	float a,
	float b,
	float c[],//output chebyshev polynomials from routine
	float cint[],
	int n
	)
	/************************
	*Given a, b, c[0..n-1], as output from the routine chebft (section 5.8)
	*and given n, the desired degree of approximation (length of c to be used)
	*this routine returns the array cint[0..n-1]. the Chebyshev coefficients  of
	*the integral of the function whose coefficients are c. The constant of integration 
	*is set so that the integral vanishes at a.
	***************************/
{
	int j;
	float sum=0.0, fac=1.0, con;

	con = 0.25 * (b-a);//Factor that normalizes the interval (b-a)
	for (j=1; j<=n-2; j++)
	{
		cint[j] = con * (c[j-1]-c[j+1])/j;//Equation 5.9.1
		sum += fac * cint[j];//Accumulates the constant of integration.
		fac = -fac;//Will equal +/-1
	}
	//Dont understand this one.
	cint[n-1] = con * c[n-2]/(n-1);//Special case of 5.9.1 for n-1. This is from ignoring c[n] term since its zero.
	sum += fac * cint[n-1];
	cint[0] = 2.0 * sum;//Set constant of integration. Chosen so that the integral vanishes at a.	
}