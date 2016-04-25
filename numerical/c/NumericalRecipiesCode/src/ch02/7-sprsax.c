void sprsax(float sa[], unsigned long ija[], float x[], float b[], unsigned long n)
{
/********************************
Multiply a matrix in row-index sparse storage arrays 
sa and ija by a vector x[1..n], giving a vector b[1..n]
********************************/
	void nrerror(char error_text[]);
	unsigned long i, k;

	if (ija[1] != n+2) nrerror("sprsax: mismatched vector and matrix");
	for (i=1;i<=n;i++)
	{
		b[i]=sa[i]*x[i]; //Diagonal entries
		for (k=ija[i]; k <= ija[i+1]-1; k++)
			b[i] += sa[k]*x[ija[k]]; //Off diagonal entries. Multiply the entry of the matrix by the x of the corresponding column
	}
}
