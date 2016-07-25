void lubksb(float **a, int n, int *indx, float b[])
/*************************************
Solves the set of n linear equations A·X = B. Here a[1..n][1..n] is input, 
not as the matrix A but rather as its LU decomposition, determined by the routine ludcmp. 
indx[1..n] is input as the permutation vector returned by ludcmp. b[1..n] is input as the right-hand side vector B, 
and returns with the solution vector X. a, n, and indx are not modiﬁed by this routine and can be left in place for successive calls with different 
right-hand sides b. This routine takes into account the possibility that b will begin with many zero elements, so it is effcient for use in matrix inversion.
*************************************/
{
	int i, ii=0, ip, j;
	float sum;

	//We now do forward substitution as per 2.3.6
	//the only new wrinkle is to unscramble the permutation as we go.
	//Note that \alpha[i][i] = 1 so no division required in this forward loop.
	for (i=1;i<=n;i++)
	{
		ip = indx[i];
		sum = b[ip];  //Get the true first b and append to sum.
		b[ip] = b[i]; //First part of exchange. Also note that ip >= i.
		if (ii) // This will ensure that the first equation does not involve the sum and the next ones do as per 2.3.6.
			for (j=ii;j<=i-1;j++) //ii is the first time we ever saw a non zero b element (taking permutation into account)
				sum -= a[i][j]*b[j]; //By now, b[j] contains the previous y (L.y=b as per 2.3.4). 
		else if (sum) //A non zero element was encountered. so from now on we will have to do the sums in the loop above.
			ii = i; //When ii is set to a positive value, it will become the index of the first nonvanishing element of b.
		b[i] = sum; //exchange between b[i] and b[ip] complete.
	}

	//Now do backsubstitution as per 2.3.7. Permutation has already been accounted for.
	for (i=n;i>=1;i--)
	{
		sum = b[i];
		for (j=i+1;j<=n;j++)
			sum -= a[i][j]*b[j];
		b[i] = sum/a[i][i];//store a component of the solution vector X. The division is by \beta[i][i].
	}
}