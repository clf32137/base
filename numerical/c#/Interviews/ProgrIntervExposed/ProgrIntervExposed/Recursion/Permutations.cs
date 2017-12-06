using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InterviewPrep.Recursion
{
    class Permutations
    {
        private static UInt64 counter = 0;
        /// Permute an array.
        public static void PermuteArr(int[] arr, int[] res, bool[] used, int indx, int n)
        {
            if (n >= arr.Length)
            {
                counter += 1;
                //Console.Out.WriteLine(counter + ":" + string.Join(",", res));
                if ( counter == 1000000)
                    Console.Out.WriteLine(counter + ":" + string.Join(",", res));
                return;
            }

            for (int i = 0; i < arr.Length; i++)
            {
                if (!used[i])
                {
                    res[indx++ % res.Length] = arr[i];
                    used[i] = true;
                    PermuteArr(arr, res, used, indx, n + 1);
                    used[i] = false; // Undo what was wrought.
                    indx--;
                }
            }
        }

        public static void PermuteArr(List<Int32> arr, int k)
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
