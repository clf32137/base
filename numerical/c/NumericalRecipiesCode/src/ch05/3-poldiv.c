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
		r[j] = u[j];
		q[j] = 0.0;
	}
	for (k = n - nv; k >= 0; k--)
	{
		q[k] = r[nv + k] / v[nv];
		for (j = nv + k - 1; j >= k; j--)
			r[j] -= q[k] * v[j - k];
	}
	for (j = nv; j <= n; j++) 
		r[j] = 0.0;
}