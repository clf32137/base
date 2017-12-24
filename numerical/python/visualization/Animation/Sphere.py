import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
import sys
from CubeObjects import *

def sphere():
    im_ind = 0
    for j in range(30):
        r = rotation(3,2*np.pi*j/30.0)
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        for z in np.arange(-1,1,0.01):
            generalized_circle(draw, np.array([0,0,z]), np.array([0,0,1]), np.sqrt(1-z*z), r,scale=300)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1


def render_sphere(draw, r, scale=235.5, shift = np.array([1009, 998, 0])):
    pltcircle(shift[:2],scale,scale,draw)
    for i in range(4):
        c = np.cos(i*np.pi/8)
        s = np.sin(i*np.pi/8)
        yradius = r[1,1] * c * scale
        xradius = c * scale
        center = shift[:dim] + scale * np.dot(r, np.array([0,0,s]))
        pltcircle(center[:2], xradius, abs(yradius), draw)
        #v1 = shift[:dim] + scale * np.dot(r, np.array([-c,-c,s]))
        #v2 = shift[:dim] + scale * np.dot(r, np.array([c, c, s]))
        #draw.ellipse((v1[0],v1[1],v2[0],v2[1]), outline = "red")

def yzrotation(j):
    r = np.eye(3)
    theta = np.pi*j/20.0
    r[1,1] = np.cos(theta)
    r[1,2] = -np.sin(theta)
    r[2,1] = np.sin(theta)
    r[2,2] = np.cos(theta)
    return r

def pltcircle(center, xradius, yradius, draw):
    [topleftx, toplefty] = [center[0] - xradius, center[1] - yradius]
    [bottomrightx, bottomrighty] = [center[0] + xradius, center[1] + yradius]
    draw.ellipse((topleftx, toplefty, bottomrightx, bottomrighty), outline = "red")

'''
Returns a three dimensional rotation matrix given the axis to rotate about and the angle to rotate by.
args:
    a: The axis to rotate about
    theta: The angle to rotate by.
'''
def general_rotation(a, theta):
    c = np.cos(theta)
    s = np.sin(theta)
    a = a/sum(a**2)**0.5
    [ax,ay,az] = a[:3]
    return np.array(
        [
            [c + ax**2 * (1-c), ax*ay*(1-c) - az*s, ax*az*(1-c) + ay*s],
            [ay*ax*(1-c)+az*s, c + ay**2*(1-c), ay*az*(1-c)-ax*s],
            [az*ax*(1-c)-ay*s, az*ay*(1-c) + ax*s, c+az**2*(1-c)]
        ])

'''
A wrapper to general_rotation named more appropriately. Returns a rotation matrix that rotates about an axis by an angle.
args:
    a: The axis to rotate about
    theta: The angle to rotate by. 
'''
def axisangle(a, theta):
    return general_rotation(a,theta)


'''
'''
def matrix_to_axisangle(m):
    theta = np.arccos(( m[0,0] + m[1,1] + m[2,2] - 1)/2)
    x = (m[2,1] - m[1,2])/np.sqrt((m[2,1] - m[1,2])**2+(m[0,2] - m[2,0])**2+(m[1,0] - m[0,1])**2)
    y = (m[0,2] - m[2,0])/np.sqrt((m[2,1] - m[1,2])**2+(m[0,2] - m[2,0])**2+(m[1,0] - m[0,1])**2)
    z = (m[1,0] - m[0,1])/np.sqrt((m[2,1] - m[1,2])**2+(m[0,2] - m[2,0])**2+(m[1,0] - m[0,1])**2)
    return (theta, np.array([x,y,z]))



'''
'''
def generalized_circle(draw, center, vec, radius, r, scale = 200, shift = np.array([1000,1000,0]), rgba = (255,122,0,50),width=5):
    vec = vec/sum(vec**2)**0.5
    if vec[0] == 0 and vec[1] == 0:
        orthogonal_vec = np.array([1,1,0])
    else:
        orthogonal_vec = np.array([vec[0], -vec[1], 0]) 
    orthogonal_vec = orthogonal_vec/sum(orthogonal_vec**2)**0.5
    pt1 = center + radius * orthogonal_vec
    pt1 = np.dot(r,pt1)
    theta = np.pi * 2.0 / 80.0
    r1 = general_rotation(np.dot(r,vec),theta)
    for j in range(0,80):       
        pt2 = np.dot(r1,pt1)
        #draw.ellipse( (pt2[0]-2,pt2[1]-2,pt2[0]+2,pt2[1]+2), fill = (68,193,195), outline = (68,193,195))
        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=rgba, width=width)
        pt1 = pt2

'''
'''
def generalized_circle2(draw, center, vec, radius, r, scale = 200, shift = np.array([1000,1000,0]), rgba = (255,122,0,50), width=5):
    vec = vec/sum(vec**2)**0.5
    if vec[0] == 0 and vec[1] == 0:
        orthogonal_vec = np.array([1,1,0])
    else:
        orthogonal_vec = np.array([vec[0], -vec[1], 0]) 
    orthogonal_vec = orthogonal_vec/sum(orthogonal_vec**2)**0.5
    pt1 = np.dot(r,center) + radius * np.dot(r,orthogonal_vec)
    #pt1 = np.dot(r,pt1)
    theta = np.pi * 2.0 / 80.0
    r1 = general_rotation(np.dot(r,vec),theta)
    for j in range(0,80):       
        pt2 = np.dot(r1,pt1)
        #draw.ellipse( (pt2[0]-2,pt2[1]-2,pt2[0]+2,pt2[1]+2), fill = (68,193,195), outline = (68,193,195))
        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=rgba, width=width)
        pt1 = pt2

'''
'''
def generalized_arc(draw, r, center, vec, point, radius, prcnt = 1, rgba = (255,0,0,100), scale = 200, shift = np.array([1000,1000,0])):
    pt1 = np.dot(r,point)
    vec = vec/sum(vec**2)**0.5
    theta = np.pi * 2.0 / 80.0 * prcnt
    r1 = general_rotation(np.dot(r,vec),theta)
    for j in range(0,80):       
        pt2 = np.dot(r1, pt1)
        #draw.ellipse( (pt2[0]-2,pt2[1]-2,pt2[0]+2,pt2[1]+2), fill = (68,193,195), outline = (68,193,195))
        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=rgba, width=5)
        pt1 = pt2

'''
'''
def rotation(n, theta = np.pi/3):
    r = np.eye(n)
    for i in range(n):
        for j in range(i+1,n):
            rij = np.eye(n)
            rij[i,i] = np.cos(theta)
            rij[i,j] = -np.sin(theta)
            rij[j,i] = np.sin(theta)
            rij[j,j] = np.cos(theta)
            r = np.dot(r,rij)
    return r

'''
'''
def render_sphere():
    im_ind = 0
    shift = np.array([1000, 1000, 0, 0, 0])
    scale = 500
    dim = 3
    for j in range(80):
        r = yzrotation(j)
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im,'RGBA')
        render_sphere(r, draw)
        im.save('Images\\Rotation\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

'''
@Legacy
'''
def transition(im_ind = 0, oldr = general_rotation(np.array([1,0,0]),np.pi/2), newr = rotation(3,2*np.pi*4/30.0) ):
    transn = np.dot(newr,np.transpose(oldr))
    (theta, vec) = matrix_to_axisangle(transn)
    axis_r = np.eye(4)
    for i in np.arange(0,1.1,0.1):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        r = general_rotation(vec,i*theta)
        rr = np.dot(r, oldr)
        axis_r[:3,:3] = rr
        render_scene_4d_axis(draw,axis_r,4)
        parabola(draw, rr)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1


'''
A sequence of intermediate rotations that take the system from an initial rotated state (oldr) to a final one (newr).
args:
    i: 1 means complete rotation to new coordinates, 0 means old rotation.
    oldr: Old rotation matrix.
    newr: New rotation matrix.
'''
def rotation_transition(i = 0, oldr = general_rotation(np.array([1,0,0]),np.pi/2), newr = rotation(3,2*np.pi*4/30.0)):
    transn = np.dot(newr,np.transpose(oldr))
    (theta, vec) = matrix_to_axisangle(transn)
    r = general_rotation(vec, i*theta)
    return np.dot(r, oldr)

'''
What rotation matrix is needed to rotate an old vector to a new vector.
args:
    oldvec: The vector we are starting with.
    newvec: The vector to which we are rotating.
'''
def rotate_vec2vec(oldvec, newvec):
    axis = np.cross(oldvec, newvec)
    oldvec1 = oldvec / np.sqrt(sum(oldvec**2))
    newvec1 = newvec / np.sqrt(sum(newvec**2))
    theta = np.arccos(sum(oldvec1*newvec1))
    return axisangle(axis, theta)

'''
Draws a circle in the x-y plane.
args:
    center : The center of the circle in original coordinate system.
    radius : The radius of the circle in original coordinate system.
'''
def draw_circle(
        draw, r, center=np.array([1,1]), radius=1, 
        start = np.array([0.0, 1.0, 0.0]), arcExtent = 180.0, rgba = (102,255,51,100), width = 5,
        shift = np.array([1000,1000,0]), scale=200):
    if len(center) == 2:
        center = np.concatenate((center, np.array([0])), axis=0)
    center = np.dot(r, center) * scale
    shift1 = shift[:3] + center
    pt1 = np.dot(r,start)
    ##
    theta = np.pi * 2.0 / 180.0
    rot = general_rotation(np.dot(r,np.array([0,0,1])), theta)
    for j in range(0, arcExtent):
        pt2 = np.dot(rot, pt1)
        #draw.line((pt1[0]*scale + shift1[0], pt1[1]*scale+shift1[1], pt2[0]*scale+shift1[0], pt2[1]*scale+shift1[1]), fill=(153, 153, 255,100), width=5)
        draw.line((pt1[0]*scale + shift1[0], pt1[1]*scale+shift1[1], pt2[0]*scale+shift1[0], pt2[1]*scale+shift1[1]), fill=rgba, width=width)
        pt1 = pt2

'''
Draws the projection of a circle onto a plane.
args:
    center : The center of the circle in original coordinate system.
    radius : The radius of the circle in original coordinate system.
    plane : The intercepts of the plane on the x, y and z axes.
    start : The point at which to start drawing the arc. It should be ensured that this point lies on the circle.
    arcEctent : The angle the arc is to make.
'''
def project_circle_on_plane(
        draw, r, center=np.array([1,1]), radius=1, plane = np.array([4.5,4.5,4.5]), 
        start = np.array([0.0, 1.0, 0.0]), arcExtent = 180.0,
        shift = np.array([1000,1000,0]), scale=200):
    [a,b,c] = plane
    center = np.concatenate((center, np.array([0])), axis=0)
    center1 = np.dot(r, center) * scale
    shift1 = shift[:3] + center1
    pt1 = np.dot(r, start)
    [x,y] = np.array([0.0, radius])
    z = c * (1-x/a-y/b)
    pt1Up = np.dot(r, np.array([x,y,z]))
    ##
    theta = np.pi * 2.0 / 180
    rot = general_rotation(np.dot(r,np.array([0,0,1])), theta)
    for j in range(0, arcExtent):
        pt2 = np.dot(rot, pt1)
        pt2Orig = np.dot(np.transpose(r), pt2) + center
        [x,y] = pt2Orig[:2]
        z = c * (1-x/a-y/b)
        pt2Up = np.dot(r, np.array([x,y,z]))
        if sum( ( pt1Up - pt2Up)**2 ) < 0.1:
            draw.line((pt1Up[0]*scale + shift[0], pt1Up[1]*scale+shift[1], pt2Up[0]*scale+shift[0], pt2Up[1]*scale+shift[1]), fill=(102, 102, 255,100), width=5)
            #draw.line((pt1Up[0]*scale + shift[0], pt1Up[1]*scale+shift[1], pt2Up[0]*scale+shift[0], pt2Up[1]*scale+shift[1]), fill=(102,255,51,100), width=5)
        # The vertical lines clibing up.
        draw.line((pt2[0]*scale + shift1[0], pt2[1]*scale+shift1[1], pt2Up[0]*scale+shift[0], pt2Up[1]*scale+shift[1]), fill=(51, 102, 255,100), width=5)
        pt1 = pt2
        pt1Up = pt2Up


def project_circle_on_surface(draw, r, fn, center=np.array([0,0]), radius=0.75, start = np.array([0.0, 0.75, 0.0]), arcExtent = 180.0, shift = np.array([1000,1000,0]), scale=300):
    center = np.concatenate((center, np.array([0])), axis=0)
    center1 = np.dot(r, center) * scale
    shift1 = shift[:3] + center1
    pt1 = np.dot(r, start)
    [x,y] = np.array([0.0, radius])
    z = fn(np.matrix([x,y]))
    pt1Up = np.dot(r, np.array([x,y,z]))
    theta = np.pi * 2.0 / 180
    rot = general_rotation(np.dot(r, np.array([0,0,1])), theta)
    for j in np.arange(0, arcExtent):
        pt2 = np.dot(rot, pt1)
        pt2Orig = np.dot(np.transpose(r), pt2) + center
        [x,y] = pt2Orig[:2]
        z = fn(np.matrix([x,y]))
        pt2Up = np.dot(r, np.array([x,y,z]))
        if sum((pt1Up - pt2Up)**2 ) < 0.1:
            draw.line((pt1Up[0]*scale + shift[0], pt1Up[1]*scale+shift[1], pt2Up[0]*scale+shift[0], pt2Up[1]*scale+shift[1]), fill=(102, 102, 255,100), width=7)
        # The vertical lines clibing up.
        draw.line((pt2[0]*scale + shift1[0], pt2[1]*scale+shift1[1], pt2Up[0]*scale+shift[0], pt2Up[1]*scale+shift[1]), fill=(51, 102, 255,100), width=8)
        pt1 = pt2
        pt1Up = pt2Up


