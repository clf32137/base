#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../../include/nrutil.h"
#include "../../include/fileio.h"
#include "../../include/general_fns.h"
#include "ch7funcs.h"

int main(int argc, char *argv[])
{
	unsigned long *iseed;
	int randBit = irbit2(&iseed);
	printf("%d", randBit);
}
