using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ProgrIntervExposed.Recursion
{
    class Configurations
    {
        public static void PrintConfigurations(int[] arr, int currDigit, int[] res)
        {
            if (currDigit >= arr.Length)
            {
                Console.Out.WriteLine(string.Join(",", res));
                return;
            }

            for (int i = 0; i < 3; i++)
            {
                res[currDigit] = i;
                PrintConfigurations(arr, currDigit + 1, res);
            }
        }

        static char GetCharKey(int tKey, int place)
        {
            if ((tKey < 0 && tKey > 9) || (place < 1 && place > 3))
            {
                return '\0';
            }
            switch (tKey)
            {
                case 0:
                    return '0';
                case 1:
                    return '1';
                case 2:
                    return Shift('A', place - 1);
                case 3:
                    return Shift('D', place - 1);
                case 4:
                    return Shift('G', place - 1);
                case 5:
                    return Shift('J', place - 1);
                case 6:
                    return Shift('M', place - 1);
                case 7:
                    return Shift('P', place - 1);
                case 8:
                    return Shift('T', place - 1);
                case 9:
                    return Shift('W', place - 1);
                default:
                    return '\0';
            }
        }

        static char Shift(char inchar, int shift)
        {
            inchar += (char)shift;
            return inchar;
        }
    }
}
