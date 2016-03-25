void sprstx(float sa[], unsigned long ija[], float x[], float b[], unsigned long n)
{
/************************
Multiply the transpose of a matrix in row-indexed sparse storage arrays sa and ija by a vector x[1..n], giving a vector b[1..n].
************************/
	void nrerror(char error_text[]);
	unsigned long i,j,k;

	if (ija[1] != n+2) nrerror("mismatched vector and matrix in sprstx");
	for (i=1;i<=n;i++)
		b[i]=sa[i]*x[i]; //First come the diagonal terms

	for (i=1;i<=n;i++)
	{//Now loop over the off diagonal terms.
		for (k=ija[i]; k <= ija[i+1]-1; k++)
		{
			j = ija[k];
			b[j] += sa[k]*x[i]; //Because this is multiplication by the transpose, the indices of b and x interchange.
		}
	}
}