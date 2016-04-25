//extern unsigned long ija[];
//extern double dsa[];

void asolve(unsigned long ija[], double dsa[], unsigned long n, double b[], double x[], int itrnsp)
{
	unsigned long i;

	for(i=1;i<=n;i++)
		x[i]=(dsa[i] != 0.0 ? b[i]/dsa[i] : b[i]); //The matrix A is the diagonal part of A, 
												 //stored in the first n elements of sa. Since the transpose matrix has the same diagonal, the flag itrnsp is not used.
}