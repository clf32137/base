using ProgrIntervExposed.Recursion;
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
            Permutations.PermuteArr(arr, res, used, 0, 0);
            //List <int> lst = new List<int>(arr);
            //PermuteArr(lst, 0);

            // Combinations of array.
            Console.Out.WriteLine("Now combinations");
            string str = "abcd";
            List<string> combntns = Combinations.CominateArr(str, str.Length);
            foreach (string st in combntns)
            {
                Console.Out.WriteLine(st);
            }

            Configurations.PrintConfigurations(arr, 0, res);

            // Binary Search Trees.
            Node n1 = new Node(null, null, 1);
            Node n4 = new Node(null, null, 4);
            Node n3 = new Node(n1, n4, 3);
            Node n7 = new Node(null, null, 7);
            Node n12 = new Node(null, null, 12);
            Node n10 = new Node(n7, n12, 10);
            Node n5 = new Node(n3, n10, 5);

            Stack<Node> stk = new Stack<Node>();

            Console.Read();
        }             
        
    }
}
