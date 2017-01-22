using ProgrIntervExposed.Recursion;
using ProgrIntervExposed.Tree;
using ProgrIntervExposed.Arrays;
using System;
using System.Collections.Generic;
using System.Collections.Specialized;
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
            int[] arr = new int[] { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
            int[] res = new int[arr.Length];
            bool[] used = new bool[arr.Length];
            Permutations.PermuteArr(arr, res, used, 0, 0);
            //Permutations.PermuteArr(new List<int>(arr), 0);

            // Combinations of array.
            Console.Out.WriteLine("Now combinations");
            string str = "abcd";
            List<string> combntns = Combinations.CominateArr(str, str.Length);
            foreach (string st in combntns)
            {
                Console.Out.WriteLine(st);
            }

            // Configurations.PrintConfigurations(arr, 0, res);

            // Binary Search Trees.
            Node n1 = new Node(null, null, 1);
            Node n4 = new Node(null, null, 4);
            Node n3 = new Node(n1, n4, 3);
            Node n7 = new Node(null, null, 7);
            Node n12 = new Node(null, null, 12);
            Node n10 = new Node(n7, n12, 10);
            Node n5 = new Node(n3, n10, 5);

            // Arrays and strings.
            String testStr = "abcdab";

            double[,] input = new double[,] { { 1, 9}, {15, 20} };
            // ArraysStrings.CumulativeSum(input);

            double[,] optimals = ArraysStrings.OptimalPath(input);

            Random random = new Random();
            double x = random.NextDouble();

            // Data structures.
            Stack<Node> stk = new Stack<Node>();
            Queue<Node> qu = new Queue<Node>();
            Dictionary<string, int> dict = new Dictionary<string, int>();
            SortedDictionary<string, int> sdict = new SortedDictionary<string, int>();
            List<int> lst = new List<int>();

            Console.Read();
        }
    }
}
