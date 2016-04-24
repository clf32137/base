######################
# Simulate a set of points inside a cube based on the condition
# in line 31.
######################


# -*- coding: utf-8 -*-
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
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

pos_samples = 0
for i in xrange(5000):
    x=np.random.uniform(0,1,1)
    y=np.random.uniform(0,1,1)
    z=np.random.uniform(0,1,1)
    if x > y and y > z and x > z:
    #if x+y+z<1:
        pos_samples = pos_samples + 1
        ax.scatter(x,y,z,color="r", s=10)

print float(pos_samples)/5000

#draw a vector

plt.show()
