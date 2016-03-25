#include <stdio.h>
#include <math.h>
#define ZON -5.0 //Time zone−5 is Eastern Standard Time.
#define IYBEG 1900 //The range of dates to be searched.
#define IYEND 2100

int main(void) /* Program badluk */ 
{ 
	void flmoon(int n, int nph, long *jd, float *frac);
	long julday(int mm, int id, int iyyy);
	int ic,icon,idwk,im,iyyy,n;
	float timzon = ZON/24.0,frac;
	long jd,jday;
	printf("\nFull moons on Friday the 13th from %5d to %5d\n",IYBEG,IYEND);
	
	for (iyyy=IYBEG;iyyy<=IYEND;iyyy++)
	{ //Loop over each year, 
		for (im=1;im<=12;im++)
		{ //and each month.
			jday=julday(im,13,iyyy); //Is the 13th a Friday? 
			idwk=(int) ((jday+1) % 7);
			if (idwk == 5)
			{
				n=(int)(12.37*(iyyy-1900+(im-0.5)/12.0)); //This value n is a ﬁrst approximation to how many full moons have occurred since 1900. We will feed it into the phase routine and adjust it up or down until we determine that our desired 13th was or was not a full moon. The variable icon signals the direction of adjustment. 
				icon=0;
				for (;;)
				{
					flmoon(n,2,&jd,&frac); //Get date of full moon n. 
					frac=24.0*(frac+timzon); //Convert to hours in correct time zone. 
					if (frac < 0.0)
					{ //Convert from Julian Days beginning at noon to civil days beginning at midnight. 
						--jd; frac += 24.0;
					}
					if (frac > 12.0)
					{
						++jd;
						frac -= 12.0;
					}
					else
						frac += 12.0;
					if (jd == jday)
					{ //Did we hit our target day? 
						printf("\n%2d/13/%4d\n",im,iyyy); 
						printf("%s %5.1f %s\n","Full moon",frac," hrs after midnight (EST)"); 
						break; //Part of the break-structure, a match. 
					}
					else
					{ //Didn’t hit it. 
						ic=(jday >= jd ? 1 : -1);
						if (ic == (-icon))
							break; //Another break, case of no match. 
						icon=ic;
						n += ic;
					}
				}
			}
		}
	}
	return 0;
}
