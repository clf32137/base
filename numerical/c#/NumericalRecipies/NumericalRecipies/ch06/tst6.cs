using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.Serialization.Formatters.Soap;
using Newtonsoft.Json;

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

            System.Console.WriteLine("howdy");
            double[,] arr = new double[,]
            {
                {0.1, 0.2, 0.7 },
                {0.3, 0.2, 0.5 },
                {0.5, 0.1, 0.4 }
            };

            var str = Helpers.ObjectToString(arr);

            System.Console.WriteLine(str);

            string out1 = JsonConvert.SerializeObject(arr);

            System.Console.WriteLine(out1);

            System.Console.Read();
        }

        
    }

    public static class Helpers
    {
        public static string ObjectToString(Array ar)
        {
            using (MemoryStream ms = new MemoryStream())
            {
                SoapFormatter formatter = new SoapFormatter();
                formatter.Serialize(ms, ar);
                return Encoding.UTF8.GetString(ms.ToArray());
            }
        }

        public static object ObjectFromString(string s)
        {
            using (MemoryStream ms = new MemoryStream(Encoding.UTF8.GetBytes(s)))
            {
                SoapFormatter formatter = new SoapFormatter();
                return formatter.Deserialize(ms) as Array;
            }
        }

        public static T ObjectFromString<T>(string s)
        {
            return (T)Helpers.ObjectFromString(s);
        }
    }
}
