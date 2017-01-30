using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ProgrIntervExposed.Arrays
{
    class ArraysStrings
    {
        
        /// <summary>
        /// Cumulative sum of a 2-d array from (0,0)
        /// </summary>
        /// <param name="input">The double array for which cumulative sums are to be caculated.</param>
        public static void CumulativeSum(double[,] input)
        {
            for (int i = 0; i < input.GetLength(0); i++)
            {
                for (int j = 0; j < input.GetLength(1); j++)
                {
                    input[i, j] = input[i,j] + 
                        (i < 1 ? 0 : input[i - 1, j]) + (j < 1 ? 0 : input[i, j - 1]) - ((i < 1 || j < 1) ? 0 : input[i - 1, j - 1]);
                }
            }
        }

        /// <summary>
        /// Given a 2-d array of numbers. The cost of going from one cell of the array to the adjecent right or bottom 
        /// cell is the difference between the source cell and destination cell. This function uses dynamic programming
        /// to find the minimal cost of going from the top left of the matrix to the bottom right.
        /// </summary>
        /// <param name="input">The array that holds the costs of moving.</param>
        public static double[,] OptimalPath(double[,] input)
        {
            double[,] optimalPaths = new double[input.GetLength(0), input.GetLength(1)];
            double option1, option2;
            
            for (int i = 0; i < input.GetLength(0); i++)
            {
                for (int j = 0; j < input.GetLength(1); j++)
                {
                    if (i >= 1)
                    {
                        option1 = (optimalPaths[i - 1, j] - input[i - 1, j] + input[i, j]);
                        optimalPaths[i, j] = option1;
                    }

                    if (j >= 1)
                    {
                        option2 = (optimalPaths[i, j - 1] - input[i, j - 1] + input[i, j]);
                        optimalPaths[i, j] = (i > 1 ? Math.Min(optimalPaths[i, j], option2) : option2);
                        // If we store a boolean argmin as well in a 2-d array, then we can decipher the actual optimal path.
                    }
                }
            }

            return optimalPaths;
        }

        /// <summary>
        /// Removes duplicates from a string.
        /// </summary>
        /// <param name="str">The input string from which duplicates are to be removed.</param>
        public static void removeDuplicates(char[] str)
        {
            if (str == null) return;
            int len = str.Length;
            if (len < 2) return;
            int tail = 1;
            for (int i = 1; i < len; ++i)
            {
                int j;
                for (j = 0; j < tail; ++j)
                {
                    if (str[i] == str[j]) break;
                }
                if (j == tail)
                {
                    str[tail] = str[i];
                    ++tail;
                }
            }

            str[tail] = '0';
        }

        /// <summary>
        /// Remove duplicates from a string when we can use a constant sized buffer.
        /// </summary>
        /// <param name="str"></param>
        public static void removeDuplicatesEff(char[] str)
        {
            if (str == null) return;
            int len = str.Length;
            if (len < 2) return;
            bool[] hit = new bool[256];
            for (int i = 0; i < 256; ++i)
            {
                hit[i] = false;
            }
            hit[str[0]] = true;
            int tail = 1;
            for (int i = 1; i < len; ++i)
            {
                if (!hit[str[i]])
                {
                    str[tail] = str[i];
                    ++tail;
                    hit[str[i]] = true;
                }
            }
            str[tail] = '0';
        }

        /// <summary>
        /// Prints out all paths going from the top right of a grid to the bottom left.
        /// </summary>
        /// <param name="x">The left-most coordinate. We go from here to 0 horizontally.</param>
        /// <param name="y">The top-most coordinate. We go from here to 0 vertically.</param>
        /// <param name="path">A string builder that contains all the paths.</param>
        public static void ListAllPaths(int x, int y, StringBuilder path)
        {
            if (x == 0 && y == 0)
            {
                Console.Out.WriteLine(path);
            }
            else if (x > 0 && y == 0)
            {
                path.Append("R");
                ListAllPaths(x - 1, y, path);
                path.Length--;
            }
            else if (x == 0 && y > 0)
            {
                path.Append("D");
                ListAllPaths(x, y - 1, path);
                path.Length--;
            }
            else if (x > 0 && y > 0)
            {
                path.Append("D");
                ListAllPaths(x, y - 1, path);
                path.Length--;
                path.Append("R");
                ListAllPaths(x -1, y, path);
                path.Length--;
            }
        }

        
        /// <summary>
        /// Searched a value over a matrix that is sorted by both rows and columns.
        /// </summary>
        /// <param name="mat">The matrix over which we should search.</param>
        /// <param name="elem">The element to be searched.</param>
        /// <param name="minrow">The minimum row defining the range over which the value is to be searched.</param>
        /// <param name="maxrow">The maximum row defining the range over which the value us to be searched.</param>
        /// <param name="mincol">The minimum column defining the range over which the value is to be searched.</param>
        /// <param name="maxcol">The maximum column defining the range over which the value is to be searched.</param>
        /// <returns>A tuple with two integers defining the index at which the element was found. If the elelemt was not found, (-1,-1) is returned.</returns>
        public static Tuple<int, int> ElementSearch2D
        (
            int[,] mat, int elem,
            int minrow, int maxrow,
            int mincol, int maxcol
        )
        {
            if (elem <= mat[minrow, mincol])
            {
                return (elem == mat[minrow, mincol]? Tuple.Create(minrow,mincol):Tuple.Create(-1, -1));
            }

            if (elem >= mat[maxrow, maxcol])
            {
                return (elem == mat[maxrow, maxcol] ? Tuple.Create(maxrow, maxcol) : Tuple.Create(-1, -1));
            }

            if (minrow >= maxrow && mincol >= maxcol)
            {
                if (mat[minrow, mincol] == elem)
                {
                    return Tuple.Create(minrow, mincol);
                }
                else
                {
                    return Tuple.Create(-1, -1);
                }
            }
            
            else if (minrow == maxrow)
            {
                int binarySearch = BinarySearch(mat, elem, minrow, true, mincol, maxcol);
                if (binarySearch > -1)
                {
                    return Tuple.Create(minrow, binarySearch);
                }
                else
                {
                    return Tuple.Create(-1, -1);
                }
            }
            else if (mincol == maxcol)
            {
                int binarySearch = BinarySearch(mat, elem, mincol, false, minrow, maxrow);
                if (binarySearch > -1)
                {
                    return Tuple.Create(binarySearch, mincol);
                }
                else
                {
                    return Tuple.Create(-1, -1);
                }
            }

            int rowslice = (minrow + maxrow) / 2;
            int colslice = (mincol + maxcol) / 2;

            if (mat[rowslice, colslice] == elem)
            {
                return Tuple.Create(rowslice, colslice);
            }
            else if (mat[rowslice, colslice] < elem)
            {
                // Split into two rectangles.
                if (mincol < maxcol && minrow <= maxrow)
                {
                    Tuple<int, int> rightSearch = ElementSearch2D(mat, elem, Math.Min(rowslice + 1, mat.GetLength(0) - 1), maxrow, 0, maxcol);
                    //Tuple<int, int> rightSearch = ElementSearch2D(mat, elem, rowslice + 1, maxrow, 0, maxcol);
                    if (rightSearch.Item1 > -1)
                    {
                        return rightSearch;
                    }
                }
                if (minrow < maxrow && mincol <= maxcol)
                {
                    Tuple<int, int> bottomSearch = ElementSearch2D(mat, elem, 0, rowslice, Math.Min(colslice + 1, mat.GetLength(1) - 1), maxcol);
                    if (bottomSearch.Item1 > -1)
                    {
                        return bottomSearch;
                    }
                }
            }
            else
            {
                // Split into two rectangles.
                if (mincol < maxcol && minrow <= maxrow)
                {
                    Tuple<int, int> leftSearch = ElementSearch2D(mat, elem, 0, Math.Max(rowslice - 1, 0), 0, maxcol);
                    if (leftSearch.Item1 > -1)
                    {
                        return leftSearch;
                    }
                }
                if (minrow < maxrow && mincol <= maxcol)
                {
                    Tuple<int, int> topSearch = ElementSearch2D(mat, elem, rowslice, maxrow, 0, Math.Max(colslice - 1, 0));
                    if (topSearch.Item1 > -1)
                    {
                        return topSearch;
                    }
                }
            }

            return Tuple.Create(-1, -1);
        }

        private static int BinarySearch(int[,] mat, int elem, int indx, bool searchrow, int start, int end)
        {
            if (searchrow)
            {
                if (start >= end)
                {
                    if (mat[indx, start] == elem)
                    {
                        return start;
                    }
                    else if (end >=0 && mat[indx, end] == elem)
                    {
                        return end;
                    }
                    else
                    {
                        return -1;
                    }
                }
                int searchIndx = (start + end) / 2;
                if (elem > mat[indx, searchIndx])
                {
                    return BinarySearch(mat, elem, indx, true, searchIndx + 1, end);
                }
                else if (elem < mat[indx, searchIndx])
                {
                    return BinarySearch(mat, elem, indx, true, 0, searchIndx - 1);
                }
                else
                {
                    return searchIndx;
                }
            }
            else
            {
                if (start >= end)
                {
                    if (mat[start, indx] == elem)
                    {
                        return start;
                    }
                    else if (end >= 0 && mat[end, indx] == elem)
                    {
                        return end;
                    }
                    else
                    {
                        return -1;
                    }
                }
                int searchIndx = (start + end) / 2;
                if (elem > mat[searchIndx, indx])
                {
                    return BinarySearch(mat, elem, indx, false, searchIndx + 1, end);
                }
                else if (elem < mat[searchIndx, indx])
                {
                    return BinarySearch(mat, elem, indx, false, 0, searchIndx - 1);
                }
                else
                {
                    return searchIndx;
                }
            }
        }

        public class AnagramComparator : Comparer<string>
        {
            public override int Compare(string x, string y)
            {
                return SortChars(x).CompareTo(SortChars(y));
            }

            public string SortChars(string s)
            {
                char[] content = s.ToCharArray();
                Array.Sort(content);
                return content.ToString();
            }
        }

        public class GenericArray<T> where T : IComparable
        {
            public static void MergeSort(T[] arr, int start, int end)
            {
                if (end <= start)
                {
                    return;
                }

                int mid = (int)((end + start) / 2);

                MergeSort(arr, start, mid);
                MergeSort(arr, mid+1, end);
                Merge(arr, start, mid+1, end);
            }

            private static void Merge(T[] arr, int start, int mid, int end)
            {
                T[] final = new T[end - start + 1];
                int firstCounter = start, secondCounter = mid, index = 0;

                while (firstCounter <= (mid - 1) || secondCounter <= end)
                {
                    if (secondCounter > end)
                    {
                        final[index++] = arr[firstCounter++];
                    }
                    else if (firstCounter > mid - 1)
                    {
                        final[index++] = arr[secondCounter++];
                    }
                    else if (arr[firstCounter].CompareTo(arr[secondCounter]) > 0)
                    {
                        final[index++] = arr[secondCounter++];
                    }
                    else
                    {
                        final[index++] = arr[firstCounter++];
                    }
                }

                for (int i = start; i <= end; i++)
                {
                    arr[i] = final[i - start];
                }
            }
        }
    }
}
