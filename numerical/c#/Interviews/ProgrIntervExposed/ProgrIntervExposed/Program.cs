using ProgrIntervExposed.Tree;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ProgrIntervExposed
{
    class Program
    {
        static void Main(string[] args)
        {
            // Permutations of an array.
            int[] arr = new int[] { 0, 1, 2 };
            int[] res = new int[arr.Length];
            bool[] used = new bool[arr.Length];
            PermuteArr(arr, res, used, 0, 0);
            //List <int> lst = new List<int>(arr);
            //PermuteArr(lst, 0);

            // Combinations of array.
            Console.Out.WriteLine("Now combinations");
            string str = "abcd";
            List<string> combntns = CominateArr(str, str.Length);
            foreach (string st in combntns)
            {
                Console.Out.WriteLine(st);
            }

            PrintConfigurations(arr, 0, res);

            Node n1 = new Node(null, null, 1);
            Node n4 = new Node(null, null, 4);
            Node n3 = new Node(n1, n4, 3);
            Node n7 = new Node(null, null, 7);
            Node n12 = new Node(null, null, 12);
            Node n10 = new Node(n7, n12, 10);
            Node n5 = new Node(n3, n10, 3);


            Console.Read();
        }

        static void PrintConfigurations(int[] arr, int currDigit, int[] res)
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

        static List<string> CominateArr(string input, int n)
        {
            if (n == 1)
            {
                return new List<string> { input[0].ToString() };
            }
            else
            {
                List<string> cmbntns = new List<string> { input[n-1].ToString()};
                List<string> lowerComb = CominateArr(input, n - 1);

                foreach (string st in lowerComb)
                {
                    cmbntns.Add(st);
                }

                foreach (string st in lowerComb)
                {
                    cmbntns.Add(input[n-1].ToString() + st);
                }
                
                return cmbntns;
            }
        }


        /// Permute an array.
        static void PermuteArr(int[] arr, int[] res, bool[] used, int indx, int n)
        {
            if (n >= arr.Length)
            {
                Console.Out.WriteLine(string.Join(",", res));
                return;
            }

            for (int i = 0; i < arr.Length; i++)
            {
                if (!used[i])
                {
                    res[indx++ % res.Length] = arr[i];
                    used[i] = true;
                    PermuteArr(arr,res,used,indx,n+1);
                    used[i] = false; // Undo what was wrought.
                    indx--;
                }
            }
        }

        static void PermuteArr(List<Int32> arr, int k)
        {
            for (int i = k; i < arr.Count; i++)
            {
                Swap(arr, i, k);
                PermuteArr(arr, k + 1);
                Swap(arr, k, i);
            }
            if (k == arr.Count - 1)
            {
                Console.Out.WriteLine(string.Join(",", arr));
            }
        }

        static void Swap(List<Int32> arr, int i, int j)
        {
            int temp = arr[j];
            arr[j] = arr[i];
            arr[i] = temp;
        }

        static void Swap(int[] arr, int i, int j)
        {
            int temp = arr[j];
            arr[j] = arr[i];
            arr[i] = temp;
        }
    }
}
