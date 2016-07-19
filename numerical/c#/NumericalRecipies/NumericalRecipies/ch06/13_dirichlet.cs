using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using MathNet.Numerics.Distributions;
using MathNet.Numerics.Properties;
using MathNet.Numerics.Random;


namespace NumericalRecipies.ch06
{
    //Note that section 13 does not exist. This is my extension to the chapter.
    class _13_dirichlet
    {
        private static double regularizer = 0.5;
        private double[] _alpha = { 1, 1};
        private double AlphaSum = 2.0;

        public double MathNetEntropy(double[] _alpha)
        {
            double AlphaSum = _alpha.Sum();
            _2_gammafamily g = new _2_gammafamily();
            var num = _alpha.Sum(t => (t - 1) * g.Digamma(t) - g.Gammaln(t));
            return -g.Gammaln(AlphaSum) + ((AlphaSum - _alpha.Length)*g.Digamma(AlphaSum)) - num;
        }

        public _13_dirichlet(double[] alpha)
        {
            this._alpha = new double[alpha.Length];
            alpha.CopyTo(_alpha, 0);
        }

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
        /// Based on the formula for Renyi information entropy given here - https://en.wikipedia.org/wiki/Dirichlet_distribution.
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

        public double RenyiInformationCorrected(double[] alpha, double lambda)
        {
            _2_gammafamily g = new _2_gammafamily();
            double alpha_0 = 0, H = 0;//The sum of coefficients (normalizing factor) and final entropy term respectively.
            int K = alpha.Length;
            for (int i = 0; i < K; i++)
            {
                alpha[i] += regularizer;//Before doing anything else, we regularize the parameters which is equivalent to a uniform prior.
                alpha_0 += alpha[i];
                H -= g.Gammaln(alpha[i]);//Positive part of normalization constant (which is the log of a multivariate beta distribution).
            }
            H *= lambda;//This way, we do just one multiplication instead of K.
            for (int i = 0; i < K; i++)
            {
                H += g.Gammaln(lambda * (alpha[i] - 1) + 1); //The contribution from each of the alphas.
            }
            H += lambda * g.Gammaln(alpha_0);//Negative part of normalization constant.
            H -= g.Gammaln(lambda * (alpha_0 - K) + K);//The contribution from the normalizing factor.
            return H / (1 - lambda);
        }

        /// <summary>
        /// Uses relative state space as a measure of skewness. The formula is - 
        /// $log(MultivariateBeta(alpha)/MultivariateBeta(flat_alpha))$
        /// </summary>
        /// <param name="alpha">The parameters of the Dirichlet distribution. These correspond to a histogram with counts.</param>
        /// <returns>The log of the ratio of the state space of the given distribution divided by the state space of a flat distribution.</returns>
        public double RelativeStateSpace(double[] alpha)
        {
            _2_gammafamily g = new _2_gammafamily();
            double alpha_0 = 0, h = 0;
            int k = alpha.Length;
            for (int i = 0; i < k; i++)
            {
                alpha[i] += regularizer;
                alpha_0 += alpha[i];
                h -= g.Gammaln(alpha[i]); // Add the multinomial coefficient contribution.
            }

            h += k * g.Gammaln(alpha_0 / k); // Add the contribution from the flat multinomial coefficient.
            return h;
        }

        /// <summary>
        /// Finds the KL divergence between two Dirichlet distributions.
        /// </summary>
        /// <param name="other"></param>
        /// <returns></returns>
        public double KLDivergence(_13_dirichlet other)
        {
            
        }

        public static void Main()
        {
            _13_dirichlet d = new _13_dirichlet();
            
            foreach (double x in new double[] { 1, 2, 3 })
            {
                //System.Console.WriteLine((x + regularizer) + "\t" + d.RenyiInformationCorrected(new double[] { x, x, x }, 0.1));
                //System.Console.Write(d.RenyiInformationCorrected(new double[] { x, x, x, x }, 0.5) + "\t");
                //System.Console.WriteLine(d.RenyiInformationCorrected(new double[] { x, x, x }, 0.999999));
                //System.Console.WriteLine(d.InformationEntropy(new double[] { x }));
            }

            //System.Console.WriteLine(d.RelativeStateSpace(new double[] { 60, 55, 18, 8, 18, 30, 23, 62, 13, 44, 23, 48, 24, 40, 38, 45, 11, 2 }));

            double[] alpha = new double[] { 60, 55, 18, 8, 18, 30, 23, 62, 13, 44, 23, 48, 24, 40, 38, 45, 11, 2 };
            

            //System.Console.WriteLine(d.RelativeStateSpace(new double[] { 1000,0,0,0 }));
            System.Console.WriteLine(d.InformationEntropy(new double[]{30, 5, 2, 1, 3, 1}));

            //System.Console.WriteLine(d.MathNetEntropy(new double[]{1.5,1.5,1.5}));
            System.Console.Read();
        }
    }
}
