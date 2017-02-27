using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InterviewPrep.Tree
{
    public class Node
    {
        // Properties..
        public Node Left;
        public Node Right;
        public int Value;

        // Constructor
        public Node(Node left, Node right, int value)
        {
            this.Left = left;
            this.Right = right;
            this.Value = value;
        }

        public static void PreorderTraverseNoRecurse(Node root)
        {
            Stack<Node> stk = new Stack<Node>();
            Node popped;
            while (root != null)
            {
                Console.Out.WriteLine(root.Value);
                if (root.Left != null)
                {
                    if (root.Right != null)
                    {
                        stk.Push(root.Right);
                    }
                    root = root.Left;
                }
                else if (root.Right != null)
                {
                    root = root.Right;
                }
                else
                {
                    if (stk.Count != 0)
                    {
                        popped = stk.Pop();
                        root = popped;
                    }
                    else
                    {
                        break;
                    }
                }
            }
        }
    }
}
