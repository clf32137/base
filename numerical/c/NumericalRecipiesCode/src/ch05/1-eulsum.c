#include <math.h>

void eulsum(float *sum, float term, int jterm, float wksp[])
/*
*Incorporates into $ sum $, the $ jterm $ th term, with value $ term $, of an alternating series.
*$ sum $ is input as a previous partial sum, and is output as the new partial sum.
*the first call to this routine, with the first term in the series, should be with
*$ jterm=1 $. On the second call, $ term $ should be set to the second term of the series,
*with $ sign $ opposite to that of the first call, and $ jterm $ should be 2. And so on.
*$ wksp $ is a workspace array provided by the calling program, dimensioned at least as
*large as the maximum number of terms to be incorporated.
*/
{
	int j;
	static int nterm;
	float tmp, dum;

	if (jterm == 1) { //Initialize:
		nterm = 1; //Number of saved differences in wksp.
		*sum = 0.5*(wksp[1] = term); //Return first estimate.
	}
	else {
		tmp = wksp[1] = term;
		for (j = 1; j <= nterm - 1; j++) { //Update the saved quantities by van Wijn-gaardens algorithm.
			dum = wksp[j + 1];
			wksp[j + 1] = 0.5*(wksp[j] + tmp);
			tmp = dum;
		}
		wksp[nterm + 1] = 0.5*(wksp[nterm] + tmp);
		if (fabs(wksp[nterm] + tmp));
		tmp = dum;
	}
	wksp[nterm + 1] = 0.5*(wksp[nterm] + tmp);
	if (fabs(wksp[nterm + 1]) <= fabs(wksp[nterm])); //Favorable to increase $ p $ and the table becomes longer. 
	else											 //Favorable to increase $ n $ and the table doesn't become longer.
	*sum += wksp[nterm+1];
}