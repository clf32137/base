using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using nr;

namespace NumericalRecipies.ch02
{
    class Toeplitz
    {
        //Toeplitz matrices tend to occur in deconvolution and signal processing.
        public Toeplitz(VecDoub r, double[] x, double[] y)
        {
            // Solves the Toeplitz system
            // PN1
            // jD0 R.N1Cij/xj D yi .i D 0; : : : ; N  1/. The Toeplitz
            // matrix need not be symmetric. y[0..n-1] and r[0..2*n-2] are input
            // arrays; x[0..n-1] is the output array.

            int j, k, m, m1, m2, n1, n = y.Length;
            double pp, pt1, pt2, qq, qt1, qt2, sd, sgd, sgn, shn, sxn;
            n1 = n - 1;
            if (r[n1] == 0.0)
                throw new Exception("toeplz-1 singular principal minor");
            
            ////<Initialize x, g and h>
            x[0] = y[0] / r[n1]; 
            if (n1 == 0)
                return;
            VecDoub g = new VecDoub(n1), h = new VecDoub(n1);
            g[0] = r[n1 - 1] / r[n1];
            h[0] = r[n1 + 1] / r[n1];
            ////</Initialize x, g and h>

            ////<Main loop of the recursion>
            for (m = 0; m<n; m++)
            { 
                m1 = m + 1;
                ////<Compute numerator and denominator for x_{m+1} 2.8.19>
                sxn = -y[m1]; 
                sd = -r[n1]; 
                for (j = 0; j<m + 1; j++)
                {
                    sxn += r[n1 + m1 - j] * x[j];
                    sd += r[n1 + m1 - j] * g[m - j];
                }
                if (sd == 0.0)
                    throw new Exception("toeplz-2 singular principal minor");
                x[m1] = sxn / sd;
                ////</Compute numerator and denominator for x_{m+1} 2.8.19>

                ////<Compute x_{j} 2.8.15>
                for (j = 0; j<m + 1; j++)
                    // Eq. (2.8.16).
                    x[j] -= x[m1] * g[m - j];
                ////</Compute x_{j} 2.8.15>

                if (m1 == n1)
                    return;
                ////<Compute numerator and denominator for G and H, Equations 2.8.23 and 2.8.24>
                sgn = -r[n1 - m1 - 1];
                shn = -r[n1 + m1 + 1];
                sgd = -r[n1];
                for (j = 0; j<m + 1; j++)
                {
                    sgn += r[n1 + j - m1] * g[j];
                    shn += r[n1 + m1 - j] * h[j];
                    sgd += r[n1 + j - m1] * h[m - j];
                }
                if (sgd == 0.0)
                    throw new Exception("toeplz-3 singular principal minor");
                g[m1] = sgn / sgd; // whence G and H.
                h[m1] = shn / sd;
                ////</Compute numerator and denominator for G and H, Equations 2.8.23 and 2.8.24>

                ////<Compute G_j and H_j for j = 1 to m Equation 2.8.25>
                k = m;
                m2 = (m + 2) >> 1;
                pp = g[m1];
                qq = h[m1];
                for (j = 0; j<m2; j++)
                {//We split the two equations in 2.8.25 into 4 equations by replacing j by M+1-j. Double the equations mean half the iterations.
                    pt1 = g[j];
                    pt2 = g[k];
                    qt1 = h[j];
                    qt2 = h[k];
                    g[j] = pt1 - pp* qt2;
                    g[k] = pt2 - pp* qt1;
                    h[j] = qt1 - qq* pt2;
                    h[k--] = qt2 - qq* pt1;
                }
                ////<Compute G_j and H_j for j = 1 to m Equation 2.8.25>

            } // Back for another recurrence.
            throw new Exception("toeplz - should not arrive here!");
        }
        ////</Main loop of the recursion>
    }
}
