using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Polynomials
{
    class Monomial : IComparable
    {
        public int[] powers; // Consider uint instead of int.

        /// <summary>
        /// Initializes an instance of a monomial of a given degree.
        /// </summary>
        /// <param name="numVariables"></param>
        public Monomial(int numVariables, double coefficient = 1)
        {
            this.powers = new int[numVariables];
        }

        public Monomial(int[] powers, double coefficient = 1)
        {
            this.powers = powers;
        }

        public Monomial(Monomial m)
        {
            int[] newPowers = new int[m.powers.Length];
            for (int i = 0; i < newPowers.Length; i++)
            {
                newPowers[i] = m.powers[i];
            }

            this.powers = newPowers;
        }

        public int Compare(object x, object y)
        {
            Monomial m1 = (Monomial)x;
            Monomial m2 = (Monomial)y;

            // This is the lex ordering scheme.
            int numVariables = Math.Min(m1.powers.Length, m2.powers.Length);
            for (int i = 0; i < numVariables; i++)
            {
                if (m1.powers[i] > m2.powers[i])
                {
                    return 1;
                }
                else if (m1.powers[i] < m2.powers[i])
                {
                    return -1;
                }
            }

            return 0;
        }

        int IComparable.CompareTo(object obj)
        {
            Monomial m = (Monomial)obj;
            return Compare(this, m);
        }

        public override bool Equals(object obj)
        {
            Monomial other = (Monomial)obj;
            int numVariables = Math.Min(this.powers.Length, other.powers.Length);
            for (int i = 0; i < numVariables; i++)
            {
                if (this.powers[i] != other.powers[i])
                {
                    return false;
                }
            }

            return true;
        }

        public override int GetHashCode()
        {
            int hash = 17;
            for (int i = 0; i < this.powers.Length; i++)
            {
                hash = hash * 31 + i.GetHashCode();
            }

            return hash;
        }

        /// <summary>
        /// Checks to see if this polynomial divides the dividend polynomial.
        /// This polynomial plays the role of would be divisor.
        /// </summary>
        /// <param name="divisor"></param>
        /// <returns></returns>
        public bool Divides(Monomial dividend)
        {
            // TODO: Handle the case when the number of terms in the two polynomials is different.
            for (int i = 0; i < this.powers.Length; i++) 
            {
                if (dividend.powers[i] < this.powers[i])
                {
                    return false;
                }
            }

            return true;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="divisor"></param>
        /// <returns></returns>
        public bool IsDividedBy(Monomial divisor)
        {
            // TODO: Handle the case when the number of terms in the two polynomials is different.
            for (int i = 0; i < this.powers.Length; i++)
            {
                if (divisor.powers[i] > this.powers[i])
                {
                    return false;
                }
            }

            return true;
        }

        /// <summary>
        /// Divides this monomial with another.
        /// </summary>
        /// <param name="divisor">The divisor</param>
        /// <returns>The quotient from the division.</returns>
        public Monomial DivideBy(Monomial divisor)
        {
            int degree = Math.Min(divisor.powers.Length, this.powers.Length); // Ideally, the degrees of the two should be the same.
            int[] result = new int[degree];
            for (int i = 0; i < degree; i++)
            {
                result[i] = (this.powers[i] - divisor.powers[i]);
                if (result[i] < 0)
                {
                    throw new Exception("Monomial provided as dividend did not divide this monomial");
                }
            }

            return new Monomial(result);
        }
    }
}

//[1] Implementing comparators for classes - https://support.microsoft.com/en-us/kb/320727

