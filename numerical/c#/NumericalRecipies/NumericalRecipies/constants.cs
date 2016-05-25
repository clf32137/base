using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NumericalRecipies.ch06
{
    class constants
    {
        //A set of constants that will come in handy in evaluation of functions.
        public static double[] digamma_coeff = { -.83333333333333333e-1, .83333333333333333e-2,-.39682539682539683e-2,
                                            .41666666666666667e-2,-.75757575757575758e-2, .21092796092796093e-1,
                                            -.83333333333333333e-1, .4432598039215686    ,-.3053954330270122e+1, .125318899521531e+2 };
        public static double[] gammaln_coeff = {76.18009173,-86.50532033,24.01409822,
                                            -1.231739516,.120858003e-2,-.536382e-5};
        public static double theZeroThreshold_ = 1e-7;
        public static double log_of_2_ = .69314718;
        public static double theEulerConst_ = 0.5772156649;
        public static double pi = Math.PI;
    }
}
