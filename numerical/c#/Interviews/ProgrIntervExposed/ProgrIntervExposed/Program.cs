using InterviewPrep.Recursion;
using InterviewPrep.Tree;
using InterviewPrep.Arrays;
using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static InterviewPrep.Arrays.ArraysStrings;

namespace InterviewPrep
{
    class Program
    {
        static void Main(string[] args)
        {
            // Permutations of an array.
            int[] arr = new int[] { 0, 3, 2, 1, 4, 9, 6, 7, 8, 5 };
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

            GenericArray<int>.MergeSort(arr, 0, arr.Length-1);

            int[,] mat = new int[,] { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 11 }, {9, 20, 100 } };
            Tuple<int, int> searchIndex = ArraysStrings.ElementSearch2D(mat, 20, 0, mat.GetLength(0)-1, 0, mat.GetLength(1) - 1);
            
            int[,] binary = new int[,] 
                                {
                                        {0, 1, 1, 0, 1},
                                        {1, 1, 0, 1, 0},
                                        {0, 1, 1, 1, 0},
                                        {1, 1, 1, 1, 0},
                                        {1, 1, 1, 1, 1},
                                        {0, 0, 0, 0, 0}
                                };

            int max1s = ArraysStrings.MaxSubmatrixOfOnes(binary);

            // Don't run this with large arrays.
            // Configurations.PrintConfigurations(arr, 0, res);

            StringBuilder paths = new StringBuilder();
            ArraysStrings.ListAllPaths(2, 2, paths);

            // Binary Search Trees.
            Node n1 = new Node(null, null, 1);
            Node n4 = new Node(null, null, 4);
            Node n3 = new Node(n1, n4, 3);
            Node n7 = new Node(null, null, 7);
            Node n12 = new Node(null, null, 12);
            Node n10 = new Node(n7, n12, 10);
            Node n5 = new Node(n3, n10, 5);

            // Arrays and strings.
            String testStr = "apple";

            double[,] input = new double[,] { { 1, 9}, {15, 20} };
            // ArraysStrings.CumulativeSum(input);

            double[,] optimals = ArraysStrings.OptimalPath(input);

            char[] inputChars = "apple".ToCharArray();
            ArraysStrings.removeDuplicates(inputChars);

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
