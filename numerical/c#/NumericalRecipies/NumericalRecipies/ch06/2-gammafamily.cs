using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NumericalRecipies.ch06
{
    class _2_gammafamily:Constants
    {
        /// <summary>
        /// Computes the value of the Digamma function for integer values.
        /// </summary>
        /// <param name="n">the int value at which evaluation needs to happen</param>
        /// <returns>The digamma function evaluated at integer value, n.</returns>
        public double Digamma(int n)
        {
            ////Computation of Digamma(n) for positive integer n
            double s = -TheEulerConst;
            for (int k = 1; k < n; k++)
            {
                s += 1.0 / k;
            }

            return s;
        }

        /// <summary>
        /// Computes the value of the Digamma function for any double value. 
        /// This is defined as the derivative of the log(Gamma) function ($\frac{\Gamma'(x)}{\Gamma(x)}$).
        /// If curious how this enters the Entropy formula, check out derivation in the PDF in the implementation notes for the DR.
        /// </summary>
        /// <param name="x">The double value at which the evaluation needs to happen</param>
        /// <returns>Digamma function</returns>
        public double Digamma(double x)
        {
            double x_a = x, dgam = 0;
            ////For integers, use integer formula.
            if (Math.Abs(x_a - (int)x_a) <= Constants.TheZeroThreshold)
            {
                return this.Digamma((int)x);
            }
            else if (Math.Abs(x_a + .5 - (int)(x_a + .5)) <= Constants.TheZeroThreshold)
            {
                ////For x = an integer + 1 / 2 use Abramowitz&Stegun(page 258 formula 6.3.4) - http://people.math.sfu.ca/~cbm/aands/abramowitz_and_stegun.pdf
                int n = (int)(x_a - .5);
                for (int k = 1; k <= n; k++)
                {
                    dgam += 1.0 / (k + k - 1.0);
                }

                dgam = (2 * (dgam - Constants.LogOf2)) - Constants.TheEulerConst; ////In this manner, we minimize the number of multiplications.
            }
            else
            {
                ////Use formula for derivative of LogGamma(z)
                if (x_a < 10)
                {
                    int n = 10 - (int)x_a;
                    ////for | x | < 10, use recursively DiGamma(x) = DiGamma(x + 1) - 1 / x
                    for (int k = 0; k < n; k++)
                    {
                        dgam -= 1.0 / (k + x_a);
                    }

                    x_a += n;
                }

                double overx2 = 1.0 / (x_a * x_a), overx2k = overx2;
                dgam += Math.Log(x_a) - (.5 / x_a);
                for (int k = 0; k < 10; k++, overx2k *= overx2)
                {
                    dgam += Constants.DigammaCoeff[k] * overx2k;
                }
            }

            ////Reflection formula
            ////for x < 0, use Digamma(1 - x) = Digamma(x) + pi / tan(pi*x);
            if (x < 0)
            {
                dgam -= (Constants.Pi * Math.Tan(Constants.Pi * x)) + (1.0 / x); ////First multiplication then addition.
            }

            return dgam;
        }

        /// <summary>
        /// Computes the value of the log of the gamma function.
        /// We don't calculate Gamma directly as it can easily make the floating point precision overflow for modest inputs
        /// (being the generalization of a factorial function). It is based on a approximation derived by Lanczos.
        /// </summary>
        /// <param name="xx">Value at which computation needs to happen</param>
        /// <returns>The log the the gamma function at xx</returns>
        public double Gammaln(double xx)
        {
            double x, y, staticTerm, seriesSum;
            y = x = xx;
            staticTerm = x + 5.5;
            staticTerm -= (x + .5) * Math.Log(staticTerm);
            seriesSum = Constants.GammalnCoeff[0];
            for (int j = 0; j <= 5; j++)
            {
                seriesSum += Constants.GammalnCoeff[j + 1] / ++y;
            }

            return -staticTerm + Math.Log(Constants.Sqrt2Pi * seriesSum / x);
        }

        public static void _Main()
        {
            _2_gammafamily gam = new _2_gammafamily();
            
            System.Console.WriteLine(gam.Gammaln(100.3));
            System.Console.Read();
        }
    }
}
