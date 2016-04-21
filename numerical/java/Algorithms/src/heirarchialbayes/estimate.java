/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package heirarchialBayes;

import org.apache.commons.math3.linear.Array2DRowRealMatrix;
import org.apache.commons.math3.linear.LUDecomposition;
import org.apache.commons.math3.linear.RealVector;
import org.apache.commons.math3.linear.MatrixUtils;
import org.apache.commons.math3.linear.RealVector;
import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.linear.CholeskyDecomposition;
import org.apache.commons.math3.random.GaussianRandomGenerator;
import org.apache.commons.math3.distribution.AbstractRealDistribution;
import linearAlgebra.Cholesky;
import random.StdRandom;


public class estimate {
 // Create a real matrix with two rows and three columns, using a factory
// method that selects the implementation class for us.
    public static void main(String[] args) {
        double[][] matrixData = { {1d,2d,3d}, {2d,5d,3d}};
        RealMatrix m = MatrixUtils.createRealMatrix(matrixData);
        // One more with three rows, two columns, this time instantiating the
        // RealMatrix implementation class directly.
        double[][] matrixData2 = { {1d,2d}, {2d,5d}, {1d, 7d}};
        double[][] A = { { 4, 1,  1 },
                         { 1, 5,  3 },
                         { 1, 3, 15 }
                       };
        RealMatrix a = MatrixUtils.createRealMatrix(A);
        RealMatrix n = new Array2DRowRealMatrix(matrixData2);
        // Note: The constructor copies  the input double[][] array in both cases.
        // Now multiply m by n
        RealMatrix p1 = m.multiply(n);
        int i1 = p1.getRowDimension();
        int j1 = p1.getRowDimension();
        System.out.println(p1.getEntry(0, 0));
        System.out.println(i1);
        // Invert p, using LU decomposition
        RealMatrix pInverse = new LUDecomposition(p1).getSolver().getInverse();
        RealMatrix chol = new CholeskyDecomposition(a).getL();
        RealMatrix chol1 = new CholeskyDecomposition(a).getLT();
        RealMatrix res = chol1.transpose().multiply(chol1);
        RealMatrix res1 = chol.multiply(chol.transpose());
        double[][] chol11 = Cholesky.cholesky(A);
        //Double[][] choll = cholesky(A);
        double aa = StdRandom.gaussian(1d,3d);
    }
}
