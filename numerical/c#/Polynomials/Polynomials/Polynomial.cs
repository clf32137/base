using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections;
using System.Collections.Specialized;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;

namespace Polynomials
{
    /// <summary>
    /// A polynomial can be defined as an ordered list of monomials.
    /// </summary>
    class Polynomial
    {
        public SortedDictionary<Monomial, double> monomialData;
        public string orderingScheme;
        public bool IsZero = true;
        private double zeroThreshold = 1e-4;
        
        /// <summary>
        /// Instatiates an instance of Polynomial class with a single monomial.
        /// </summary>
        /// <param name="m">The monomial to instantiate this polynomial with.</param>
        /// <param name="coefficient">The coefficient of the monomial.</param>
        public Polynomial(Monomial m, double coefficient = 1)
        {
            this.IsZero = false;
            this.monomialData = new SortedDictionary<Monomial, double>();
            if (coefficient != 0)
            {
                this.monomialData.Add(m, coefficient);
            }
        }

        /// <summary>
        /// Instantiates an instance of Polynomial class with monomial data.
        /// </summary>
        /// <param name="monomialData">SortedDictionary to be fed into monomial.</param>
        public Polynomial(SortedDictionary<Monomial,double> monomialData)
        {
            if (monomialData.Count > 0)
            {
                this.IsZero = false; 
                this.monomialData = monomialData;
            }
        }

        /// <summary>
        /// Instantiates an empty polynomial object.
        /// </summary>
        public Polynomial()
        {
            monomialData = new SortedDictionary<Monomial, double>();
        }

        public Polynomial(Polynomial other)
        {
            this.IsZero = other.IsZero;
            SortedDictionary<Monomial, double> newMonomialData = new SortedDictionary<Monomial, double>();
            foreach (Monomial m in other.monomialData.Keys)
            {
                newMonomialData.Add(m, other.monomialData[m]);
            }

            this.monomialData = newMonomialData;
        }

        /// <summary>
        /// Creates a copy of the object.
        /// </summary>
        /// <param name="other">The other instance to copy to.</param>
        /// <returns>The new polynomial deep copied.</returns>
        public void CopyInto(Polynomial other) //TODO: Check other polynomial is empty.
        {
            //TODO: Use a loop over properties instead of explicitly copying them.
            foreach (Monomial m in this.monomialData.Keys)
            {
                other.monomialData.Add(m, this.monomialData[m]);
            }

            other.IsZero = this.IsZero;
        }

        /// <summary>
        /// Gets the leading term as a monomial.
        /// </summary>
        /// <returns></returns>
        public Monomial GetLeadingTerm()
        {
            return monomialData.Keys.Last();
        }

        /// <summary>
        /// Gets the leading term as a polynomial.
        /// </summary>
        /// <param name="negate">If true, the coefficient is negated. Useful for subtraction.</param>
        /// <returns></returns>
        public Polynomial GetLeadingTermAsPolynomial(bool sign = true)
        {
            if (sign)
            {
                return new Polynomial(monomialData.Keys.Last(), monomialData[monomialData.Keys.Last()]);
            }
            else
            {
                return new Polynomial(monomialData.Keys.Last(), -monomialData[monomialData.Keys.Last()]);
            }
        }

        public void AddMonomial(Monomial m, double coefficient = 1)
        {
            if (monomialData.ContainsKey(m))
            {
                monomialData[m] += coefficient;
            }
            else
            {
                monomialData[m] = coefficient;
            }
        }

        /// <summary>
        /// Multiplies a monomial to each term of a polynomial
        /// </summary>
        /// <param name="multiplicant">The monomial being multiplied</param>
        public void MultiplyMonomial(Monomial multiplicant, double coefficient = 1)
        {
            if (coefficient == 0)
            {
                this.IsZero = true;
                this.monomialData = null;
                return;
            }

            SortedDictionary<Monomial, double> result = new SortedDictionary<Monomial, double>();

            foreach (Monomial m in this.monomialData.Keys)
            {
                double originalCoefficient = this.monomialData[m];
                Monomial newM = new Monomial(m); // If we can get away with using m, we might save some memory.
                for (int i =0; i < m.powers.Length; i++) // TODO: Handle the case when the number of terms in the power arrays are different
                {
                    newM.powers[i] += multiplicant.powers[i];
                }

                result[newM] = originalCoefficient * coefficient;
            }

            this.monomialData = result;
        }

        /// <summary>
        /// From page 2 of CLO, a polynomial f divides another polynomial g if g = f.h for some h \in k[x_1, ... , x_n]
        /// This means that if g is divided by f then, g = f.h. 
        /// In this context, this will be true if every monomial in the polynomial is divided by the dividing monomial.
        /// </summary>
        /// <param name="dividingMonomial"> The monomial we are checking weather divides.</param>
        /// <returns>true or false depending on weather the monomial divides the polynomial.</returns>
        public bool IsDividedBy(Monomial dividingMonomial)
        {
            foreach (Monomial m in this.monomialData.Keys)
            {
                if (!m.Divides(dividingMonomial))
                {
                    return false;
                }
            }

            return true;
        }

        /// <summary>
        /// Divides the current polynomial by a list of divisor polynomials given by the argument.
        /// Based on the algorithm in section 2.3 of CLO book.
        /// </summary>
        /// <param name="divisorList">Comma saperated list with all the divisors.</param>
        /// <returns>The quotient and remainder in the form of a two element dictinoary.</returns>
        public List<Polynomial> DivideBy(params Polynomial[] divisorList)
        {
            Polynomial remainder = new Polynomial();
            Polynomial p = this;
            List<Polynomial> quotients = new List<Polynomial>();
            int s = divisorList.Length;
            
            foreach (Polynomial p1 in divisorList)
            {
                quotients.Add(new Polynomial());
            }

            while (!p.IsZero)
            {
                int i = 1;
                bool divisionoccurred = false;

                while (i <= s && !divisionoccurred)
                {
                    if (p.GetLeadingTerm().IsDividedBy(divisorList[i - 1].GetLeadingTerm()))
                    {
                        Monomial cancellingMonomial = p.GetLeadingTerm().DivideBy(divisorList[i - 1].GetLeadingTerm());
                        double cancellingCoefficient = p.monomialData[p.GetLeadingTerm()]/divisorList[i - 1].monomialData[divisorList[i - 1].GetLeadingTerm()];
                        quotients[i - 1].Add(new Polynomial(cancellingMonomial, cancellingCoefficient));

                        Polynomial cancellingPolynomial = new Polynomial(divisorList[i-1]);
                        cancellingPolynomial.MultiplyMonomial(cancellingMonomial, -cancellingCoefficient);
                        p.Add(cancellingPolynomial);

                        divisionoccurred = true;
                    }
                    else
                    {
                        i++;
                    }
                }

                if (!divisionoccurred)
                {
                    remainder.Add(p.GetLeadingTermAsPolynomial());
                    p.Add(p.GetLeadingTermAsPolynomial(false)); // A false addition is basically a subtraction. TODO: This is ugly! the Add method should have the flag to indicate subtraction.
                }
            }

            return quotients;
        }

        /// <summary>
        /// Adds other polynomial to this one.
        /// </summary>
        /// <param name="other">The polynomial to add to this one.</param>
        /// <returns>The result of the addition.</returns>
        public void Add(Polynomial other)
        {
            if (this.IsZero && !other.IsZero)
            {
                this.IsZero = false;
            }

            foreach (Monomial m in other.monomialData.Keys)
            {
                if (this.monomialData.ContainsKey(m))
                {
                    if (Math.Abs(this.monomialData[m] + other.monomialData[m]) < this.zeroThreshold) // Accounting for rounding error this way.
                    {
                        this.monomialData.Remove(m); // If the coefficients cancel, we can remove the term.
                        if (this.monomialData.Count == 0)
                        {
                            this.IsZero = true; //If via additions, all the coefficients become zero and we lose all terms, the polynomial has become zero.
                        }
                    }
                    else
                    {
                        this.monomialData[m] += other.monomialData[m]; // Update the coefficient.
                    }
                }
                else if(Math.Abs(other.monomialData[m]) > this.zeroThreshold ) // You have to be this tall to enter this ride.
                {
                    this.AddMonomial(m, other.monomialData[m]); // Add a new term with its coefficient.
                }
            }
        }

        /// <summary>
        /// Multiplies this polynomial to another polynomial.
        /// </summary>
        /// <param name="other"></param>
        /// <returns></returns>
        public Polynomial Multiply(Polynomial other)
        {
            throw new NotImplementedException();
        }
    }
}

//[1] http://stackoverflow.com/questions/8315154/get-the-largest-key-in-a-dictionary
