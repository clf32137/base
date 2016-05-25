using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Remoting.Messaging;
using System.Text;
using System.Threading.Tasks;
using nr;
using NumericalRecipies.util;

namespace NumericalRecipies.ch02
{
    class tst
    {
        
        public static void _Main(String[] args)
        {
            var array2D = new Double[,]
            {
                {3.0, 0.0, 1.0, 0.0, 0.0},  
		        {0.0, 4.0, 0.0, 0.0, 0.0},
		        {0.0, 7.0, 5.0, 9.0, 0.0},
		        {0.0, 0.0, 0.0, 0.0, 2.0},
		        {0.0, 0.0, 0.0, 6.0, 5.0}
            };

            MatDoub a = new MatDoub(5, 5);

            MatUtils.fillMat(a, array2D);
            MatUtils.printmatrix(a);
            
            MatDoub b = new MatDoub(5,5);
            MatUtils.fillMat(b, array2D);
            MatUtils.fillMat(a, array2D);
            
            GaussJordan.gaussj(a, b);
            MatUtils.printmatrix(a);

            LUdcmp lu = new LUdcmp(a);

            MatDoub aInv = new MatDoub(5, 5);//A container for the inverse of a.
            lu.inverse(aInv);
            MatUtils.printmatrix(aInv);

            MatUtils.fillMat(a, array2D);
            Sprsin sprs = new Sprsin(a);

            System.Console.Write("\n###################\n Sparse matrix \n###################\n");
            for (int i = 0; i < sprs.numelements; i++)
                System.Console.Write(sprs.sa[i] + (i + 1 < sprs.numelements ? "," : "\n"));
                                                                                                                                                                                                                                                                                          
            for (int i = 0; i < sprs.numelements; i++)
                System.Console.Write(sprs.ija[i] + (i + 1 < sprs.numelements ? "," : "\n"));
            
            //////////////////////////
            /// Now lets solve the system of linear equations.
            /////////////////////////
            VecDoub b1 = new VecDoub(new double[]{1,1,1,1,1});
            VecDoub x1 = new VecDoub(new double[]{0.14,0.3,0.5,-0.25,0.7});
            int iter = 0;
            double err = 0;
            
            System.Console.Write("\n###################\n Solution of sparse system \n###################\n");
            sprs.linbcg(b1, x1, 1, 1e-4d, 30,ref iter,ref err);
            
            for (int i = 0; i < 5; i++)
                System.Console.Write(x1[i] + (i + 1 < 5 ? "," : "\n"));
            
            //////////////////////////
            /// Vandermonde matrices.
            /////////////////////////
            System.Console.Write("\n###################\n Vandermonde matrices \n###################\n");
            VecDoub x_v = new VecDoub(new double[] { 2, 3, 5});
            double[] w = new double[] { 1, 1, 1 };
            double[] q = new double[] { 1, 1, 1 };
            
            Vander va = new Vander(x_v, w, q);

            for (int i = 0; i < w.Length; i++)
                System.Console.Write(w[i] + (i+1<w.Length?",":"\n"));

            //////////////////////////
            /// Toeplitz matrices.
            /////////////////////////
            System.Console.Write("\n###################\n Toeplitz matrices \n###################\n");
            VecDoub x_t = new VecDoub(new double[] { 1.3, 2, 3.7, 4, 5.2 });

            Toeplitz to = new Toeplitz(x_t, w, q);

            for (int i = 0; i < w.Length; i++)
                System.Console.Write(w[i] + (i + 1 < w.Length ? "," : "\n"));
            
            System.Console.WriteLine("End");
            System.Console.Read();
        }
    }
}
