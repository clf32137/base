######################
# Plot a set of points inside a simplex within a cube.
######################


# -*- coding: utf-8 -*-
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

from numpy import sin, cos
import scipy.integrate as integrate
import matplotlib.animation as animation


class Cubes:
    def __init__(self, idx = 0):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_aspect("equal")
        #draw cube
        r = [0, 1]
        for s, e in combinations(np.array(list(product(r,r,r))), 2):
            if np.sum(np.abs(s-e)) == r[1]-r[0]:
                ax.plot3D(*zip(s,e), color="g")

        #draw the origin
        ax.scatter([0],[0],[0],color="g",s=100)

        transform_matrix = np.array([np.array([1,0,0]),np.array([1,1,0]),np.array([1,1,1])])
        pos_samples = 0
        for i in xrange(5000):
            x=np.random.uniform(0,1,1)
            y=np.random.uniform(0,1,1)
            z=np.random.uniform(0,1,1)
            #if x > y and y > z:
            if x+y+z < 1 and x+y+z > .9:
                pos_samples = pos_samples + 1
                #ax.scatter(x,y,z,color="r", s=10, alpha=.5)
                trnsfm = transform_matrix.dot(np.array([x[0],y[0],z[0]]))
                #ax.scatter(x,y,z,color="y",s=20,alpha=.5)
                #alph = 1/(x+y+z)
                ax.scatter(trnsfm[0],trnsfm[1],trnsfm[2],color="y",s=20,alpha=.5)
            if z-y > 0 and z-y < 0.1 and y-x > 0 and y-z < 0.1:
                ax.scatter(x, y, z, color="b", s=10)
            elif z>y and y>x:
                ax.scatter(x, y, z, color="b", s=10, alpha = .1)

        print float(pos_samples)/5000
        ax.view_init(50 + idx, 50+idx)
        plt.savefig("RotatingCube/movie" + str(idx) +".png")


if __name__ == "__main__":
    for i in range(10):
        c = Cubes(i)

