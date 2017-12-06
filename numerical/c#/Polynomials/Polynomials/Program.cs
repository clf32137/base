using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Polynomials
{
    class Program
    {
        static void Main(string[] args)
        {
            if (string.Concat("abc", string.Empty) == "abc")
            {
                System.Console.WriteLine("toldya!");
            }

            Program p = new Program();

            p.TestOneVariablePolynomialDivision();

            System.Console.WriteLine("##Multivariate polynomial division##");
            p.TestMultiVariatePolynomialDivision();

            System.Console.WriteLine("##S-polynomials##");
            p.TestSPolynomial();

            System.Console.WriteLine("##Groebner basis##");
            p.TestGroebnerBasis();

            System.Console.Read();
        }

        public void TestOneVariablePolynomialDivision()
        {
            OneVariablePolynomial dividend = new OneVariablePolynomial(new double[] { 1, 1, 2, 1 });
            OneVariablePolynomial divisor = new OneVariablePolynomial(new double[] { 1, 2 });
            Dictionary<string, OneVariablePolynomial> result = dividend.Divide(divisor);
            System.Console.WriteLine(string.Join(",", result["quotient"].coefficients));
        }

        public void TestMultiVariatePolynomialDivision()
        {
            Monomial m1 = new Monomial(new int[] { 2, 1 }); Monomial m2 = new Monomial(new int[] { 1, 2 }); Monomial m3 = new Monomial(new int[] { 0, 2 });
            Polynomial dividend = new Polynomial(m1);
            dividend.AddMonomial(m2);
            dividend.AddMonomial(m3); // x^2.y + x.y^2 + y^2

            Polynomial divisor1 = new Polynomial(new Monomial(new int[] { 0, 2 })); // (y^2 - 1)
            divisor1.AddMonomial(new Monomial(new int[] { 0, 0 }), -1);

            Polynomial divisor2 = new Polynomial(new Monomial(new int[] { 1, 1 })); // (xy - 1)
            divisor2.AddMonomial(new Monomial(new int[] { 0, 0 }), -1);

            List<Polynomial> quotients = dividend.DivideBy(divisor2, divisor1);

            foreach (Monomial m in quotients[0].monomialData.Keys)
            {
                System.Console.WriteLine(string.Join(",", m.powers));
            }
        }

        public void TestSPolynomial()
        {
            Polynomial f = new Polynomial(new Monomial(new int[] { 3, 2}), 1);
            f.AddMonomial(new Monomial(new int[] { 2, 3 }), -1);
            f.AddMonomial(new Monomial(new int[] { 1, 0 }), 1);

            Polynomial g = new Polynomial(new Monomial(new int[] { 4 , 1}), 3);
            g.AddMonomial(new Monomial(new int[] { 0, 2 }), 1);

            Polynomial s = f.GetSPolynomial(g);

            foreach (Monomial m in s.monomialData.Keys)
            {
                System.Console.WriteLine(string.Join(",", m.powers));
            }
        }

        /// <summary>
        /// Test method for Groebner basis.
        /// </summary>
        public void TestGroebnerBasis()
        {
            Monomial.orderingScheme = "grlex";

            Polynomial f = new Polynomial(new Monomial(new int[] { 3, 0 }), 1);
            f.AddMonomial(new Monomial(new int[] { 1, 1 }), -2); //x^3 -2.x.y

            Polynomial g = new Polynomial(new Monomial(new int[] { 2, 1 }), 1);
            g.AddMonomial(new Monomial(new int[] { 0, 2 }), -2);
            g.AddMonomial(new Monomial(new int[] { 1, 0 }), 1);

            PolynomialBasis gb = Polynomial.GroebnerBasis(f, g);

            int i = 0;
            foreach (Polynomial p in gb.polynomialData)
            {
                System.Console.WriteLine("Polynomial - " + i++.ToString());
                foreach (Monomial m in p.monomialData.Keys)
                {
                    System.Console.WriteLine(string.Join(",", m.powers));
                }
            }
        }
    }
}
