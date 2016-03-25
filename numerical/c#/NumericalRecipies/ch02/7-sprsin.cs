using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using nr;

namespace NumericalRecipies.ch02
{
    public class Sprsin
    {
        public int numelements;
        public VecDoub sa;
        public VecLong ija;

        private int n;
        private double thresh = 0.001;
        private int nmax = 30;
        private double EPS = 1.0e-14;

        public Sprsin(MatDoub a)//TODO: make a VecULong type to further save on space.
        {
            /************************************
            Converts a square matrix a[1..n][1..n] into row-indexed sparse storage mode.
            Only elements of a with magnitude ≥thresh are retained. Output is in two linear arrays
            with dimension nmax (an input parameter): sa[1..] contains array values, indexed by ija[1..].
            The number of elements ﬁlled of sa and ija on output are both ija[ija[1]-1]-1
            ************************************/
            sa = new VecDoub(new double[nmax]);
            ija = new VecLong(18, new long[nmax], 0);
            n = a.nrows();
            
            int i, j, k;
            for (j = 0; j < n; j++)
                sa[j] = a[j][j]; //Store the diagonal elements.

            ija[0] = n + 1; //Index to the first off diagonal element if any.
            k = n;

            for (i = 0; i < n; i++)
            {
                for (j = 0; j < n; j++)
                {
                    if (Math.Abs(a[i][j]) >= thresh && i != j)
                    {
                        if (++k > (int)nmax) throw new Exception("sprsin: nmax too small");
                        sa[k] = a[i][j]; //Store off diagonal elements.
                        ija[k] = j;	   //And their column indices.
                    }
                }
                ija[i + 1] = k + 1; //As each row is completed, store index to next
            }
            this.numelements = k+1;
        }
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

        public void linbcg(VecDoub b, VecDoub x, int itol, double tol, int itmax, ref int iter, ref double err)
        {
            VecDoub p = new VecDoub(n);
            VecDoub pp = new VecDoub(n);
            VecDoub r = new VecDoub(n);
            VecDoub rr = new VecDoub(n);
            VecDoub z = new VecDoub(n);
            VecDoub zz = new VecDoub(n);

            iter = 0;
            atimes(n, x, r, 0);

            double ak, akden, bk, bkden = 0, bknum = 0, bnrm, dxnrm, xnrm, zm1nrm, znrm = 0;
            int j;

            for (j = 0; j < n; j++)
            {   //Initialize r and rr. The vectors corresponding to A and A^T.
                r[j] = b[j] - r[j];
                rr[j] = r[j];
            }
            /*atimes(n, r, rr, 0); */
            //Uncomment this line to get maximum residual variant of the algorithm.
            if (itol == 1)
            {
                bnrm = snrm(n, b, itol);
                //Equation (4)
                asolve(n, r, z, 0); //Input is r[1..n], output is z[1..n]; the final 0 indicates that A and not its transpose is used.
            }
            else if (itol == 2)
            {
                asolve(n, b, z, 0);
                bnrm = snrm(n, z, itol);
                asolve(n, r, z, 0);
            }
            else if (itol == 3 || itol == 4)
            {
                asolve(n, b, z, 0);
                bnrm = snrm(n, z, itol);
                asolve(n, r, z, 0);
                znrm = snrm(n, z, itol);
            }
            else
                throw new Exception("illegal itol in linbcg");

            while (iter <= itmax) //Main loop.
            {
                ++iter;
                //Equation (5)
                asolve(n, rr, zz, 1);	//Final 1 indicates use of transpose matrix AT

                for (bknum = 0.0, j = 0; j < n; j++)
                    bknum += z[j] * rr[j]; //Numerator of equation (6)

                if (iter == 1)
                {
                    for (j = 0; j < n; j++)
                    {
                        p[j] = z[j];
                        pp[j] = zz[j];
                    }
                }
                else
                {
                    bk = bknum / bkden; //beta
                    for (j = 0; j < n; j++)
                    {
                        p[j] = bk * p[j] + z[j]; //Equation (7) 
                        pp[j] = bk * pp[j] + zz[j]; //Equation (8)
                    }
                }
                bkden = bknum; //Denominator of equation (6)

                atimes(n, p, z, 0); //Since z has been used, we change its definition to save space.

                for (akden = 0.0, j = 0; j < n; j++) //Denominator of equation (1)
                    akden += z[j] * pp[j];

                ak = bknum / akden; //Equation (1)

                atimes(n, pp, zz, 1); //Since zz has been used, we can changte the definition to save space.

                for (j = 0; j < n; j++)
                {
                    x[j] += ak * p[j]; //Equation (9)
                    r[j] -= ak * z[j]; //Equation (2)
                    rr[j] -= ak * zz[j]; //Equation (3)
                }
                asolve(n, r, z, 0); //Equation (4)

                if (itol == 1)
                    err = snrm(n, r, itol) / bnrm;
                else if (itol == 2)
                    err = snrm(n, z, itol) / bnrm;
                else if (itol == 3 || itol == 4)
                {
                    zm1nrm = znrm;
                    znrm = snrm(n, z, itol);
                    if (Math.Abs(zm1nrm - znrm) > EPS * znrm)
                    {
                        dxnrm = Math.Abs(ak) * snrm(n, p, itol);
                        err = znrm / Math.Abs(zm1nrm - znrm) * dxnrm;
                    }
                    else
                    {
                        err = znrm / bnrm;	//Error may not be accurate, so loop again.
                        continue;
                    }
                    xnrm = snrm(n, x, itol);
                    if (err <= 0.5 * xnrm)
                        err /= xnrm;
                    else
                    {
                        err = znrm / bnrm;	//Error may not be accurate, so loop again.
                        continue;
                    }
                }
                System.Console.WriteLine("iteration : " +  iter + " ;error : " + err);
                if (err <= tol) break;
            }
        }

        private double snrm(int n, VecDoub sx, int itol)
        {
            /*****************************
            Compute one of two norms for a vector sx[1..n] as signaled by itol. Used by linbcg.
            ****************************/
            int isamax;
            int i;
            double ans;

            if (itol <= 3)
            {
                ans = 0.0;
                for (i = 0; i < n; i++)
                    ans += sx[i] * sx[i]; //Vector magnitude norm.
                return Math.Sqrt(ans);
            }
            else
            {
                isamax = 1;
                for (i = 0; i < n; i++)
                { //Largest component norm
                    if (Math.Abs(sx[i]) > Math.Abs(sx[isamax]))
                        isamax = i;
                }
                return Math.Abs(sx[isamax]);
            }
        }

        private void asolve(int n, VecDoub b, VecDoub x, int itrnsp)
        {
            int i;
            for (i = 0; i < n; i++)
                x[i] = (sa[i] != 0.0 ? b[i] / sa[i] : b[i]); //The matrix A is the diagonal part of A, 
            //stored in the first n elements of sa. Since the transpose matrix has the same diagonal, the flag itrnsp is not used.
        }

        private void atimes(int n, VecDoub x, VecDoub r, int itrnsp)
        {
            if (itrnsp > 0) sprstx(sa, ija, x, r, n);
            else sprsax(sa, ija, x, r, n);
        }

        private void sprsax(VecDoub sa, VecLong ija, VecDoub x, VecDoub b, int n)
        {
            if (ija[1] != n + 2) new Exception("sprsax: mismatched vector and matrix");
            int i;
            long k;
            
            for (i = 0; i < n; i++)
            {
                b[i] = sa[i] * x[i]; //Diagonal entries
                for (k = ija[i]; k <= ija[i + 1] - 1; k++)//TODO: Verify this.
                    b[i] += sa[(int)k] * x[(int)ija[(int)k]]; //Off diagonal entries. Multiply the entry of the matrix by the x of the corresponding column.
                //TODO: Find out how to reference arrays in C# with some thing that could be > 2 billion (max value of integer).
            }
        }

        private void sprstx(VecDoub sa, VecLong ija, VecDoub x, VecDoub b, int n)
        {
            int i, j;
            long k;
            if (ija[1] != n + 2) new Exception("mismatched vector and matrix in sprstx");
            for (i = 0; i < n; i++)
                b[i] = sa[i] * x[i]; //First come the diagonal terms

            for (i = 0; i < n; i++)
            {//Now loop over the off diagonal terms.
                for (k = ija[i]; k <= ija[i + 1] - 1; k++)
                {
                    j = (int)ija[(int)k];
                    b[j] += sa[(int)k] * x[i]; //Because this is multiplication by the transpose, the indices of b and x interchange.
                }
            }
        }

    }
}
