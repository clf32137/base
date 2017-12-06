#define IB1 1
#define IB2 2
#define IB5 16
#define IB18 131072
#define MASK IB1+IB2+IB5

int irbit2(unsigned long *iseed)
/*
*Returns as an integer a random but, based on the 18 low-significance bits in iseed (which is modified for the next call).
*/
{
	if (*iseed & IB18) 
	{
		*iseed=((*iseed ^ MASK) << 1) | IB1;
		return 1;
	} else 
	{
		*iseed <<= 1;
		return 0;
	}
}

#undef MASK
#undef IB18
#undef IB5
#undef IB2
#undef IB1

