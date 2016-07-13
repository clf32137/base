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
            Program p = new Program();

            p.TestOneVariablePolynomialDivision();
            p.TestMultiVariatePolynomialDivision();
            
            System.Console.Read();
        }

        public void TestOneVariablePolynomialDivision()
        {
            //Test division of polynomials.
            OneVariablePolynomial dividend = new OneVariablePolynomial(new double[] { 1, 1, 2, 1 });
            OneVariablePolynomial divisor = new OneVariablePolynomial(new double[] { 1, 2 });
            Dictionary<string, OneVariablePolynomial> result = dividend.Divide(divisor);
            System.Console.WriteLine("Result of division:");
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
    }
}
