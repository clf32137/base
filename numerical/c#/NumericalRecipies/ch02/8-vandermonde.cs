using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using nr;

namespace NumericalRecipies.ch02
{
    class Vander
    {
        //For theory see 31st Jan notes
        public Vander(VecDoub x, double[] w, double[] q)
        {
            // Solves the Vandermonde linear system PN1
            // iD0 xk i wi D qk .k D 0; : : : ; N  1/. Input consists
            // of the vectors x[0..n-1] and q[0..n-1]; the vector w[0..n-1] is output.
            int i, j, k, n = q.Length;
            double b, s, t, xx;
            VecDoub c = new VecDoub(n);
            if (n == 1)
                w[0] = q[0];
            else
            {
                for (i = 0; i < n; i++)
                    c[i] = 0.0; // Initialize array.
                c[n - 1] = -x[0]; // Coefficients of the master polynomial are found.
                for (i = 1; i < n; i++)
                { // by recursion.
                    xx = -x[i];
                    for (j = (n - 1 - i); j < (n - 1); j++)
                        c[j] += xx * c[j + 1];
                    c[n - 1] += xx;
                }
                for (i = 0; i < n; i++)
                { // Each subfactor in turn
                    xx = x[i];
                    t = b = 1.0;
                    s = q[n - 1];
                    for (k = n - 1; k > 0; k--)
                    { // Is synthetically divided.
                        b = c[k] + xx * b; //This is just the synthetic division formula.
                        s += q[k - 1] * b; // Matrix-multiplied by the right-hand side.
                        t = xx * t + b;
                    }
                    w[i] = s / t; // and supplied with a denominator.
                }
            }
        }
    }
}
