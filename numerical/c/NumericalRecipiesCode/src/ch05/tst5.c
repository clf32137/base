#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include "../../include/nrutil.h"
#include "../../include/fileio.h"
#include "../../include/general_fns.h"
#include "ch5funcs.h"


int main(int argc, char *argv[])
{
	//Used to determine which section gets its results printed.
	int shouldiprint[] = 
	{
		1, // polynomial evaluation
		1, //
		1, //
		1, //
		1, //
		1, //
		1, //
		1, //
		1, //
		1, //
		1, //
		1  //
	};
	int printindx = 0;
	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Evaluate polynomial and calculate its derivatives\n###################\n");
		float c[] = {1,1,1,1,0};
		int nc = 3;
		float x = 2.0;
		float pd[] = {0,0,0,0,0};
		int nd = 4;
		ddpoly_debug(c,nc,x,pd,nd);
		int i;
		for(i=0; i < nd; i++)
			printf("%f%s", pd[i], i < nd - 1 ? "\t" : "\n");
	}
	if(shouldiprint[printindx++])
	{
		printf("\n###################\n Divide two polynomials\n###################\n");
		float c1[] = {1,1,1,1,0};
		int nc1 = 3;
		
	}
}


