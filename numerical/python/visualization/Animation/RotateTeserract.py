from PIL import Image, ImageDraw
from colour import Color
import numpy as np
from HyperCube import *

edges = generate_edges(4)['edges']

for j in range(0,100):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im)

    theta = j/100.0 * np.pi*2
    phi = j/100.0 * np.pi*2
    alp = j/100.0 * np.pi*2
    beta = (j/100.0 - 0/100.0) * np.pi*2
    gamma = (j/100.0 - 0/100.0) * np.pi*2
    delta = (j/100.0 - 0/100.0) * np.pi*2
    [r1,r2,r3,r4,r5,r6] = rotation_matrix(theta,phi,alp,beta,gamma,delta)

    if j < 0:
        r = np.dot(r3,np.dot(r1,r2))
    else:
        r = np.dot(r6,np.dot(r5,np.dot(r4,np.dot(r3,np.dot(r1,r2)))))
        #r = np.dot(r4,np.dot(r3,np.dot(r1,r2)))
    ind = 0
    for e in edges:
        v1 = np.dot(r, e[0])
        v2 = np.dot(r, e[1])
        [v1x,v1y] = 1000 + 500 * v1[0:2]
        [v2x,v2y] = 1000 + 500 * v2[0:2]
        #if is_inside_teserract(r, v1 - np.array([0,0,0.5,0.5]) ) or is_inside_teserract(r, v2 - np.array([0,0,0.5,0.5])):
        if is_inside(r, v1 - np.array([0,0,0.5,0.5])) or is_inside(r, v2 - np.array([0,0,0.5,0.5])):
            width = 3
        else:
            width = 3
        if ind < 8:
            draw.line((v1x, v1y, v2x, v2y), fill='green', width=width)
        else:
            draw.line((v1x, v1y, v2x, v2y), fill='orange', width=width)
        ind = ind + 1

    im.save('Images\\RotatingCube\\im' + str(j) + '.bmp')


vertices = generate_edges(4)['vertices']
#rotate
rotated_vertices = np.transpose(np.dot(r,np.transpose(vertices)))
#displace
ver1 = [v - np.array([0,0,0,0.5]) for v in rotated_vertices]
#rotate back
ver_rotated = np.transpose(np.dot(np.transpose(r),np.transpose(ver1)))

