using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NumericalRecipies.ch06
{
    class _2_gammafamily:constants
    {
        /// <summary>
        /// Computes the value of the Digamma function for integer values.
        /// </summary>
        /// <param name="n">the int value at which evaluation needs to happen</param>
        /// <returns></returns>
        private double Digamma(int n)
        {
            //Computation of Digamma(n) for positive integer n
            double s = -theEulerConst_;
            for (int k = 1; k < n; k++) s += 1.0 / k;
            return s;
        }
        /// <summary>
        /// Computes the value of the Digamma function for any double value.
        /// </summary>
        /// <param name="x">The double value at which the evaluation needs to happen</param>
        /// <returns></returns>
        public double Digamma(double x)
        {
            double x_a = x, dgam = 0;
            //For integers, use integer formula.
            if (Math.Abs(x_a - (int)(x_a)) <= theZeroThreshold_)
                return Digamma((int)(x));
            else if (Math.Abs(x_a + .5 - (int)(x_a + .5)) <= theZeroThreshold_)
            {
                //For x = an integer + 1 / 2 use Abramowitz&Stegun(page 258 formula 6.3.4)
                int n = (int)(x_a - .5);
                for (int k = 1; k <= n; k++) dgam += 1.0 / (k + k - 1.0);
                dgam = 2 * (dgam - log_of_2_) - theEulerConst_;//In this manner, we minimize the number of multiplications.
            }
            else
            {
                //Use formula for derivative of LogGamma(z)
                if (x_a < 10)
                {
                    int n = (10 - (int)(x_a));
                    //for | x | < 10, use recursively DiGamma(x) = DiGamma(x + 1) - 1 / x
                    for (int k = 0; k < n; k++) dgam -= 1.0 / (k + x_a);
                    x_a += n;
                }
                double overx2 = (1.0 / (x_a * x_a)), overx2k = overx2;
                dgam += Math.Log(x_a) - .5 / x_a;
                for (int k = 0; k < 10; k++, overx2k *= overx2) dgam += digamma_coeff[k] * overx2k;
            }
            //Reflection formula
            //for x < 0, use Digamma(1 - x) = Digamma(x) + pi / tan(pi*x);
            if (x < 0) dgam -= pi * (Math.Tan(pi * x)) + 1.0 / x;
            return dgam;
        }
        /// <summary>
        /// Computes the value of the log of the gamma function. 
        /// We don't calculate Gamma directly as it can easily make the floating point precision overflow for modest inputs.
        /// </summary>
        /// <param name="xx">Value at which computation needs to happen</param>
        /// <returns></returns>
        public double Gammaln(double xx)
        {
            double x, y, tmp, ser;
            y = x = xx;
            tmp = x + 5.5;
            tmp -= (x + .5) * Math.Log(tmp);
            ser = 1.000000000190015;
            for (int j = 0; j <= 5; j++) ser += gammaln_coeff[j] / ++y;
            return -tmp + Math.Log(2.5066282746310005 * ser / x);
        }


        public static void _Main()
        {
            _2_gammafamily gam = new _2_gammafamily();
            
            System.Console.WriteLine(gam.Gammaln(1000000));
            System.Console.Read();
        }
    }
}
