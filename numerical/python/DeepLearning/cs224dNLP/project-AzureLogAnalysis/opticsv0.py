##########################################################################
# Ordering objects of a data set to obtain the clustering structure 
##########################################################################
# Input: 
# X - data set (m,n); m-points, n-features
# k - number of objects in a neighborhood of the selected object
# (minimal number of objects considered as a cluster)
##########################################################################
# Output: 
# RD - vector with reachability distances (size m)
# CD - vector with core distances (size m)
# order - vector specifying the order of objects (size m)
##########################################################################
# Example of use:
# x=[randn(30,2)*.4;randn(40,2)*.5+ones(40,1)*[4 4]];
# [RD,CD,order]=optics(x)
##########################################################################


import numpy as np
import math
from scipy import spatial
import matplotlib.pyplot as plt

# Calculates the distances between the i-th object and all objects in x
# Input: 
# i - an object (1,n)
# x - data matrix (m,n); m-objects, n-variables
# Output - an array D of distances from i to each row of X

def dist(i,x):
    D = []
    for j in x:
        #We use cosine here as it is appropriate for binary vectors
        D.append(spatial.distance.cityblock(i,j))
        #D.append(spatial.distance.euclidean(i,j))
    return np.array(D)


##########################################################################
# Now begins the Optics algorithm
##########################################################################

def optics(X, k = 30):
    (m,n)=X.shape

    CD=np.zeros(m);
    RD=np.array(pow(np.ones(m)*10,10))

    # Calculate Core Distances
    for i in range(m):
        D=np.sort(dist(X[i],X))
        CD[i]=D[k+1]

    order=[]
    seeds=np.array(range(m))
    ind=0

    while len(seeds)>0:
        ob=seeds[ind]
        seeds = np.delete(seeds,ind)
        order.append(ob)
        dd = dist(X[ob],X[seeds])
        mm = [max(j,CD[ob]) for j in dd]
        mm = np.array(mm)
        ii = RD[seeds]>mm
        RD[seeds[ii]]=mm[ii]
        try:
            ind=np.argmin(RD[seeds])
        except:
            dummy = 'dummy'

    RD[0]=max(RD[1:m])+.1*max(RD[1:m])
    plt.plot(range(len(RD)),RD[order])
    plt.show()

if __name__ == "__main__":
    #Test on some random data.
    mean = [0,0]
    cov = [[1,0],[0,1]]
    x,y = np.random.multivariate_normal(mean,cov,100).T
    mean = [5,5]
    cov = [[1,0],[0,1]]
    x1,y1 = np.random.multivariate_normal(mean,cov,100).T
    x = np.concatenate((x,x1), axis=0)
    y = np.concatenate((y,y1), axis=0)
    plt.plot(x, y, 'x')
    plt.axis('equal')
    plt.show()
    X = np.vstack((x,y)).T
    optics(X)

##########################################################################
# References: 
# [0] This code in Matlab/Octave - http://chemometria.us.edu.pl/download/OPTICS.M
# [1] M. Ankrest, M. Breunig, H. Kriegel, J. Sander - OPTICS: Ordering Points To Identify the Clustering Structure, 
# available from www.dbs.informatik.uni-muenchen.de/cgi-bin/papers?query=--CO
# [2] M. Daszykowski, B. Walczak, D.L. Massart, Looking for natural patterns in analytical data. Part 2. Tracing local density
# with OPTICS, J. Chem. Inf. Comput. Sci. 42 (2002) 500-507
##########################################################################

