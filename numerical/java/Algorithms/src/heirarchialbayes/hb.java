/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package heirarchialBayes;

import org.apache.commons.math3.linear.ArrayRealVector;
import org.apache.commons.math3.linear.CholeskyDecomposition;
import org.apache.commons.math3.linear.LUDecomposition;
import org.apache.commons.math3.linear.MatrixUtils;
import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.linear.RealVector;
import org.apache.commons.math3.distribution.NormalDistribution;
import random.StdRandom;

/**
 *
 * @author rohit576
 */
public class hb {
    public static int resp = 500;
    public static int trips = 15;
    public static int items = 3;
    public static int itrns = 40000;
    public static int burnins = 10000;
    public static void main(String[] args){
        long startTime = System.currentTimeMillis();
        double[][][] prices = new double [resp][trips][items];
        for(int i=0;i<resp;i++){
            for(int j=0;j<trips;j++){
                for(int k=0;k<items;k++){
                    prices[i][j][k] = StdRandom.gaussian(2, 1.3);
                }
            }
        }
        double bt1[] = new double[] {1d,1d,-1d};//The first element remember is frozen to zero.
        double w[][] = new double[][] {{1d,0d,0d},{0d,1d,0d},{0d,0d,1d}};
        RealMatrix Wt1 = MatrixUtils.createRealMatrix(w);
        double[][] betas = new double [resp][(items+1)];
        for(int i=0;i<resp;i++)betas[i] = nextGaussian(bt1, Wt1);
        int[][][] choices = new int[resp][trips][items];
        choices = genchoices(prices, betas);
        fileIO.fileIO.writechsfile(prices, choices, "test1.chs");
        fileIO.fileIO.writecustomfile(prices, choices, "test1.csv");
        /*prices = new double[][][]{{{2d,2.1d,3d},
                                   {1.1d,.9d,5d},
                                   {1.1d,3d,.8d}}, {
                                       {.5d,.6d,.8d},
                                       {.8d,.6d,.5d},
                                       {.1d,.5d,.25d}}, {
                                           {.1d,.5d,.9d},
                                           {.5d,.1d,.2d},
                                           {.2d,1.1d,.9d}}};*/
        /*prices = new double[][][]{{{1d,1d,1d},
                                   {1d,1d,1d},
                                   {1d,1d,1d}}, {
                                       {1d,1d,1d},
                                       {1d,1d,1d},
                                       {1d,1d,1d}}, {
                                           {1d,1d,1d},
                                           {1d,1d,1d},
                                           {1d,1d,1d}}};*/
        /*choices = new int[][][]{{{1,0,0},
                                   {0,1,0},
                                   {0,0,1}}, {
                                       {1,0,0},
                                       {1,0,0},
                                       {1,0,0}}, {
                                           {1,0,0},
                                           {0,0,1},
                                           {0,0,1}}};
        betas = new double[][]{{1d,1d,1d},{1d,1d,1d},{1d,1d,1d}};*/
        //Confirmation that premultiplying a vector to a matrix actually means post multiplying it.
        /*double[][] A = { { 1, 0 },
                         { 0, 1 }
                       };
        RealMatrix a = MatrixUtils.createRealMatrix(A);/*
        double[] a1 = {1,2,3};
        double[] a2;
        a2 = new CholeskyDecomposition(a).getL().preMultiply(a1);*/
        //double d = gauspdf(new double[] {0d,0d},new double[]{0d,0d},a);
        //double w[][] = new double[][] {{2d,1d,1d,1d},{1d,2d,1d,1d},{1d,1d,2d,1d},{1d,1d,1d,2d}};
              
        double[][] betat1 = new double[betas.length][betas[0].length];
        for(int i=0;i<betas.length;i++)for(int j=0;j<betas[i].length;j++)betat1[i][j]=betas[i][j];
        double[] bt = null;
        int N = resp,K = bt1.length;
        double[][] meanbetas = new double[betas.length][betas[0].length];
        RealMatrix meanW = MatrixUtils.createRealMatrix(K, K);
        double[][] meanb = new double[N][K];
        for(int i=0;i<itrns;i++){
            //One draw from a gaussian
            for(int k=0;k<K;k++)bt1[k]=0d;
            for(int j=0;j<betat1.length;j++){//First take average of beta_t
                for(int k=0;k<K;k++){
                    bt1[k]+=betat1[j][k]/N;
                }
            }
            System.out.println(i);
            try{
                bt = nextGaussian(bt1, Wt1.scalarMultiply(Math.pow(N,-1)));
            }
            catch(Exception e){
                e.printStackTrace();
                System.out.println(Wt1.toString());
                break;
            }
            //And one draw from IW
            RealVector vbt = new ArrayRealVector(bt);
            double[][] tempm = new double[K][K];for(int ro=0;ro<tempm.length;ro++)for(int co=0;co<tempm[ro].length;co++)tempm[ro][co]=0d;
            RealMatrix m = MatrixUtils.createRealMatrix(tempm);
            for(int j=0;j<N;j++){
                RealVector vbetat = new ArrayRealVector(betat1[j]);
                RealVector diff = vbetat.subtract(vbt);
                m = m.add(diff.outerProduct(diff));
            }
            for(int k=0;k<K;k++){
                m.addToEntry(k, k, K);
            }
            m = m.scalarMultiply(Math.pow((K+N),-1));
            try{
                Wt1 = nextWishart((K+N),m);
                if(i>burnins)meanW.add(Wt1);
            }catch(Exception e){
                e.printStackTrace();
                System.out.println(Wt1.toString());
                break;
            }
            //Finally one iteration of the MH algorithm..across all respondents
            for(int i1=0;i1<N;i1++){
                double[] trialb = nextGaussian(betat1[i1],Wt1,0.33d);
                double unif = StdRandom.uniform();
                double d1 = lik(prices[i1],choices[i1],trialb)*gauspdf(trialb,bt,Wt1);
                d1 /= lik(prices[i1],choices[i1],betat1[i1])*gauspdf(betat1[i1],bt,Wt1);
                if(d1>=unif)betat1[i1]=trialb;
                if(i>burnins)for(int ro=0;ro<K;ro++)meanb[i1][ro] += trialb[ro];
            }
        }
        //Write out the mean results.
        for(int i = 0; i<meanb.length; i++){
            for(int j = 0; j<meanb[i].length; j++){
                fileIO.fileIO.write2file(meanb[i][j]/30000+",", "params.csv");
            }
            fileIO.fileIO.write2file("\n", "params.csv");
        }
        for(int i = 0; i<meanW.getRowDimension(); i++){
            for(int j = 0; j<meanW.getColumnDimension(); j++){
                fileIO.fileIO.write2file(String.valueOf(meanW.getEntry(i, j)/30000)+ ",", "params.csv");
            }
            fileIO.fileIO.write2file("\n", "params.csv");
        }
        long finishTime = System.currentTimeMillis();
        System.out.println("The program took: " + (finishTime-startTime)+ " ms to run");
        //System.out.println(lik);
    }
    public static double lik(double[][][] prices,int [][][] choices,double [][] betas){
        double lik=1d;
        for(int i=0;i<resp;i++){
            for(int j=0;j<trips;j++){
                double numr = 0d, denomn = 0d;
                for(int k=0;k<items;k++){
                    if(choices[i][j][k]>0)numr+=Math.exp(prices[i][j][k]*betas[i][3] + betas[i][k]);
                    denomn+=Math.exp(prices[i][j][k]*betas[i][3] + betas[i][k]);
                }
                lik *= numr/denomn;
            }
        }
        return lik;
    }
    public static double lik(double[][] prices,int [][] choices,double [] betas){
        double lik=1d;
        double[] betas1 = new double[betas.length+1];betas1[0]=1d;for(int i=1;i<betas1.length;i++)betas1[i]=betas[i-1];
        //for(int i=0;i<resp;i++){
            for(int j=0;j<trips;j++){
                double numr =0d, denomn=0d;
                for(int k=0;k<items;k++){
                    if(choices[j][k]>0)numr+=Math.exp(prices[j][k]*betas1[(betas1.length-1)] + betas1[k]);
                    denomn+=Math.exp(prices[j][k]*betas1[(betas1.length-1)] + betas1[k]);
                }
                lik *= numr/denomn;
            }
        //}
        return lik;
    }
    public static RealMatrix nextWishart(int df, RealMatrix scaleMatrix) {
        int dim = scaleMatrix.getRowDimension();
        double[][] draw = new double[dim][dim];
        double[][] z = new double[df][dim];
        for (int i = 0; i < z.length; i++) {
            for (int j = 0; j < z[i].length; j++) {
                //z[i][j] = Randomizer.nextGaussian();
                z[i][j] = StdRandom.gaussian();
            }
        }
        RealMatrix L = new LUDecomposition(scaleMatrix).getSolver().getInverse();
        for(int i=0;i<L.getRowDimension();i++)//Make it symmetric..
            for(int j=0;j<i;j++)L.setEntry(i, j, L.getEntry(j, i));
        L = new CholeskyDecomposition(L).getL();
        RealMatrix R = MatrixUtils.createRealMatrix(dim, dim);
        for(int i=0;i<df;i++){
            RealVector v1 = MatrixUtils.createRealVector(z[i]);//Test this with R or matlab..
            RealVector temp = L.transpose().preMultiply(v1);//(L\eta_i)'
            RealMatrix temp2 = temp.outerProduct(temp);
            R = R.add(temp2);
        }
        R = R.scalarMultiply(Math.pow(df, -1));
        R = new LUDecomposition(R).getSolver().getInverse();
        return R;
    }
    public static double[] nextGaussian(double[] means, RealMatrix var){
        //draw K iid standard normal deviates
        double[] z = new double[means.length];
        for(int i=0;i<z.length;i++)z[i]=StdRandom.gaussian();
        for(int i=0;i<var.getRowDimension();i++)//Make it symmetric..
            for(int j=0;j<i;j++)var.setEntry(i, j, var.getEntry(j, i));
        RealMatrix L = new CholeskyDecomposition(var).getL();
        double[] z1 = L.preMultiply(z);
        for(int i=0;i<z1.length;i++)z1[i]+=means[i];
        return z1;
    }
    public static double[] nextGaussian(double[] means, RealMatrix var,double rho){
        //draw K iid standard normal deviates
        double[] z = new double[means.length];
        for(int i=0;i<z.length;i++)z[i]=StdRandom.gaussian();
        for(int i=0;i<var.getRowDimension();i++)//Make it symmetric..
            for(int j=0;j<i;j++)var.setEntry(i, j, var.getEntry(j, i));
        RealMatrix L = new CholeskyDecomposition(var).getL();
        double[] z1 = L.preMultiply(z);for(int i=0;i<z1.length;i++)z1[i]*=rho;
        for(int i=0;i<z1.length;i++)z1[i]+=means[i];
        return z1;
    }
    public static double gauspdf(double[] vals, double[] means, RealMatrix cov){
        double res = 0d;
        RealVector v1 = MatrixUtils.createRealVector(vals);
        RealVector v2 = MatrixUtils.createRealVector(means);
        v1=v1.subtract(v2);
        double d1 = new LUDecomposition(cov).getDeterminant();
        RealMatrix siginv = new LUDecomposition(cov).getSolver().getInverse();
        res = Math.pow(2*Math.PI, -1*means.length/2)*Math.pow(d1, -0.5)*Math.exp(-1*siginv.preMultiply(v1).dotProduct(v1)/2);
        return res;
    }
    public static int[][][] genchoices(double[][][] prices,double [][] betas){
        int[][][] choices = new int[resp][trips][items];
        //for(int i=0;i<resp;i++)for(int j=0;j<trips;j++)for(int k=0;k<items;k++)choices[i][j][k]=0;
        for(int i=0;i<resp;i++){
            double[] betas1 = new double[betas[i].length+1];
            betas1[0]=1d;
            for(int i1=1;i1<betas1.length;i1++)betas1[i1]=betas[i][i1-1];
            for(int j=0;j<trips;j++){
                double max1=-2000d;int ch = 0;
                for(int k=0;k<items;k++){
                    if(prices[i][j][k]*betas1[3] + betas1[k]>max1){
                        max1 = prices[i][j][k]*betas1[3] + betas1[k];
                        ch = k;
                    }
                }
                choices[i][j][ch]=1;
            }
        }
        return(choices);
    }
}
