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
    }
}
