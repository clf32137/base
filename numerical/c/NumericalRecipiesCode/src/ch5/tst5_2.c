#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include "../../include/nrutil.h"
#include "../../include/fileio.h"

int main(int argc, char *argv[])
{
	//Used to determine which section gets its results printed.
	
		float c[] = {1,1,1,0,0};
		int nc = 2;
		float x = 2.0;
		float pd[] = {0,0,0,0,0};
		int nd = 3;
		printf("x outside: %f\n",x);
		ddpoly2(x);
}


