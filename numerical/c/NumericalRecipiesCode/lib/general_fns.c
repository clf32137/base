#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define ANSI_COLOR_BLACK "\033[22;30m"// - black
//#define ANSI_COLOR_RED "\033[22;31m"// - red
//#define ANSI_COLOR_GREEN "\033[22;32m"// - green
#define ANSI_COLOR_BROWN "\033[22;33m"// - brown
//#define ANSI_COLOR_BLUE "\033[22;34m"// - blue
//#define ANSI_COLOR_MAGENTA "\033[22;35m"// - magenta
//#define ANSI_COLOR_CYAN "\033[22;36m"// - cyan
#define ANSI_COLOR_GRAY "\033[22;37m"// - gray
#define ANSI_COLOR_DARKGRAY "\033[01;30m"// - dark gray
#define ANSI_COLOR_LIGHTRED "\033[01;31m"// - light red
#define ANSI_COLOR_LIGHTGREEN "\033[01;32m"// - light green
//#define ANSI_COLOR_YELLOW "\033[01;33m"// - yellow
#define ANSI_COLOR_LIGHTBLUE "\033[01;34m"// - light blue
#define ANSI_COLOR_LIGHTMAGENTA "\033[01;35m"// - light magenta
#define ANSI_COLOR_LIGHTCYAN "\033[01;36m"// - light cyan
#define ANSI_COLOR_WHITE "\033[01;37m"// - white

#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_GREEN   "\x1b[32m"
#define ANSI_COLOR_YELLOW  "\x1b[33m"
#define ANSI_COLOR_BLUE    "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN    "\x1b[36m"
#define ANSI_COLOR_RESET   "\x1b[0m"

void pprint1d_float(float *a, int n)
{ 
	int k;
	for(k=0; k < n; k++)
		printf(ANSI_COLOR_MAGENTA "%.2f%s", a[k], k < n - 1 ? "\t" : "\n" ANSI_COLOR_RESET);
}

void pprint2d_float(float **a, int ros, int cols)
{
	int i, j;
	for (i = 0; i<ros; i++)
		for (j = 0; j<cols; j++)
			printf("%lf%s", a[i + 1][j + 1], j < cols - 1 ? "\t" : "\n");
	printf("\n");
}
