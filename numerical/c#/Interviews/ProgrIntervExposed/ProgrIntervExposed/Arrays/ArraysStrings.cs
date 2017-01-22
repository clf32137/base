using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ProgrIntervExposed.Arrays
{
    class ArraysStrings
    {
        public static string RemoveChars(string str, string remove)
        {
            var set = new HashSet<char>(remove.ToCharArray());
            char[] rem = remove.ToCharArray();
            bool[] flags = new bool[128]; // Assumes ASCII.
            return new string(rem, 0, 5);
        }

        public static void CumulativeSum(double[,] input)
        {
            for (int i = 0; i < input.GetLength(0); i++)
            {
                for (int j = 0; j < input.GetLength(1); j++)
                {
                    input[i, j] = input[i,j] + 
                        (i < 1 ? 0 : input[i - 1, j]) + (j < 1 ? 0 : input[i, j - 1]) - ((i < 1 || j < 1) ? 0 : input[i - 1, j - 1]);
                }
            }
        }

        /// <summary>
        /// Given a 2-d array of numbers. The cost of going from one cell of the array to the adjecent right or bottom 
        /// cell is the difference between the source cell and destination cell. This function uses dynamic programming
        /// to find the minimal cost of going from the top left of the matrix to the bottom right.
        /// </summary>
        /// <param name="input"></param>
        public static double[,] OptimalPath(double[,] input)
        {
            double[,] optimalPaths = new double[input.GetLength(0), input.GetLength(1)];
            double option1, option2;
            
            for (int i = 0; i < input.GetLength(0); i++)
            {
                for (int j = 0; j < input.GetLength(1); j++)
                {
                    if (i >= 1)
                    {
                        option1 = (optimalPaths[i - 1, j] - input[i - 1, j] + input[i, j]);
                        optimalPaths[i, j] = option1;
                    }

                    if (j >= 1)
                    {
                        option2 = (optimalPaths[i, j - 1] - input[i, j - 1] + input[i, j]);
                        optimalPaths[i, j] = (i > 1 ? Math.Min(optimalPaths[i, j], option2) : option2);
                        // If we store a boolean argmin as well in a 2-d array, then we can decipher the actual optimal path.
                    }
                }
            }

            return optimalPaths;
        }
    }
}
