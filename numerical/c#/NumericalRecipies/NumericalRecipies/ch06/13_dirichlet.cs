using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NumericalRecipies.ch06
{
    //Note that section 13 does not exist. This is my extension to the chapter.
    class _13_dirichlet
    {
        private static double regularizer = 0.1;
        /// <summary>
        /// Based on the formula for total information entropy given here - https://en.wikipedia.org/wiki/Dirichlet_distribution.
        /// </summary>
        /// <param name="alpha">The parameters of the Dirichlet distribution. These correspond to a histogram with counts.</param>
        /// <returns>The Entropy of a Dirichlet distribution.</returns>
        public double InformationEntropy(double[] alpha)
        {
            _2_gammafamily g = new _2_gammafamily();
            double alpha_0 = 0, H = 0;//The sum of coefficients (normalizing factor) and final entropy term respectively.
            int K = alpha.Length;
            for (int i = 0; i < K; i++)
            {
                alpha[i] += regularizer;//Before doing anything else, we regularize the parameters which is equivalent to a uniform prior.
                alpha_0 += alpha[i];
                H += g.Gammaln(alpha[i]);//Positive part of normalization constant (which is the log of a multivariate beta distribution).
                H -= (alpha[i] - 1) * g.Digamma(alpha[i]); //The contribution from each of the alphas.
            }
            H -= g.Gammaln(alpha_0);//Negative part of normalization constant.
            H += (alpha_0 - K) * g.Digamma(alpha_0);//The contribution from the normalizing factor.
            return H;
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="alpha">The parameters of the Dirichlet distribution. These correspond to a histogram with counts.</param>
        /// <returns>The Entropy of a Dirichlet distribution.</returns>
        public double RenyiInformation(double[] alpha, double lambda)
        {
            _2_gammafamily g = new _2_gammafamily();
            double alpha_0 = 0, H = 0;//The sum of coefficients (normalizing factor) and final entropy term respectively.
            int K = alpha.Length;
            for (int i = 0; i < K; i++)
            {
                alpha[i] += regularizer;//Before doing anything else, we regularize the parameters which is equivalent to a uniform prior.
                alpha_0 += alpha[i];
                H -= g.Gammaln(alpha[i]);//Positive part of normalization constant (which is the log of a multivariate beta distribution).
                H += g.Gammaln(lambda*(alpha[i] - 1) + 1); //The contribution from each of the alphas.
            }
            H += g.Gammaln(alpha_0);//Negative part of normalization constant.
            H -= g.Gammaln(lambda * (alpha_0 - K) + K);//The contribution from the normalizing factor.
            return H / (1-lambda);
        }
        public static void Main()
        {
            _13_dirichlet d = new _13_dirichlet();
            foreach (double x in new double[] {0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 5.0, 10.0, 50.0, 100.0})
            {
                System.Console.WriteLine(d.RenyiInformation(new double[] { x, 0, 0 }, 0.999999999));
                //System.Console.WriteLine(d.InformationEntropy(new double[] { x, 0, 0 }));
            }
            System.Console.Read();
        }
    }
}
