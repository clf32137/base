using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using nr;


namespace NumericalRecipies.ch02
{
    class GaussJordan
    {
        public static void gaussj(MatDoub a, MatDoub b)
        {
            // Linear equation solution by Gauss-Jordan elimination,
            // equation (2.1.1) above. The input matrix is a[0..n-1][0..n-1].
            // b[0..n-1][0..m-1] is input containing the m right-hand side vectors.
            // On output, a is replaced by its matrix inverse, and b is replaced by
            // the corresponding set of solution vectors.
            int i, icol = 0, irow = 0, j, k, l, ll, n = a.nrows(), m = a.ncols();
            double big, dum, pivinv;
            VecInt indxc = new VecInt(n);
            VecInt indxr = new VecInt(n);
            VecInt ipiv = new VecInt(n); // These integer arrays are used
                                     // for bookkeeping on the pivoting.
            for (j = 0; j < n; j++)
                ipiv[j] = 0;
            for (i = 0; i < n; i++) { // This is the main loop over the columns to
                                      // be
                big = 0.0; // reduced.
                for (j = 0; j < n; j++)
                    // This is the outer loop of the search for a pivot over the entire matrix!
                    if (ipiv[j] != 1) // element.
                        for (k = 0; k < n; k++)
                            if (ipiv[k] == 0)
                                if (Math.Abs(a[j][k]) >= big)
                                {
                                    big = Math.Abs(a[j][k]);
                                    irow = j;
                                    icol = k;
                                }
            ++(ipiv[icol]);
            // We now have the pivot element, so we interchange rows, if needed,
            // to put the pivot element on the diagonal. The columns are not
            // physically interchanged, only relabeled: indxc[i], the column of the .iC1/th
            // pivot element, is the .iC1/th column that is reduced, while indxr[i] is
            // the row in which that pivot element was originally located.
            // If indxr[i] indxc[i], there is an implied column interchange.
            // With this form of bookkeeping, the solution bs will end up in the
            // correct order, and the inverse matrix will be scrambled by columns.
            if (irow != icol)
            {
                for (l = 0; l < n; l++)
                    NR.SWAP(a, irow, l, icol, l);
                for (l = 0; l < m; l++)
                    NR.SWAP(b, irow, l, icol, l);
            }
            indxr[i] = irow; // We are now ready to divide the pivot row by the
            // pivot element, located at irow and icol.
            indxc[i] = icol;
            if (a[icol][icol] == 0.0)
                throw new Exception("gaussj: Singular Matrix");
            pivinv = 1.0 / a[icol][icol];
            a[icol][icol] = 1.0;
            for (l = 0; l < n; l++)
                a[icol][l] *= pivinv;
            for (l = 0; l < m; l++)
                b[icol][l] *= pivinv;
            for (ll = 0; ll < n; ll++)
                // Next, we reduce the rows...
                if (ll != icol)
                { // ...except for the pivot one, of course.
                    dum = a[ll][icol];
                    a[ll][icol] = 0.0;
                    for (l = 0; l < n; l++)
                        a[ll][l] -= a[icol][l] * dum;
                    for (l = 0; l < m; l++)
                        b[ll][l] -= b[icol][l] * dum;
                }
            }
            // This is the end of the main loop over columns of the reduction. It
            // only remains to unscramble the solution in view of the column
            // interchanges. We do this by interchanging pairs of columns in the
            // reverse order that the permutation was built up.
            for (l = n - 1; l >= 0; l--)
                if (indxr[l] != indxc[l])
                    for (k = 0; k < n; k++)
                        NR.SWAP(a, k, indxr[l], k, indxc[l]);
        }

        public static void gaussj(MatDoub a)
        {
            // Overloaded version with no right-hand sides. Replaces a by its
            // inverse.
            MatDoub b = new MatDoub(a.nrows(), 0); // Dummy vector with zero columns.
            gaussj(a, b);
        }
       
    }
}
