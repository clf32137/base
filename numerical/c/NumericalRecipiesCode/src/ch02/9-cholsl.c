/*
** cholsl.c
**
** This function calculates the inverse of the decomposed cholesky matrix and
** backsubstitutes the vector through it.
**
** Function Type:
**    void
**
** Calling Procedure: 
**    cholsl ( matrix, np, dp, b, x );
**
** Inputs:
**    *matrix         double        Matrix to decompose
**    np              long          Number of time stamps and flux points
**    *dp             double        Output vector from decomposition
**    *b              double        Vector to backsubstitute
**
** !*!*!*! All arrays have standard C zero-offset arrays.
**
** Outputs:
**    *x              double        Backsubstituted vector.
**
** Originally written in FORTRAN by Bill Press.  Translated to C and modified
** by John Ellithorpe, 9/30/1991.
**
*/

#include <stdio.h>
#include "../../include/fileio.h"

void cholslinv( 
       matrix,
	     np,
	     dp,
	     b,
	     x)

  /* Inputs */

     float matrix[NMAT][NMAT];
     long   np;
     float dp[NMAT];
     float b[NMAT];
     float x[NMAT];

{
  
  /* Locals */

  long i,k;                           /* Dummy variables */
  float sum;                         /* Temp variable */

 /**********
 **       **
 ** Begin **
 **       **
 **********/

  for( i=0; i<np; i++ )
    {
      sum = b[i];
      k = i;
      while ( --k >= 0 )
	     sum -= matrix[i][k] * x[k];
      x[i] = sum / dp[i];
    }

  for( i=np-1; i>=0; i-- )
    {
      sum = x[i];
      k = i;
      while ( ++k < np )
	     sum -= matrix[k][i] * x[k];
      x[i] = sum / dp[i];
    }

 /**********
 **       **
 **  End  **
 **       **
 **********/

}

void cholslvec(float **a, int n, float p[], float b[], float x[])
{
  int i,k;
  float sum;

  for (i=1;i<=n;i++) {
    for (sum=b[i],k=i-1;k>=1;k--) sum -= a[i][k]*x[k];
    x[i]=sum/p[i];
  }
  for (i=n;i>=1;i--) {
    for (sum=x[i],k=i+1;k<=n;k++) sum -= a[k][i]*x[k];
    x[i]=sum/p[i];
  }
}