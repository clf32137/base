#include <math.h>

int sprsin(float **a, int n, float thresh, unsigned long nmax, float sa[], unsigned long ija[])
/************************************
Converts a square matrix a[1..n][1..n] into row-indexed sparse storage mode.
Only elements of a with magnitude ≥thresh are retained. Output is in two linear arrays
with dimension nmax (an input parameter): sa[1..] contains array values, indexed by ija[1..].
The number of elements ﬁlled of sa and ija on output are both ija[ija[1]-1]-1
************************************/
{
	void nrerror(char error_text[]);
	int i,j;
	unsigned long k;

	for (j=1;j<=n;j++)
		sa[j] = a[j][j]; //Store the diagonal elements.
	
	ija[1] = n+2; //Index to the first off diagonal element if any.
	k = n+1;
	
	for (i=1;i<=n;i++)
	{
		for (j=1;j<=n;j++)
		{
			if (fabs(a[i][j]) >= thresh && i != j)
			{
				if (++k > nmax) nrerror("sprsin: nmax too small");
				sa[k] = a[i][j]; //Store off diagonal elements.
				ija[k] = j;	   //And their column indices.
			}
		}
		ija[i+1] = k+1; //As each row is completed, store index to next
	}
	return k;
}

