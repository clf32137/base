//extern unsigned long ija[];
//extern double dsa[];

void atimes(unsigned long ija[], double dsa[], unsigned long n, double x[], double r[], int itrnsp)
{
	void dsprsax(double dsa[], unsigned long ija[], double x[], double b[], unsigned long n);

	void dsprstx(double dsa[], unsigned long ija[], double x[], double b[], unsigned long n);

	if (itrnsp) dsprstx(dsa,ija,x,r,n);
	else dsprsax(dsa,ija,x,r,n);
}