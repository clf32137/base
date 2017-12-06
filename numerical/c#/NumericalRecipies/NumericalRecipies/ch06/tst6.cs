using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NumericalRecipies.ch06
{
    class tst6
    {
        public static void Main(String[] args)
        {
            
            double[][] beta1 =
                new double[][]
                {
                    new double[]{2,0.1,0.1 },
                    new double[]{2,0.1,0.1 },
                    new double[]{2,0.1,0.1 }
                };

            double[][] beta = 
                        new double[][]
                        {
                            new double[]{2.8,   0.1,   0.1 },
                            new double[]{2.8,   0.1,   0.1 },
                            new double[]{2.8,   0.1,   0.1 }
                        };

            double[] alpha1 = new double[3];
            double[] alpha2 = new double[3];

            for (int i = 0; i < beta.Length; i++)
            {
                for (int j = 0; j < beta[i].Length; j++)
                {
                    alpha1[i] += beta[i][j];
                    alpha2[j] += beta[i][j];
                }
            }

            Dirichlet dr1 = new Dirichlet(alpha1);
            Dirichlet dr2 = new Dirichlet(alpha2);

            double res = dr1.KLDivergence(dr2, beta);

            System.Console.WriteLine("KL divergence is:" + res);

            System.Console.Read();
        }

        
    }
}
