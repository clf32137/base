
namespace NumericalRecipies.ch06
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    /// <summary>
    /// Various properties of the Dirichlet distribution.
    /// </summary>
    public class Dirichlet
    {
        /// <summary>
        /// The regularizer is like a prior for the Dirichlet. Its needed since otherwise, for zero, the Entropy becomes -infinity.
        /// </summary>
        private static double regularizer = 0.5; ////The regularizer will guard against alpha parameters that contain zeros since the Entropy goes to -Inf for them.

        /// <summary>
        /// Initializes a new instance of the Dirichlet class
        /// </summary>
        /// <param name="alpha">The vector of counts falling into each category as input.</param>
        public Dirichlet(double[] alpha)
        {
            this.Alpha = new double[alpha.Length];
            alpha.CopyTo(this.Alpha, 0);
            this.SumAlpha = alpha.Sum();
        }

        /// <summary>
        /// Gets or sets the vector of counts falling into each category.
        /// </summary>
        public double[] Alpha { get; set; }

        /// <summary>
        /// Gets or sets the total sample size on which the Dirichlet is based.
        /// </summary>
        public double SumAlpha { get; set; }

        /// <summary>
        /// Based on the formula for total information entropy given here - https://en.wikipedia.org/wiki/Dirichlet_distribution.
        /// </summary>
        /// <returns>The Entropy of a Dirichlet distribution.</returns>
        public double InformationEntropy()
        {
            _2_gammafamily g = new _2_gammafamily();
            double alpha_0 = 0, h = 0; ////The sum of coefficients (normalizing factor) and final entropy term respectively.
            int k = this.Alpha.Length;
            for (int i = 0; i < k; i++)
            {
                this.Alpha[i] += regularizer; ////Before doing anything else, we regularize the parameters which is equivalent to a uniform prior.
                alpha_0 += this.Alpha[i];
                h += g.Gammaln(this.Alpha[i]); ////Positive part of normalization constant (which is the log of a multivariate beta distribution).
                h -= (this.Alpha[i] - 1) * g.Digamma(this.Alpha[i]); ////The contribution from each of the alphas.
            }

            h -= g.Gammaln(alpha_0); ////Negative part of normalization constant.
            h += (alpha_0 - k) * g.Digamma(alpha_0); ////The contribution from the normalizing factor.
            return h;
        }

        /// <summary>
        /// Based on the formula for Renyi information entropy given here - https://en.wikipedia.org/wiki/Dirichlet_distribution.
        /// </summary>
        /// <param name="lambda">The spectral parameter for the Renyi Entropy formula.</param>
        /// <returns>The Renyi spectral entropy of a Dirichlet distribution.</returns>
        public double RenyiInformation(double lambda)
        {
            _2_gammafamily g = new _2_gammafamily();
            double alpha_0 = 0, h = 0; ////The sum of coefficients (normalizing factor) and final entropy term respectively.
            int k = this.Alpha.Length;
            for (int i = 0; i < k; i++)
            {
                this.Alpha[i] += regularizer; ////Before doing anything else, we regularize the parameters which is equivalent to a uniform prior.
                alpha_0 += this.Alpha[i];
                h -= g.Gammaln(this.Alpha[i]); ////Positive part of normalization constant (which is the log of a multivariate beta distribution).
            }

            h *= lambda; ////This way, we do just one multiplication instead of K.
            for (int i = 0; i < k; i++)
            {
                h += g.Gammaln((lambda * (this.Alpha[i] - 1)) + 1); ////The contribution from each of the alphas.
            }

            h += lambda * g.Gammaln(alpha_0); ////Negative part of normalization constant.
            h -= g.Gammaln((lambda * (alpha_0 - k)) + k); ////The contribution from the normalizing factor.
            return h / (1 - lambda);
        }

        /// <summary>
        /// Uses relative state space as a measure of skewness. The formula is - 
        /// $log(MultivariateBeta(alpha)/MultivariateBeta(flat_alpha))$
        /// </summary>
        /// <returns>The log of the ratio of the state space of the given distribution divided by the state space of a flat distribution.</returns>
        public double RelativeStateSpace()
        {
            _2_gammafamily g = new _2_gammafamily();
            double alpha_0 = 0, h = 0;
            int k = this.Alpha.Length;
            for (int i = 0; i < k; i++)
            {
                this.Alpha[i] += regularizer;
                alpha_0 += this.Alpha[i];
                h -= g.Gammaln(this.Alpha[i]); // Add the multinomial coefficient contribution.
            }

            h += k * g.Gammaln(alpha_0 / k); // Add the contribution from the flat multinomial coefficient.
            return h;
        }

        /// <summary>
        /// Calculates the KL-divergence between this Dirichlet random variable and another  
        /// </summary>
        /// <param name="other">The other Dirichlet distribution.</param>
        /// <param name="beta">The two dimensional array of cross-counts.</param>
        /// <returns>The KL divergence</returns>
        public double KLDivergence(Dirichlet other, double[][] beta)
        {
            _2_gammafamily g = new _2_gammafamily();
            double kl = this.InformationEntropy();

            for (int i = 0; i < other.Alpha.Length; i++)
            {
                kl += g.Gammaln(other.Alpha[i]);
            }

            kl -= g.Gammaln(other.SumAlpha);

            double crossTerm;
            for (int i = 0; i < this.Alpha.Length; i++)
            {
                crossTerm = 0;
                for (int j = 0; j < other.Alpha.Length; j++)
                {
                    crossTerm -= (beta[i][j] - 1) * (g.Digamma(beta[i][j]) - g.Digamma(other.Alpha[j]));
                }

                kl -= crossTerm * this.Alpha[i] / this.SumAlpha;
            }

            return kl;
        }
    }
}