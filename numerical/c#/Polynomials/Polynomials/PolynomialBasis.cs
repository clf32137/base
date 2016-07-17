using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Polynomials
{
    class PolynomialBasis
    {
        public HashSet<Polynomial> polynomialData;

        /// <summary>
        /// Initializes a new instance of class PolynomialBasis
        /// </summary>
        /// <param name="inputPolynomials"></param>
        public PolynomialBasis(List<Polynomial> inputPolynomials)
        {
            polynomialData = new HashSet<Polynomial>();

            foreach (Polynomial p in inputPolynomials)
            {
                Polynomial toAdd = new Polynomial(p);
                polynomialData.Add(toAdd);
            }
        }

        /// <summary>
        /// Initializes a new instance of class PolynomialBasis
        /// </summary>
        /// <param name="inputPolynomials">An array of input polynomials</param>
        public PolynomialBasis(Polynomial[] inputPolynomials)
        {
            polynomialData = new HashSet<Polynomial>();

            foreach (Polynomial p in inputPolynomials)
            {
                Polynomial toAdd = new Polynomial(p);
                polynomialData.Add(toAdd);
            }
        }

        public PolynomialBasis(PolynomialBasis inputBasis)
        {
            polynomialData = new HashSet<Polynomial>();

            foreach (Polynomial p in inputBasis.polynomialData)
            {
                Polynomial toAdd = new Polynomial(p);
                polynomialData.Add(toAdd);
            }
        }

        /// <summary>
        /// Checks to see if the two polynomial bases are equal.
        /// </summary>
        /// <param name="obj"></param>
        /// <returns></returns>
        public override bool Equals(object obj)
        {
            PolynomialBasis other = (PolynomialBasis)obj;

            if (this.polynomialData.Count != other.polynomialData.Count)
            {
                return false;
            }

            foreach (Polynomial p in other.polynomialData)
            {
                if (!this.polynomialData.Contains(p))
                {
                    return false;
                }
            }

            return true;
        }

        /// <summary>
        /// Generates hash code for the polynomial object.
        /// </summary>
        /// <returns></returns>
        public override int GetHashCode()
        {
            int hash = 17;
            foreach (Polynomial p in this.polynomialData)
            {
                hash = hash * 31 + p.GetHashCode();
            }

            return hash;
        }

        public bool IsZero()
        {
            if (this.polynomialData == null || this.polynomialData.Count == 0)
            {
                return true;
            }

            foreach (Polynomial p in this.polynomialData)
            {
                if (!p.IsZero)
                {
                    return true;
                }
            }

            return true;
        }
    }
}
