void chder(
	float a,//Lower bound of range in which function was evaluated.
	float b,//Upper bound of range in which function was evaluated.
	float c[],//Chebyshev coefficients previous routine.
	float cder[],//OUTPUT: Will contain the derivative Chebyshev coefficients.
	int n//Degree of approximation.
)
{
	int j;
	float con;

	cder[n-1] = 0.0;//n-1 and n-2 are special cases.
	cder[n-2] = 2*(n-1)*c[n-1];//Substitute into 5.9.2 with cder[n+1] = 0.
	
	for (j=n-3;j>=0;j--) //From the formula, the earliest derivative we can calculate is (n-2). So the loop begins from (n-3).
		cder[j] = cder[j+2] + 2*(j+1)*c[j+1];//Equation 5.9.2
	con=2.0/(b-a);
	for (j=0;j<n;j++)//Normalize to the interval (b-a).
		cder[j] *= con;
}

