using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ProgrIntervExposed.Tree
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
    }
}
