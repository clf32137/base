using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using nr;

namespace NumericalRecipies.ch02
{
    class QRdcmp
    {
        private int n;
        private final double[][] qt, r; // Stored QT and R.
        private boolean sing; // Indicates whether A is singular.
        
        public QRdcmp(MatDoub a)
        {
            n = a.nrows;
            MatDoub qt = new MatDoub(n, n);
            MatDoub r = new MatDoub(a);
            sing = (false);
            int i, j, k;
            VecDoub c = new VecDoub(n);
            VecDoub d = new VecDoub(n);
            double scale, sigma, sum, tau;
            
            for (k = 0; k < n - 1; k++)
            {
                scale = 0.0;
                for (i = k; i < n; i++)
                    scale = Math.Max(scale, Math.Abs(r[i][k]));
                if (scale == 0.0) 
                { // Singular case.
                    sing = true;
                    c[k] = d[k] = 0.0;
                }
                else 
                { // Form Qk and Qk A.
                    for (i = k; i < n; i++)
                        r[i][k] /= scale;

                    for (sum = 0.0, i = k; i < n; i++)
                        sum += r[i][k] * r[i][k];

                    sigma = SIGN(sqrt(sum), r[k][k]);
                    r[k][k] += sigma;
                    c[k] = sigma * r[k][k];
                    d[k] = -scale * sigma;

                    for (j = k + 1; j < n; j++) 
                    {
                        for (sum = 0.0, i = k; i < n; i++)
                            sum += r[i][k] * r[i][j];
                        tau = sum / c[k];
                        for (i = k; i < n; i++)
                            r[i][j] -= tau * r[i][k];
                    }
                }
             }
             d[n - 1] = r[n - 1][n - 1];
            if (d[n - 1] == 0.0)
                sing = true;

            ///////////////////////////
            for (i = 0; i < n; i++) 
            { // Form QT explicitly.
                for (j = 0; j < n; j++)
                    qt[i][j] = 0.0;
                qt[i][i] = 1.0;
            }
            for (k = 0; k < n - 1; k++) 
            {
                if (c[k] != 0.0) 
                {
                    for (j = 0; j < n; j++) 
                    {
                        sum = 0.0;
                        for (i = k; i < n; i++)
                            sum += r[i][k] * qt[i][j];
                        sum /= c[k];
                        for (i = k; i < n; i++)
                            qt[i][j] -= sum * r[i][k];
                    }
                }
            }
            for (i = 0; i < n; i++)
            { // Form R explicitly.
                r[i][i] = d[i];
                for (j = 0; j < i; j++)
                    r[i][j] = 0.0;
            }
        }

    }
}
