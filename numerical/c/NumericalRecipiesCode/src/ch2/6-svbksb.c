void svbksb(u,w,v,m,n,b,x)
/*****************************
Solves A.X = B for a vector X, where A is speciﬁed by the arrays u[1..m][1..n], w[1..n], v[1..n][1..n] as returned by svdcmp.
m and n are the dimensions of a, and will be equal for square matrices. b[1..m] is the input right-hand side.
x[1..n] is the output solution vector. No input quantities are destroyed, so the routine may be called sequentially with different b’s.
*****************************/
float **u, w[], **v, b[], x[];

int m,n;
{
	int jj,j,i;
	float s,*tmp,*vector();
	void free_vector();

	tmp=vector(1,n);
	for (j=1;j<=n;j++)
		{							//Calculate U^T b
		s=0.0;
		if (w[j])
		{							//Non zero result only if w_j is nonzero.
			for (i=1;i<=m;i++)
				s += u[i][j]*b[i];
			s /= w[j];				//This is the divide by w_j.
		}
		tmp[j]=s;
	}
	for (j=1;j<=n;j++)
	{								//Multiply by V to get answer.
		s=0.0;
		for (jj=1;jj<=n;jj++) 
			s += v[j][jj] * tmp[jj];
		x[j]=s;
	}
	free_vector(tmp,1,n);
}
