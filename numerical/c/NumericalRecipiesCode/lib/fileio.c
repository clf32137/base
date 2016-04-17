#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int read_matrix_from_file(float** mat, char* filename, int rows, int cols)
{
	FILE *file;
	char *buffer;
	int ret, row = 0, i, j;

	// Set Field Separator here
	char delims[] = " ";
	char *result = NULL;
	// Memory allocation
	if ((file = fopen(filename, "r")) == NULL){
		fprintf(stdout, "Error: Can't open file !\n");
		return -1;
	}
	while(!feof(file))
	{
		//buffer = static_cast<char*>(malloc(sizeof(char) * 4096));
		buffer = (char*) malloc (sizeof(char)*4096);
		memset(buffer, 0, 4096);
		ret = fscanf(file, "%4095[^\n]\n", buffer);
		if (ret != EOF && row < rows) 
		{
			int field = 0;
			result = strtok(buffer,delims);
			while(result!=NULL)
			{
				 // Set no of fields according to your requirement
				if(field>cols)break;
				mat[row+1][field+1] = atof(result);
				result = strtok(NULL,delims);
				field++;
			}
			++row;
		}
		free(buffer);
	}
	fclose(file);
	return -1;
 }