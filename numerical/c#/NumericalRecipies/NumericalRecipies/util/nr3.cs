using System;
using System.Numerics;

namespace nr
{
    public struct doubleptr
    {

        private double[] arr;
        private int off;
        public doubleptr(double[] arr, int off)
        {
            this.arr = arr;
            this.off = off;
        }
        public doubleptr(doubleptr ptr, int off)
        {
            this.arr = ptr.arr;
            this.off = ptr.off + off;
        }
        public double this[int i]
        {
            get { return arr[off + i]; }
            set { arr[off + i] = value; }
        }
    }
    public class NR
    {
        public static void SWAP<T>(ref T a, ref T b) { T dum = a; a = b; b = dum; }
        public static void SWAP<T>(T[] aVec, int a, T[] bVec, int b) { T dum = aVec[a]; aVec[a] = bVec[b]; bVec[b] = dum; }
        public static void SWAP(VecDoub aVec, int a, VecDoub bVec, int b) { double dum = aVec[a]; aVec[a] = bVec[b]; bVec[b] = dum; }
        public static void SWAP(MatDoub aMat, int ia, int ja, MatDoub bMat, int ib, int jb) { double dum = aMat[ia][ja]; aMat[ia][ja] = bMat[ib][jb]; bMat[ib][jb] = dum; }
        public static void SWAP(MatDoub x, int i, int j, int k, int l) {
            double t = x[i][j];
            x[i][j] = x[k][l];
            x[k][l] = t;
        }
        public static double SIGN(double a, double b) { return (b >= 0 ? (a >= 0 ? a : -a) : (a >= 0 ? -a : a)); }
        public static double SQR(double x)
        {
            return x * x;
        }
    }

    public class NRvector<T, A>
        where A : NRvector<T, A>, new()
    {
        private int nn;	// size of array. upper index is nn-1
        private T[] v;
        protected static Random rand = new Random(0);
        public T[] vect
        {
            get { return v; }
        }
        public NRvector()
        {
            nn = (0);
            v = (null);
        }
        // public NRvector(int n);		
        // Zero-based array
        public NRvector(int n)
        {
            nn = (n);
            v = (n > 0 ? new T[n] : null);
        }
        
        // public NRvector(int n, T a);	//initialize to constant value

        public NRvector(int n, T a)
        {
            nn = (n);
            v = (n > 0 ? new T[n] : null);
            for (int i = 0; i < n; i++) v[i] = a;
        }
        
        // public NRvector(int n, T[] a);	// Initialize to array

        public NRvector(int n, T[] a, int begin)
        {
            nn = (n);
            v = (n > 0 ? new T[n] : null);
            for (int i = 0; i < n; i++) v[i] = a[begin++];
        }
        // public NRvector(NRvector rhs);	// Copy constructor
        public NRvector(A rhs)
        {

            nn = (rhs.nn);

            v = (nn > 0 ? new T[nn] : null);



            for (int i = 0; i < nn; i++) v[i] = rhs[i];

        }

        // public T this[int i];	//i'th element

        public T this[int i]	//subscripting
        {

            get { return v[i]; }

            set { v[i] = value; }

        }



        /*SKM

        template <class T>

        inline const T & NRvector<T>::operator[](const int i) const	//subscripting

        {

        #ifdef _CHECKBOUNDS_

        if (i<0 || i>=nn) {

        	throw("NRvector subscript out of bounds");

        }

        #endif

        	return v[i];

        }

        */



        // public int size();

        public int size()
        {

            return nn;

        }



        //public void resize(int newn); // resize (contents not preserved)

        public void resize(int newn)
        {

            if (newn != nn)
            {

                //SKM if (v != null) delete[] (v);

                nn = newn;

                v = nn > 0 ? new T[nn] : null;

            }

        }



        // public void assign(int newn, T a); // resize and assign a constant value

        public void assign(int newn, T a)
        {

            if (newn != nn)
            {

                nn = newn;
                v = nn > 0 ? new T[nn] : null;

            }
            for (int i = 0; i < nn; i++) v[i] = a;

        }

        public void copyTo(NRvector<T, A> to)
        {

            if (size() != to.size())

                throw new Exception();

            System.Array.Copy(v, 0, to.v, 0, v.Length);

        }

        public void copyFrom(NRvector<T, A> from)
        {

            if (size() != from.size())

                throw new Exception();

            System.Array.Copy(from.v, 0, v, 0, from.v.Length);

        }

        public A shuffle()
        {
            int n = v.Length;
            A result = new A();
            result.resize(n);

            for (int i = 0; i < n; i++)
                result[i] = v[i];

            for (int k = n; k >= 1; k--)
            {
                int i = rand.Next() % k;
                T temp = result[k - 1];
                result[k - 1] = result[i];
                result[i] = temp;
            }
            return (A)result;
        }

    }



    // end of NRvector definitions



    // #endif //ifdef _USESTDVECTOR_



    public class NRmatrix<T, M>

        where M : NRmatrix<T, M>
    {

        private int nn;

        private int mm;

        private T[][] v;



        // public NRmatrix();

        public NRmatrix()
        {

            nn = (0);

            mm = (0);

            v = (null);

        }



        // public NRmatrix(int n, int m);			
        // Zero-based array

        public NRmatrix(int n, int m)
        {
            nn = (n);
            mm = (m);
            v = (n > 0 ? new T[n][] : null);
            if (v != null)
                for (int i = 0; i < n; i++) v[i] = new T[m];
        }



        // public NRmatrix(int n, int m, const T &a);	//Initialize to constant

        public NRmatrix(int n, int m, T a)
        {

            nn = (n);

            mm = (m);

            v = (n > 0 ? new T[n][] : null);


            if (v != null)
            {
                for (int i = 0; i < n; i++)
                {
                    v[i] = new T[m];
                    for (int j = 0; j < m; j++)
                        v[i][j] = a;
                }
            }
        }

        // public NRmatrix(const NRmatrix &rhs);		// Copy constructor

        public NRmatrix(M rhs)
        {

            nn = (rhs.nn);

            mm = (rhs.mm);

            v = (nn > 0 ? new T[nn][] : null);



            /*SKM

            int i,j,nel=mm*nn;

            if (v != null) v[0] = nel>0 ? new T[nel] : null;

            for (i=1; i< nn; i++) v[i] = v[i-1] + mm;

            for (i=0; i< nn; i++) for (j=0; j<mm; j++) v[i][j] = rhs[i][j];

            */

            if (v != null)
            {

               for (int i = 0; i < nn; i++)

                    v[i] = new T[mm];

                for (int i = 0; i < nn; i++)

                    System.Array.Copy(rhs[i], 0, v[i], 0, mm);

            }

        }



        //SKM public typedef T value_type; // make T available externally



        /*SKM

        // public NRmatrix & operator=(const NRmatrix &rhs);	//assignment

        public NRmatrix<T> & NRmatrix<T>::operator=(const NRmatrix<T> &rhs)

        // postcondition: normal assignment via copying has been performed;

        //		if matrix and rhs were different sizes, matrix

        //		has been resized to match the size of rhs

        {

        	if (this != &rhs) {

        		int i,j,nel;

        		if (nn != rhs.nn || mm != rhs.mm) {

        			if (v != null) {

        				delete[] (v[0]);

        				delete[] (v);

        			}

        			nn=rhs.nn;

        			mm=rhs.mm;

        			v = nn>0 ? new T*[nn] : null;

        			nel = mm*nn;

        			if (v) v[0] = nel>0 ? new T[nel] : null;

        			for (i=1; i< nn; i++) v[i] = v[i-1] + mm;

        		}

        		for (i=0; i< nn; i++) for (j=0; j<mm; j++) v[i][j] = rhs[i][j];

        	}

        	return *this;

        }

            */



        // public inline T* operator[](const int i);	//subscripting: pointer to row i

        public T[] this[int i]	//subscripting: pointer to row i
        {

            get { return v[i]; }

        }



        /*SKM

        // public inline const T* operator[](const int i) const;

        inline const T* NRmatrix<T>::operator[](const int i) const

        {

        	return v[i];

        }

        */



        // public inline int nrows() const;

        public int nrows()
        {

            return nn;

        }



        //public inline int ncols() const;

        public int ncols()
        {

            return mm;

        }



        //public void resize(int newn, int newm); // resize (contents not preserved)

        public void resize(int newn, int newm)
        {

            //SKM int i,nel;

            if (newn != nn || newm != mm)
            {
                nn = newn;

                mm = newm;

                v = nn > 0 ? new T[nn][] : null;

                if (v != null)
                {
                    for (int i = 0; i < nn; i++)
                        v[i] = new T[mm];
                }
            }
        }
        // public void assign(int newn, int newm, const T &a); // resize and assign a constant value

        public void assign(int newn, int newm, T a)
        {
            //SKM int i,j,nel;
            if (newn != nn || newm != mm)
            {
                nn = newn;
                mm = newm;
                v = nn > 0 ? new T[nn][] : null;
                if (v != null)
                {

                    for (int i = 0; i < nn; i++)

                        v[i] = new T[mm];

                }

            }
            for (int i = 0; i < nn; i++) for (int j = 0; j < mm; j++) v[i][j] = a;
        }
    }



    public class NRMat3d<T>
    {
        private int nn;
        private int mm;
        private int kk;
        private T[][][] v;
        // public NRMat3d();
        public NRMat3d()
        {
            nn = (0);
            mm = (0);
            kk = (0);
            v = (null);
        }
        // public NRMat3d(int n, int m, int k);
        public NRMat3d(int n, int m, int k)
        {
            nn = (n);
            mm = (m);
            kk = (k);
            v = (new T[n][][]);
            for (int i = 0; i < nn; i++)
            {
                v[i] = new T[mm][];
                for (int j = 0; j < mm; j++)
                {
                    v[i][j] = new T[kk];
                }
            }
        }
        // public inline T** operator[](const int i);	//subscripting: pointer to row i

        public T[][] this[int i] //subscripting: pointer to row i
        {

            get { return v[i]; }

        }
        public int dim1()
        {

            return nn;

        }
        // public inline int dim2() const;

        public int dim2()
        {

            return mm;

        }
        //public inline int dim3() const;

        public int dim3()
        {
            return kk;
        }
    }



    // vector types



    public class VecInt : NRvector<int, VecInt>
    {

        public VecInt() : base() { }

        public VecInt(int n) : base(n) { }

        public VecInt(int n, int a) : base(n, a) { }

        public VecInt(int n, int[] a, int begin) : base(n, a, begin) { }

        public VecInt(int[] a) : base(a.Length, a, 0) { }

        public VecInt(VecInt rhs) : base(rhs) { }

    }



    public class VecLong : NRvector<long, VecLong>
    {

        public VecLong() : base() { }

        public VecLong(int n) : base(n) { }

        public VecLong(int n, int a) : base(n, a) { }

        public VecLong(int n, long[] a, int begin) : base(n, a, begin) { }

        public VecLong(long[] a) : base(a.Length, a, 0) { }

        public VecLong(VecLong rhs) : base(rhs) { }

    }



    public class VecDoub : NRvector<double, VecDoub>
    {

        public VecDoub() : base() { }

        public VecDoub(int n) : base(n) { }

        public VecDoub(int n, double a) : base(n, a) { }

        public VecDoub(int n, double[] a, int begin) : base(n, a, begin) { }

        public VecDoub(double[] a) : base(a.Length, a, 0) { }

        public VecDoub(VecDoub rhs) : base(rhs) { }

        public VecDoub minus(VecDoub x)
        {
            if (size() != x.size())
                throw new ArgumentException();
            int n = size();
            VecDoub result = new VecDoub(n);
            for (int i = 0; i < n; i++)
                result[i] = this[i] - x[i];
            return result;
        }
        public VecDoub plus(VecDoub x)
        {
            if (size() != x.size())
                throw new ArgumentException();
            int n = size();
            VecDoub result = new VecDoub(n);
            for (int i = 0; i < n; i++)
                result[i] = this[i] + x[i];

            return result;
        }
        public VecDoub times(double x)
        {
            int n = size();
            VecDoub result = new VecDoub(n);
            for (int i = 0; i < n; i++)
                result[i] = this[i] * x;
            return result;
        }

        public static VecDoub random(VecDoub range)
        {
            int n = range.size();
            VecDoub result = new VecDoub(n);
            for (int i = 0; i < n; i++)
                result[i] = rand.NextDouble() * range[i];
            return result;
        }
    }
    public class VecComplex : NRvector<Complex, VecComplex>
    {
        public VecComplex() : base() { }
        public VecComplex(int n) : base(n) { }
        public VecComplex(int n, Complex a) : base(n, a) { }
        public VecComplex(int n, Complex[] a, int begin) : base(n, a, begin) { }
        public VecComplex(VecComplex rhs) : base(rhs) { }
    }
    public class MatInt : NRmatrix<int, MatInt>
    {
        public MatInt() : base() { }
        public MatInt(int n, int m) : base(n, m) { }
        public MatInt(int n, int m, int a) : base(n, m, a) { }
        public MatInt(MatInt rhs) : base(rhs) { }
    }
    public class MatUint : NRmatrix<uint, MatUint>
    {

        public MatUint() : base() { }

        public MatUint(int n, int m) : base(n, m) { }

        public MatUint(int n, int m, uint a) : base(n, m, a) { }

        public MatUint(MatUint rhs) : base(rhs) { }

    }
    public class MatLlong : NRmatrix<long, MatLlong>
    {

        public MatLlong() : base() { }

        public MatLlong(int n, int m) : base(n, m) { }

        public MatLlong(int n, int m, long a) : base(n, m, a) { }

        public MatLlong(MatLlong rhs) : base(rhs) { }

    }
    public class MatUllong : NRmatrix<ulong, MatUllong>
    {

    }
    public class MatDoub : NRmatrix<double, MatDoub>
    {
        public MatDoub() : base() { }
        public MatDoub(int n, int m) : base(n, m) { }
        public MatDoub(int n, int m, double a) : base(n, m, a) { }
        public MatDoub(MatDoub rhs) : base(rhs) { }
    }
}

