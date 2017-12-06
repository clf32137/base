using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InterviewPrep.Recursion
{
    class Combinations
    {
        public static List<string> CominateArr(string input, int n)
        {
            if (n == 1)
            {
                return new List<string> { input[0].ToString() };
            }
            else
            {
                List<string> cmbntns = new List<string> { input[n - 1].ToString() };
                List<string> lowerComb = CominateArr(input, n - 1);

                foreach (string st in lowerComb)
                {
                    cmbntns.Add(st);
                }

                foreach (string st in lowerComb)
                {
                    cmbntns.Add(input[n - 1].ToString() + st);
                }

                return cmbntns;
            }
        }
    }
}
