/**************************************************
Given a matrix a[1..n][1..n], this routine replaces it by the LU decomposition of a rowwise permutation of itself. 
a and n are input. a is output, arranged as in equation (2.3.14); 
indx[1..n] is an output vector that records the row permutation effected by the partial pivoting; 
d is output as ±1 depending on whether the number of row interchanges was even or odd, respectively. 
This routine is used in combination with lubksb to solve linear equations or invert a matrix.
**************************************************/
#include <math.h>
#define TINY 1.0e-20;
#define NRANSI
#include "../../include/nrutil.h" 
#define TINY 1.0e-20;


void ludcmp(float **a, int n, int *indx, float *d)
{
 	int i,imax,j,k;
 
        float big, dum, sum, temp;
 
        float *vv; //Stores the implicit scaling of each row.
 
        vv = vector(1,n);
 
        *d = 1.0; //No row interchanges yet.
 
        for (i=1;i<=n;i++) { //Loop through rows to get the implicit scaling information.
 
                big=0.0;
 
                for (j=1;j<=n;j++)
 
                        if ((temp=fabs(a[i][j])) > big) big = temp;
 
                if (big == 0.0) nrerror("Singular matrix in routine ludcmp"); //If largest element is zero after abs, the whole row is zero.
 
                vv[i] = 1.0/big; //Save the scaling.
 
        }
 
        for (j=1;j<=n;j++)
        { //This is the loop over columns for Crouts method.
 
                for (i=1;i<j;i++)
                { //This is equation 2.3.12 except for i=j.
 
                        sum = a[i][j];
 
                        for (k=1; k<i; k++) 
                                sum -= a[i][k]*a[k][j]; //because by now, a[i][k] has already been replaced by $\alpha[k][j]$ and a[k][j] by $\beta[k][j]$. See fig 2.3.1.
 
                        a[i][j] = sum;
 
                }
 
                big = 0.0; //Initialize for the search of the largest pivot element.
 
                for (i=j;i<=n;i++)
                {//Moving along the column as in figure 2.3.1. 
                //This is i=j of equation 2.3.12 and i = (j+1) to N of equation 2.3.13.
 
                        sum = a[i][j];
 
                        for (k=1;k<j;k++)

			     sum -= a[i][k]*a[k][j];//See loop2 in 1-4-2016 notes.
/*
https://onedrive.live.com/edit.aspx/Documents/Rohit^4s%20Notebook?cid=7cad132a61933826&id=documents&wd=target%28scheming.one%7CFE1272CF-6764-4D8C-AF68-296A975E75F3%2FNumericalRecipies%3A%20LU%20Decomposition%7C11677EEA-2BE1-4D6C-B6E9-2AE69E0D66B9%2F%29
onenote:https://d.docs.live.net/7cad132a61933826/Documents/Rohit's%20Notebook/scheming.one#NumericalRecipies%20LU%20Decomposition&section-id={FE1272CF-6764-4D8C-AF68-296A975E75F3}&page-id={11677EEA-2BE1-4D6C-B6E9-2AE69E0D66B9}&end
 */
                        a[i][j]=sum;
 
                        if ( (dum=vv[i]*fabs(sum)) >= big)
                        { //Is the figure of merit for the pivot better than the best so far?
			     big = dum;
			     imax = i;
			}
		}
 
                if (j != imax)
                { //Do we need to interchange rows?
 
                        for (k=1;k<=n;k++)
                        { //Yes we do. So swap all columns with imax row.
 
                                dum = a[imax][k];
 
                                a[imax][k] = a[j][k];
 
                                a[j][k] = dum;
 
                        }
 
                        *d = -(*d); //And change the parity of d.
 
                        vv[imax] = vv[j]; //Also interchange the scale factor.
                        //Because we only look to j>i for pivoting, we don't need to update the vv for this particular j.
 
                }
 
                indx[j]=imax;
 
                if (a[j][j] == 0.0) a[j][j] = TINY; //If the pivot element is zero, the matrix is singular to the precision of the algorithm. 
                //For some applications on singular matrices, we change TINY for zero.
 
                if (j != n) //If j==n, no more rows for updating \alpha as per 2.3.13.
                { //Now, finally divide by the pivot element.
 
                        dum = 1.0/(a[j][j]); //a[j][j] is \beta[j][j] by now.
 
                        for (i=j+1;i<=n;i++) a[i][j] *= dum;
 
                }
 
        } //Go back for the next column in the reduction.
 
        free_vector(vv,1,n);

}

#undef TINY

#undef NRANSI

