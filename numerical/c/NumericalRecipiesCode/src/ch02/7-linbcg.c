#include <stdio.h>
#include <math.h>
#define NRANSI
#include "../../include/nrutil.h"
#define EPS 1.0e-14

/***************************************
View these equations in a latex editor. They are referenced in the comments. These are the bi-conjugate gradient with pre-conditioning matrix equations.
  \[\alpha_k = \frac{\vec rr_k^T \vec z_k}{\vec pp_k^T.A. \vec p_k} \tag{1}\]
  \[\vec r_{k+1} = \vec r_k - \alpha_k . A . \vec p_k \tag{2}\]
  \[\vec rr_k = \vec rr_k - \alpha_kA^T \vec pp_k \tag{3}\]
  \[\vec z_k = \widetilde{A}^{-1}. \vec r_k \tag{4}\]
  \[\vec zz_k = \widetilde{A}^{-T} \vec rr_k \tag{5}\]
  \[\beta_k = \frac{\vec rr_k^T.\vec z_{k+1}}{\vec rr_k ^T \vec z_k} \tag{6}\]
  \[\vec p_{k+1} = \vec z_{k+a} + \beta_k \vec p_k \tag{7}\]
  \[\vec pp_{k+1} = \vec zz_{k+1} + \beta_k. \vec pp_k \tag{8}\]
  \[\vec x_{k+a} = \vec x_k + \alpha_k. \vec p_k \tag{9}\]
 ***************************************/
void linbcg(unsigned long ija[], double dsa[], unsigned long n, double b[], double x[], int itol, double tol, int itmax, int *iter, double *err)
{
/***************************************************
Solves A· x = b for x[1..n], givenb[1..n], by the iterative biconjugate gradient method. 
On input x[1..n] should be set to an initial guess of the solution (or all zeros); itol is 1,2,3, or 4, 
specifying which convergence test is applied (see text); itmax is the maximum number of allowed iterations; 
and tol is the desired convergence tolerance. On output, x[1..n] is reset to the improved solution, 
iter is the number of iterations actually taken, and err is the estimated error. The matrix A is referenced 
only through the user-supplied routines atimes, which computes the product of either A or its transpose on a vector; 
and asolve, which solves A·x = b or A T ·x = b for some preconditioner matrix A (possibly the trivial diagonal part of A). 
***************************************************/
	void asolve(unsigned long ija[], double dsa[], unsigned long n, double b[], double x[], int itrnsp);
	void atimes(unsigned long ija[], double dsa[], unsigned long n, double x[], double r[], int itrnsp);
	double snrm(unsigned long n, double sx[], int itol);
	unsigned long j;
	double ak, akden, bk, bkden, bknum, bnrm, dxnrm, xnrm, zm1nrm, znrm;
	double *p, *pp, *r, *rr, *z, *zz;

	p = dvector(1,n);
	pp = dvector(1,n);
	r = dvector(1,n);
	rr = dvector(1,n);
	z = dvector(1,n);
	zz = dvector(1,n);

	*iter = 0;
	atimes(ija, dsa, n,x,r,0); //Input to atimes is x[1..n], output is r[1..n].
	for (j=1; j<=n; j++)
	{	//Initialize r and rr. The vectors corresponding to A and A^T.
		r[j] = b[j]-r[j];
		rr[j] = r[j];
	}
	/*atimes(n, r, rr, 0); */ //Uncomment this line to get maximum residual variant of the algorithm.
	if (itol == 1)
	{
		bnrm = snrm(n,b,itol);
		//Equation (4)
		asolve(ija, dsa, n,r,z,0); //Input is r[1..n], output is z[1..n]; the final 0 indicates that A and not its transpose is used.
	}
	else if (itol == 2)
	{
		asolve(ija, dsa, n,b,z,0);
		bnrm = snrm(n,z,itol);
		asolve(ija, dsa, n,r,z,0);
	}
	else if (itol == 3 || itol == 4)
	{
		asolve(ija, dsa, n,b,z,0);
		bnrm = snrm(n,z,itol);
		asolve(ija, dsa, n,r,z,0);
		znrm = snrm(n,z,itol);
	}
	else
		nrerror("illegal itol in linbcg");
	while (*iter <= itmax)  //Main loop.
	{
		++(*iter);
		//Equation (5)
		asolve(ija, dsa, n,rr,zz,1);	//Final 1 indicates use of transpose matrix AT
		
		for (bknum=0.0,j=1;j<=n;j++) 
			bknum += z[j]*rr[j]; //Numerator of equation (6)
		
		if (*iter == 1)
		{
			for (j=1;j<=n;j++)
			{
				p[j]=z[j];
				pp[j]=zz[j];
			}
		}
		else
		{
			bk = bknum/bkden; //beta
			for (j=1;j<=n;j++)
			{
				p[j] = bk*p[j]+z[j]; //Equation (7) 
				pp[j] = bk*pp[j]+zz[j]; //Equation (8)
			}
		}
		bkden = bknum; //Denominator of equation (6)
		
		atimes(ija, dsa, n, p, z, 0); //Since z has been used, we change its definition to save space.
		
		for (akden=0.0,j=1;j<=n;j++) //Denominator of equation (1)
			akden += z[j]*pp[j];

		ak = bknum/akden; //Equation (1)

		atimes(ija, dsa, n, pp, zz, 1); //Since zz has been used, we can changte the definition to save space.

		for (j=1;j<=n;j++)
		{
			x[j] += ak*p[j]; //Equation (9)
			r[j] -= ak*z[j]; //Equation (2)
			rr[j] -= ak*zz[j]; //Equation (3)
		}
		asolve(ija, dsa, n,r,z,0); //Equation (4)

		if (itol == 1)
			*err = snrm(n,r,itol)/bnrm;
 		else if (itol == 2)
			*err=snrm(n,z,itol)/bnrm;
		else if (itol == 3 || itol == 4)
		{
			zm1nrm=znrm;
			znrm=snrm(n,z,itol);
			if (fabs(zm1nrm-znrm) > EPS*znrm)
			{
				dxnrm = fabs(ak)*snrm(n,p,itol);
				*err = znrm/fabs(zm1nrm-znrm)*dxnrm;
			}
			else
			{
				*err = znrm/bnrm;	//Error may not be accurate, so loop again.
				continue;
			}
			xnrm=snrm(n,x,itol);
			if (*err <= 0.5*xnrm)
				*err /= xnrm;
			else
			{
				*err=znrm/bnrm;	//Error may not be accurate, so loop again.
				continue;
			}
		}
		printf("iter=%4d err=%12.6f\n",*iter,*err);
		if (*err <= tol) break;
	}

	free_dvector(p,1,n);
	free_dvector(pp,1,n);
	free_dvector(r,1,n);
	free_dvector(rr,1,n);
	free_dvector(z,1,n);
	free_dvector(zz,1,n);
}
#undef EPS
#undef NRANSI
