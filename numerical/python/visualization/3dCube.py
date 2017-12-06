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
    def __init__(self, idx = 0, show = True):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_aspect("equal")
        #draw cube
        r = [0, 1]
        for s, e in combinations(np.array(list(product(r,r,r))), 2):
            if np.sum(np.abs(s-e)) == r[1]-r[0]:
                ax.plot3D(*zip(s,e), color="g")
                ax.plot3D(*zip(s+1,e+1), color="r")

        #draw the origin
        ax.scatter([0],[0],[0],color="g",s=100)

        transform_matrix = np.array([np.array([1,0,0]),np.array([1,1,0]),np.array([1,1,1])])
        pos_samples = 0
        for i in xrange(500):
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

        print float(pos_samples)/500
        ax.view_init(40 + idx, 30 + idx)
        if show:
            plt.show()
        else:
            plt.savefig("RotatingCube/movie" + str(idx) + ".png")


class PointToLine():
    def __init__(self, idx = 0, show = True, frames = 10, extendUntil = 0.5, step = 0):
        self.frames = frames
        self.i = idx
        self.extendUntil = extendUntil
        self.show = show
        self.step = step
        
        fig = plt.figure()
        #ax = fig.gca(projection='3d')
        #ax.set_aspect("equal")
        if step == 0:
            self.Point2Line()
        elif step == 1:
            self.Line2Square()
        else:
            self.Square2Cube()

        self.SetFrameProperties()
        self.ShowFigure()
        plt.close()

    def Point2Line(self, idx = 0, x1 = 0, x2 = -1, y1 = 0, y2 = 0):
        if x2 == -1:
            x2 = self.extendUntil
        plt.scatter(x1, y1)
        plt.scatter(x2, y2)
        if idx == 0: # Just plot the whole thing.
            frac = float(self.i)/self.frames
        else: # Plot the partial line.
            frac = float(idx)/self.frames

        plt.plot([x1, x2 * frac], [y1, y2], 'k-', lw=2)

    def Line2Square(self):
        plt.scatter(0, self.extendUntil)
        plt.scatter(self.extendUntil, self.extendUntil)
        
        self.Point2Line(self.frames)
        self.Point2Line(self.frames, 0, self.extendUntil, self.extendUntil, self.extendUntil)
        plt.plot([0, 0], [0, self.extendUntil * (float(self.i)/self.frames)], 'k-', lw=2)
        plt.plot([self.extendUntil, self.extendUntil], [0, self.extendUntil * (float(self.i)/self.frames)], 'k-', lw=2)

    def SetFrameProperties(self):
        frame1 = plt.gca()
        frame1.axes.get_xaxis().set_visible(False)
        frame1.axes.get_yaxis().set_visible(False)
        frame1.set_xlim(-1, 1)
        frame1.set_ylim(-1, 1)

    def ShowFigure(self):
        if self.show:
            plt.show()
        else:
            plt.savefig("YouTuVids/movie" + str(self.step * self.frames + self.i) + ".png")


if __name__ == "__main__":
    for i in range(16):
        #c = Cubes(i,False)
        for j in range(2):
            PointToLine(i, False, 15, 0.5, j)


'''
i = 3
frames = 15

fig = plt.figure()
plt.scatter(0, 0)
plt.plot([0, float(i)/frames], [0, 0], 'k-', lw=2)
plt.scatter(0, self.extendUntil)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
frame1.set_xlim(-1, 1)
frame1.set_ylim(-1, 1)
plt.show()
'''

