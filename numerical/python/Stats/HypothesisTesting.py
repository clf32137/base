import numpy as np
from scipy.stats import t

def pVal(mu1,mu2,s1,s2,n1,n2):
	se = np.sqrt(s1*s1/n1+s2*s2/n2)
	df = (s1**2/n1 + s2**2/n2)**2 / ( ((s1**2 / n1)**2 / (n1 - 1)) + ((s2**2 / n2)**2 / (n2 - 1)))
	tVal = (mu1 - mu2)/se
	return (1 - t.cdf(tVal,df))



