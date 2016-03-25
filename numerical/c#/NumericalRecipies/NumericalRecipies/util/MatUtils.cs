using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using nr;

namespace NumericalRecipies.util
{
    class MatUtils
    {
        public static void fillMat(MatDoub a, Double[,] b)
        {
            int rows = a.nrows();
            for (int i = 0; i < rows; i++)
                for (int j = 0; j < rows; j++)
                    a[i][j] = b[i, j];
        }

        public static void printmatrix(MatDoub a)
        {
            for (int i = 0; i < a.nrows(); i++)
            {
                for (int j = 0; j < a.ncols(); j++)
                    System.Console.Write(a[i][j] + ",");
                System.Console.WriteLine();
            }
            System.Console.WriteLine();
        }
    }
}
