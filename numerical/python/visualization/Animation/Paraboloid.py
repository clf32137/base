#!/usr/bin/env python
import math
from Sphere import *
from CubeObjects import *

'''
'''
def paraboloid():
    im_ind = 0
    #for i in np.concatenate((np.arange(1.1,20,1),np.arange(-20,-1.1,1)),axis=0):
    for i in (np.concatenate((np.arange(0.5,1,0.01), np.arange(1,3,0.05),np.arange(3,10,0.6)),axis=0) + 1e-4): #Controls the rotation of the plane.
        r2 = general_rotation(np.array([.3, .3, .3]), np.pi/i)
        r1 = np.eye(4)
        orthogonal_vec = np.dot(r2, np.array([0,1,0]))
        orthogonal_vec = orthogonal_vec/sum(orthogonal_vec**2) # Should be unnecessary since rotation doesn't change magnitude.
        for j in range(4,5): # Controls the rotation of the paraboloid.
            r = rotation(3, 2*np.pi*j/30.0)
            r1[:3,:3] = r
            im = Image.new("RGB", (2048, 2048), "black")
            draw = ImageDraw.Draw(im, 'RGBA')
            translate = np.array([0,0,1.5])
            plane(draw, r, r2, 200, np.array([1000,1000,0]), translate)
            render_scene_4d_axis(draw, r1, 4)
            for z in np.arange(0.001, 3.5, 0.01):
                #generalized_circle(draw, np.array([0,0,z]), np.array([0,0,1]), np.sqrt(z), r, rgba = (255,20,147,50))
                #generalized_arc(draw, r, np.array([0,0,z]), np.array([0,0,1]), np.array([np.sqrt(z),0,z]), np.sqrt(z), 0.5, (255,20,147,50))
                #generalized_arc(draw, r, np.array([0,0,z]), np.array([0,0,1]), np.array([-np.sqrt(z),0,z]), np.sqrt(z), 0.5, (255,20,147,10))
                pt1 = np.dot(r, np.array([-np.sqrt(z),0,z]))
                theta = np.pi * 2.0 / 180.0
                rot = general_rotation(np.dot(r,np.array([0,0,1])),theta)
                for j in range(0,180):
                    pt2 = np.dot(rot, pt1)
                    pt2Orig = np.dot(np.transpose(r),pt2)
                    if sum(pt2Orig * orthogonal_vec) - 1.5*orthogonal_vec[2] > 0:
                        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=(255,20,147,30), width=5)
                    else:
                        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=(255,20,147,10), width=5)
                    pt1 = pt2
            #parabola(draw,r)
            curve(draw, r, r2)
            im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
            im_ind = im_ind + 1

'''
Draws a section of a paraboloid between two planes. The first plane is the x-y plane and the second one is x-y plane rotated by an angle gamma
along the z-axis.
'''
def paraboloidSection(gamma, draw = None):
    im_ind = 0
    r1 = np.eye(4)
    j = 4
    r = rotation(3,2*np.pi*j/30.0)
    r1[:3,:3] = r
    if draw is None:
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
    render_scene_4d_axis(draw, r1, 4)
    # Now we create the paraboloid one x-y cross section at a time.
    for z in np.arange(0.001, 3.5, 0.01):
        pt1 = np.dot(r, np.array([0,np.sqrt(z),z]))
        theta = np.pi * 2.0 / 180.0
        # A small rotation along the z-axis. This will create the circle that is the paraboloid section.
        rot = general_rotation(np.dot(r,np.array([0,0,1])), theta)
        for j in range(0,180):
            pt2 = np.dot(rot, pt1)
            if j * theta  < gamma:
                draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=(255,20,147,30), width=5)
            else:
                #draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=(255,20,147,10), width=5)
                continue
            pt1 = pt2
    if draw is None:
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

'''
Creates the 3 dimensional graph for a general quadratic form given by - ax^2+by^2+2cxy
'''
def generalParaboloid(coeffs = [1.0,1.0,0], draw = None, j = 4, scale = 200):
    [a, b, c] = coeffs
    im_ind = 0
    r1 = np.eye(4)
    r = rotation(3,2*np.pi*j/30.0)
    #r = np.eye(3)
    r1[:3,:3] = r
    if draw is None:
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
    render_scene_4d_axis(draw, r1, 4)    
    # Now we create the paraboloid one x-y cross section at a time.
    for z in np.arange(0.001, 3.5, 0.01):
        radius1 = np.sqrt(z)
        pt1 = np.array([0,np.sqrt(z),z])
        theta = np.pi * 2.0 / 180.0
        # A small rotation along the z-axis. This will create the circle that is the paraboloid section.
        rot = general_rotation(np.array([0,0,1]), theta)
        for j in range(0,180):
            pt2 = np.dot(rot, pt1)
            radius2 = np.sqrt(z / (a * np.cos(j*theta)**2 + b*np.sin(j*theta)**2 + 2*c*np.cos(j*theta)*np.sin(j*theta)))
            pt2 = pt2 * radius2/radius1
            rpt1 = np.dot(r,pt1)
            rpt2 = np.dot(r,pt2)
            draw.line((rpt1[0]*scale + shift[0], rpt1[1]*scale+shift[1], rpt2[0]*scale+shift[0], rpt2[1]*scale+shift[1]), fill=(255,20,147,30), width=5)
            pt1 = pt2
            radius1 = radius2
    if draw is None:
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

'''
@MoneyShot
    A paraboloid with a plane tangential to it.
'''
def paraboloid_dirty(im_ind = 0, scale = 200, shift = np.array([1000,1000,0]), opacity = 60):
    font = ImageFont.truetype("arial.ttf", 75)
    for i in np.arange(1,2): #Controls the rotation of the plane.
        r2 = general_rotation(np.array([.3, .3, .3]), np.pi/i)
        r1 = np.eye(4)
        #orthogonal_vec = np.dot(r2, np.array([0,1,0]))
        #orthogonal_vec = orthogonal_vec/sum(orthogonal_vec**2) # Should be unnecessary since rotation doesn't change magnitude.
        rot = general_rotation(np.array([0,0,1]), np.pi/20.0 * (8 + im_ind/3.0) )
        for j in range(4,5): # Controls the rotation of the paraboloid.
            txt = "1) What direction minimizes the plane?"
            txt1 = "2) How do we know we have reached a minima?"
            txt2 = "3) Move along that direction."
            r = rotation(3, 2 * np.pi* j /30.0)
            r = np.dot(r, rot)
            #rfinal = general_rotation(np.array([1.0,0,0]), np.pi/2)
            rfinal = np.eye(3)
            rtrnsn = np.dot(rfinal, np.transpose(r))
            (theta, ax) = matrix_to_axisangle(rtrnsn)
            #r = np.dot( general_rotation(ax, theta * (10.0 - im_ind)/10.0 ), r)
            #r = np.dot(general_rotation(ax, theta * im_ind/10.0), r)
            r1[:3,:3] = r
            im = Image.new("RGB", (2048, 2048), "black")
            #im = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\RotatingCube\\base.png')
            draw = ImageDraw.Draw(im, 'RGBA')
            #im_stone = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Objects\\stone.png')
            #im_stone.thumbnail((  1281*im_ind / 7.0,  758*im_ind / 7.0 ), Image.ANTIALIAS)
            #pasteImage(im_stone, im, (im_ind * 100, im_ind * 100))
            #draw.text((250,200), txt[:min(im_ind*3, len(txt))], (255,255,255), font=font)
            #if im_ind * 3 > len(txt):
            #    draw.text((250,270), txt1[:min( (im_ind*3-len(txt)) , len(txt1))], (255,255,255), font=font)
            #if im_ind * 3 > len(txt) + len(txt1):
            #    draw.text((250,340), txt2[:min( (im_ind*3-len(txt)-len(txt1)) , len(txt2))], (255,255,255), font=font)
            #render_xy_plane(draw, r1)
            translate = np.array([0, 0, 1.5])
            render_scene_4d_axis(draw, r1, 4, scale, shift)
            #xzplane(draw, r, 1)
            #xzcurve(draw, r, 1)
            #xyplane(draw, r, 1)
            #xycurve(draw, r, 1)
            #verticalLine(draw, r, 1.0, 1.0)
            y_posn = 2000 - 32 * 60
            #im_cat = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Objects\\cat\\cat_top'+ str(1+im_ind%4)+ '.png')
            #pasteImage(im_cat, im, (1050-196,y_posn - 80 - abs(16*np.sin(im_ind))) )
            im_lazer = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Objects\\lazer_dot.png')
            im_lazer.thumbnail((60,60), Image.ANTIALIAS)
            #pasteImage(im_lazer, im, (1050,y_posn))
            for z in np.arange(0.001, 3.5, 0.01):
                #generalized_circle(draw, np.array([0,0,z]), np.array([0,0,1]), np.sqrt(z), r, rgba = (255,20,147,50))
                pt1 = np.dot(r, np.array([-np.sqrt(z),0,z]))
                theta = np.pi * 2.0 / 180.0
                rot = general_rotation(np.dot(r,np.array([0,0,1])),theta)
                for j in range(0, 180):
                    pt2 = np.dot(rot, pt1)
                    pt2Orig = np.dot(np.transpose(r),pt2)                    
                    if pt2Orig[0] > 1 and pt2Orig[1] > 1:
                        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=(255,20,147,60), width=5) #50
                    elif pt2Orig[0] > 1 or pt2Orig[1] > 1:
                        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=(255,20,147, 60 ), width=5) #17
                    else:
                        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=(255,20,147, 60 ), width=5) #10
                    pt1 = pt2
            [i,j] = helix(im_ind)
            #draw_points(draw,r,i,j)
            #all_points(draw,r)
            #im_sam = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\\SamuraiBest\\SamuraiWalking\\Waving\\im' +  str(im_ind) + '.png')
            #im_sam.thumbnail((750*0.6,1000*0.6), Image.ANTIALIAS)
            #pasteImage(im_sam,im,(1275,1170))
            #xzgradients(draw, r, 1.0) # draws the arrows correponding to gradients.
            im_car = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Misc\\toycar.png')
            im_car.thumbnail((200,200), Image.ANTIALIAS)
            x_min = 0.98
            slope = 2 * x_min
            angle = np.arctan(slope) * 180 / np.pi
            im_car_faded = im_car.rotate(angle)
            im_car_faded = im_car_faded.point(lambda p: p*0.6)
            posn = np.array([x_min, -(x_min*x_min + 1)]) * scale + shift[:2] - np.array([100,100])
            #pasteImage(im_car_faded, im, posn)
            x1 = x_min + 9 * 0.05
            slope = 2 * x1
            angle = np.arctan(slope) * 180 / np.pi
            im_car = im_car.rotate(angle)
            posn = np.array([x1, -(x1*x1 + 1)]) * scale + shift[:2] - np.array([100,100])
            #pasteImage(im_car, im, posn)
            span = (x1*x1 - x_min*x_min) * scale
            destin = np.array([1635, 340])
            #base = np.array([1000 + x_min * scale,1000])
            base = np.array([1000, 1000 - posn[1] - 100])
            vec = destin - base
            #drawDoubleArrowVer(draw, base +  vec * (im_ind-22.0)/10.0, span-(im_ind-22.0)/10.0*span)
            im_math = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Math\\delZBydelX.png')
            #im_math.thumbnail((im_math.size[0] * (1-im_ind/10.0+0.1), im_math.size[1] * (1-im_ind/10.0+0.1)), Image.ANTIALIAS)
            posn = np.array([1635, 400]) +  ((np.dot(r, np.array([1,3,2])) * scale + shift[:3])[:2] - np.array([1635,400])) * im_ind / 10.0
            #pasteImage(im_math, im, (posn[0],posn[1]))
            im_math = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Math\\delZBydelY.png')
            #im_math.thumbnail((im_math.size[0] * (1-im_ind/10.0+0.1), im_math.size[1] * (1-im_ind/10.0+0.1)), Image.ANTIALIAS)
            posn = np.array([1635, 620]) +  ((np.dot(r, np.array([3,1,2])) * scale + shift[:3])[:2] - np.array([1635,620])) * im_ind / 10.0
            im_math = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Math\\(x,y).png')
            #pasteImage(im_math,im,(1220,1165))
            im_math = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Math\\x=1.png')
            #pasteImage(im_math,im,(1480,217))
            #pasteImage(im_math, im, (posn[0],posn[1]))
            optim = np.dot(r,np.array([1,0,1])) * scale + shift[:3]
            #draw.ellipse((optim[0]-10,optim[1]-10,optim[0]+10,optim[1]+10),fill="yellow")
            #arrowV1(draw,r,np.array([1,0,1]), np.array([3,0,1]),(204,102,255))
            xvals = [-1.2,-0.7,-0.3,-0.1,0.1,0.3,0.7,1.2]
            #for i in range(im_ind):
                #y = xvals[i]
                #arrowV1(draw,r,np.array([1,y,1+y**2]), np.array([3,3*y,1+y**2]),(204,102,255))
            takeUp = 2.0
            [vx, vy, vz] = np.dot(r, np.array([1,1,2.0])) * scale + shift[:3]
            size = (10) # + im_ind*18.0/24.0
            #draw.ellipse( (vx-size,vy-size,vx+size,vy+size), fill = 'yellow', outline = 'yellow')
            [vx1, vy1, vz1] = np.dot(r, np.array([1,1,0.0])) * scale + shift[:3]
            #
            #now!
            xy = (np.sin(np.pi * im_ind/5.0))/2 + np.cos(np.pi * im_ind/10.0)/1.5
            zz = 2*xy**2
            [vx2, vy2, vz2] = np.dot(r, np.array([xy, xy, 2 * xy**2 ])) * scale + shift[:3]
            draw.ellipse( (vx2-size,vy2-size,vx2+size,vy2+size), fill = 'red', outline = 'yellow')
            paraboloidTangent(draw, r, xy , xy, d = 1.0, rgba = (120,80,200,150), scale = scale, shift = shift)
            centerOffset = np.array([vx1-1000.0, vy1-1000.0, 0])
            shift1 = shift + centerOffset
            #draw.line((vx,vy,vx2,vy2), fill='red', width = 7)            
            vtemp = np.dot(r, np.array([1.0,1.0,2.0])) * scale + shift[:3]
            if xy > 0:
                arrowV1(draw,r, np.array([xy+zz, xy+zz,zz]), np.array([xy,xy,zz]), (120,80,200))
            else:
                arrowV1(draw,r, np.array([xy-zz, xy-zz,zz]), np.array([xy,xy,zz]), (120,80,200))
            ext = 10.0 * 1.0/10.0
            x1,y1 = xy, xy
            x2,y2 = xy-ext, xy-ext
            line_pt = np.array([x2, y2, zz])
            plane_pt = np.array([x2, y2, 2*x1*x2 + 2*y1*y2 - (x1**2 + y1**2)])
            vtemp = np.dot(r, np.array([xy,xy,zz])) * scale + shift[:3]
            vtemp2 = np.dot(r, plane_pt) * scale + shift[:3]
            vtemp3 = np.dot(r, line_pt) * scale + shift[:3]
            draw.line((vtemp[0],vtemp[1],vtemp2[0],vtemp2[1]), fill = 'blue', width = 7)
            draw.polygon([(vtemp[0], vtemp[1]),(vtemp2[0], vtemp2[1]),(vtemp3[0], vtemp3[1])], (0,0,255,80))
            ext = -10.0 * 1.0/10.0
            x2,y2 = xy-ext, xy-ext
            line_pt = np.array([x2, y2, zz])
            plane_pt = np.array([x2, y2, 2*x1*x2 + 2*y1*y2 - (x1**2 + y1**2)])
            vtemp = np.dot(r, np.array([xy,xy,zz])) * scale + shift[:3]
            vtemp2 = np.dot(r, plane_pt) * scale + shift[:3]
            vtemp3 = np.dot(r, line_pt) * scale + shift[:3]
            draw.line((vtemp[0],vtemp[1],vtemp2[0],vtemp2[1]), fill = 'red', width = 7)
            draw.polygon([(vtemp[0], vtemp[1]),(vtemp2[0], vtemp2[1]),(vtemp3[0], vtemp3[1])], (255,0,0,80))
            #
            pt1 = np.dot(r, np.array([0.0, 1.0, takeUp]))
            pt1Orig = np.dot(np.transpose(r), pt1) + np.array([1,1,takeUp])
            [x,y] = pt1Orig[:2]
            z = 2*x + 2*y - 2
            pt1Up = np.dot(r, np.array([x,y,z]))
            ##
            theta = np.pi * 2.0 / 180.0
            rot = general_rotation(np.dot(r,np.array([0,0,1])), theta)
            #for j in range(0, int(180*im_ind/10.0)):
            '''
            for j in range(0, 180):
                pt2 = np.dot(rot, pt1)
                pt2Orig = np.dot(np.transpose(r), pt2) + np.array([1,1,0])
                [x,y] = pt2Orig[:2]
                z = 2*x + 2*y - 2
                pt2Up = np.dot(r, np.array([x,y,z]))
                draw.line((pt2[0]*scale + shift1[0], pt2[1]*scale+shift1[1], pt2Up[0]*scale+shift[0], pt2Up[1]*scale+shift[1]), fill=(0,153,255,100), width=5)
                #continue
                draw.line((pt1[0]*scale + shift1[0], pt1[1]*scale+shift1[1], pt2[0]*scale+shift1[0], pt2[1]*scale+shift1[1]), fill=(0,153,255,100), width=5)
                draw.line((pt1Up[0]*scale + shift[0], pt1Up[1]*scale+shift[1], pt2Up[0]*scale+shift[0], pt2Up[1]*scale+shift[1]), fill=(0,153,255,100), width=5)
                pt1 = pt2
                pt1Up = pt2Up
            '''
            #if j > 0:
            j = (np.sin(im_ind/5.0)) * 40 + np.cos(im_ind/20.0) * 60
            arrowHead = np.array([np.sin(-theta * j), np.cos(-theta * j), takeUp]) + np.array([1,1,0])
            #arrowV1(draw,r,np.array([1,1,takeUp]), arrowHead, (204,102,255))
            [x,y] = np.array([np.sin(-theta * j), np.cos(-theta * j)]) + np.array([1,1])
            z = 2*x + 2*y - 2
            rgb = heat_rgb(-1, 5, z)
            arrowHeadUp = np.array([x,y,z])
            #arrowHeadUp = np.dot(r, arrowHeadUp)
            #arrowHead = np.dot(r, arrowHead)
            #draw.line((arrowHead[0]*scale + shift[0], arrowHead[1]*scale+shift[1], arrowHeadUp[0]*scale+shift[0], arrowHeadUp[1]*scale+shift[1]), fill=(66,146,244 ), width=5)
            #arrowV1(draw,r,arrowHead, arrowHeadUp, (66,146,244))
            #arrowV1(draw,r,arrowHead, arrowHeadUp, rgb)
            y_samurai = 1195 if im_ind < 6 else (1195-(im_ind-5)*80)
            #pasteSamurai(im, ind = im_ind, posn = (35*30, y_samurai))
            alp = 50 + im_ind * 10
            im = im.crop((0,0,2048,1365))
            im.thumbnail((1024, 682), Image.ANTIALIAS)
            im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
            im_ind = im_ind + 1

'''
Draws a tangent plane to a paraboloid: x^2+y^2 = z at point given by coordinates (x1, y1)
'''
def paraboloidTangent(draw, r, x1, y1, d = 1.0, rgba = (120,80,200,150), scale = 200, shift = np.array([1000,1000,0])):
    x2 = x1-d
    y2 = y1+d
    pt1 = np.dot( r, np.array([x2, y2, z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    x2 = x1+d
    y2 = y1+d
    pt2 = np.dot( r, np.array([x2, y2, z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    x2 = x1+d
    y2 = y1-d
    pt3 = np.dot( r, np.array([x2, y2, z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    x2 = x1-d
    y2 = y1-d
    pt4 = np.dot( r, np.array([x2, y2, z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    draw.polygon( [(pt1[0], pt1[1]), (pt2[0], pt2[1]), (pt3[0], pt3[1]), (pt4[0], pt4[1])], rgba)

'''
Returns the z-coordinate of a point on a plane that is tangent to the paraboloid z = x^2 + y^2
'''
def z_plane(x, y, x1, y1):
    return 2*x1*x + 2*y1*y - (x1**2 + y1**2)

'''
'''
def helix(ind):
    theta = np.pi/4
    r = np.sqrt(2)
    r = r - ind * np.sqrt(2)/40
    theta = theta + ind * np.pi/20.0
    return np.array([r*np.cos(theta), r*np.sin(theta)])

'''
'''
def verticalLine(draw, r, x, y):
    extent = 2.8
    pln = np.array(
            [
                [x, y, 0],
                [x, y, extent*2]
            ]
        )
    pln = np.dot(pln, np.transpose(r)) * scale + shift[:3]
    draw.line((pln[0][0], pln[0][1], pln[1][0], pln[1][1]), fill = (0,102,255,100), width = 3)

'''
'''
def xzplane(draw, r, y):
    extent = 2.8
    pln = np.array(
            [
                [-extent,y,0],
                [extent,y,0],
                [extent,y,extent*2],
                [-extent,y,extent*2]
            ]
        )
    pln = np.dot(pln, np.transpose(r))
    pln = pln * scale + shift[:3]
    #draw.polygon([(pln[0][0],pln[0][1]),(pln[1][0],pln[1][1]),(pln[2][0],pln[2][1]),(pln[3][0],pln[3][1])], (204,0,255,70))
    draw.polygon([(pln[0][0],pln[0][1]),(pln[1][0],pln[1][1]),(pln[2][0],pln[2][1]),(pln[3][0],pln[3][1])], (0,102,255,70))

'''
'''
def xyplane(draw, r, x):
    extent = 2.8
    pln = np.array(
            [
                [x,-extent,0],
                [x,extent,0],
                [x,extent,extent*2],
                [x,-extent,extent*2]
            ]
        )
    pln = np.dot(pln,np.transpose(r))
    pln = pln * scale + shift[:3]
    #draw.polygon([(pln[0][0],pln[0][1]),(pln[1][0],pln[1][1]),(pln[2][0],pln[2][1]),(pln[3][0],pln[3][1])], (204,0,255,70))
    draw.polygon([(pln[0][0],pln[0][1]),(pln[1][0],pln[1][1]),(pln[2][0],pln[2][1]),(pln[3][0],pln[3][1])], (0,102,255,70))

'''
Draws a parabola in the x-z plane with minimum at origin.
args:
    y: The point at which the plane perpendicular to the y-axis intersects it. This plane is to intersect the paraboloid.
'''
def xzcurve(draw, r, y, maxx = None, rgba = (204,102,255), width = 5):
    minx = np.sqrt(3.5 - y*y)
    if maxx is None:
        maxx = abs(minx)
    z = minx * minx + y * y
    pt1 = np.dot(r, [-minx, y, z]) * scale + shift[:3]
    for x in np.arange(-minx, maxx, 0.01):
        z = x*x + y*y
        pt2 = np.dot(r, [x, y, z]) * scale + shift[:3]
        draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = rgba, width=width)
        #draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (0,102,255), width=5)
        pt1 = pt2

'''
Draws a parabola in the x-z plane with minimum at origin.
args:
    x: The point at which the plane perpendicular to the y-axis intersects it. This plane is to intersect the paraboloid.
'''
def xycurve(draw, r, x, maxy = None, rgba = (204,102,255), width=5):
    miny = np.sqrt(3.5 - x*x)
    if maxy is None:
        maxy = abs(miny)
    z = miny * miny + x * x
    pt1 = np.dot(r, [x, -miny, z]) * scale + shift[:3]
    for y in np.arange(-miny, maxy, 0.01):
        z = x*x + y*y
        pt2 = np.dot(r, [x, y, z]) * scale + shift[:3]
        draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = rgba, width=width)
        #draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (0,102,255), width=5)
        pt1 = pt2

'''
Rolls an object (like a soccer ball) down the x-z curve.
args:
    y: The point at which the plane perpendicular to the y-axis intersects it. This plane is to intersect the paraboloid.
'''
def rollBallDownCurve(im, r, y, imobj, p = 0.7, maxx = None):    
    minx = np.sqrt(3.5 - y*y)
    if maxx is None:
        maxx = abs(minx)
    z = minx * minx + y * y
    pt1 = np.dot(r,[y, -minx, z]) * scale + shift[:3]
    #for x in np.arange(-minx, maxx, 0.01):
    x = -minx * p + maxx * (1-p)
    z = x*x + y*y
    pt2 = np.dot(r, [ y, x, z]) * scale + shift[:3]
    pasteImage(imobj,im,(pt2[0], pt2[1]))
    #pasteImage(imobj,im,(1000,1000))
    pt1 = pt2


def xzgradients(draw, r, y):
    for x in [-1.2,-0.7,-0.3,-0.1,0.1,0.3,0.7,1.2]:
        z = x*x + y*y
        #draw_points(draw, r, y, x)
        arrowV1(draw,r,np.array([y,x,z]), np.array([3*y,3*x,z]), (204,102,255))
        arrowV1(draw,r,np.array([y,x,z]), np.array([y+1.0,x,z]), (0,102,255))

def all_points(draw,r):
    for i in np.arange(1,2):
        for j in np.arange(1,2):
            if i >=0 or j >=0:
                draw_points(draw, r, i, j)

def draw_points(draw, r, i, j):
    bub=7
    z_coord = i**2 + j**2
    grad_coord = np.array([3*i,3*j,z_coord])
    xx = np.array([i,0,0])
    xx = np.dot(r, xx)
    xx = xx * scale + shift[:3]
    draw.ellipse((xx[0]-5,xx[1]-5,xx[0]+5,xx[1]+5),fill="yellow")
    yy = np.array([0,j,0])
    yy = np.dot(r,yy)
    yy = yy * scale + shift[:3]
    draw.ellipse((yy[0]-5,yy[1]-5,yy[0]+5,yy[1]+5),fill="yellow")
    xy = np.array([i,j,0])
    xy = np.dot(r,xy)
    xy = xy*scale+shift[:3]
    draw.line((xx[0],xx[1],xy[0],xy[1]), fill="yellow")
    yypr1 = np.array([0,j,0]) + (np.array([1,1,2]) - np.array([0,j,0])) * 1.0
    yypr2 = np.array([i,j,0]) + (np.array([3,1,2]) - np.array([i,j,0])) * 1.0
    yypr1 = np.dot(r,yypr1) * scale + shift[:3]
    yypr2 = np.dot(r,yypr2) * scale + shift[:3]
    #draw.line((yypr1[0],yypr1[1],yypr2[0],yypr2[1]), fill="yellow")
    xxpr1 = np.array([i,0,0]) + (np.array([1,1,2]) - np.array([i,0,0])) * 1.0
    xxpr2 = np.array([i,j,0]) + (np.array([1,3,2]) - np.array([i,j,0])) * 1.0
    xxpr1 = np.dot(r,xxpr1) * scale + shift[:3]
    xxpr2 = np.dot(r,xxpr2) * scale + shift[:3]
    xyzpr = np.dot(r,np.array([3,3,2]))*scale + shift[:3]
    xyz = np.dot(r,np.array([i,j,i**2+j**2])) * scale + shift[:3]                
    #draw.line((xxpr1[0],xxpr1[1],xxpr2[0],xxpr2[1]), fill="yellow")
    #draw.line((xxpr1[0],xxpr1[1],xxpr2[0],xxpr2[1]), fill="green", width=5)
    xxpr1 = np.array([1,1,2])
    xxpr2 = np.array([1,3,2])
    #arrowV1(draw,r,xxpr1,xxpr2)
    xxpr1 = np.dot(r,xxpr1) * scale + shift[:3]
    xxpr2 = np.dot(r,xxpr2) * scale + shift[:3]
    #draw.polygon([(xyz[0],xyz[1]),(xxpr2[0],xxpr2[1]),(xyzpr[0],xyzpr[1]),(yypr2[0],yypr2[1])],fill=(204,102,255,80))
    draw.line((yy[0],yy[1],xy[0],xy[1]), fill="yellow")
    draw.ellipse((xy[0]-7,xy[1]-7,xy[0]+7,xy[1]+7),fill=(204,102,255))
    draw.line((xy[0],xy[1],xyz[0],xyz[1]),fill=(204,102,255),width=3)
    draw.ellipse((xyz[0]-bub,xyz[1]-bub,xyz[0]+bub,xyz[1]+bub),fill=(147,112,219))
    #draw.line((xxpr2[0],xxpr2[1],xyzpr[0],xyzpr[1]),fill="green", width=5)##
    xxpr2 = np.array([1,3,2])
    xyzpr = np.array([3,3,2])
    #arrowV1(draw,r,xxpr2,xyzpr)
    zz = np.dot(r,np.array([0,0,i**2+j**2])) * scale + shift[:3]
    #draw.line((zz[0],zz[1],xyz[0],xyz[1]),fill="blue")
    dircn = xyz - zz
    new_pt = xyz + dircn * 2.0
    #draw.line((new_pt[0],new_pt[1],xyz[0],xyz[1]),fill=(204,102,255),width=3)
    arrowV1(draw,r,np.array([i,j,z_coord]),grad_coord,(204,102,255))
    #arrowV1(draw,r,np.array([0,0,z_coord]),np.array([i,j,z_coord]))
    #arrowV1(draw,r,np.array([0,0,0]),np.array([3,3,2]),(255,255,255))


def arrow(draw, r, start, end):
    end1 = end - start
    start1 = np.array([0,0,0])
    offset = np.array([1000,1000,1000]) - np.dot(r, end1 - end) * scale
    for i in np.arange(0,2,0.2):
        generalized_circle(draw, end1 - i/50.0 * (end1-start1), (start1-end1), i/4.0, r, rgba=(0,255,0,100),shift=offset)
    start = np.dot(r, start) * scale + shift[:3]
    end = np.dot(r,end) * scale + shift[:3]
    draw.line((start[0],start[1],end[0],end[1]),fill="green",width=5)
    i = 1.8
    generalized_circle(draw, end1 - i/50.0 * (end1-start1), (start1-end1), i/4.0, r,rgba="white",width=1,shift=offset)

'''
Draws an arrow from start point to end point.
'''
def arrowV1(draw, r, start, end, rgb = (0,255,0), scale=200, shift=np.array([1000,1000,0])):
    rgba = rgb + (150,)
    [cx,cy,cz] = start + (end-start) * 0.8 # The base of the arrow.
    c_vec = np.dot(r, np.array([cx,cy,cz])) * scale + shift[:3]
    [ex,ey,ez] = (end - start)
    if abs(ez) < 1e-6:
        arrowV2(draw, r, start, end, rgb, scale, shift)
        return
    start = np.dot(r, start) * scale + shift[:3]
    end = np.dot(r, end) * scale + shift[:3]
    d = 0.08
    y1_range = abs(d * (ez**2 + ex**2)**0.5/ (ex**2 + ey**2 + ez**2)**.5)
    for y1 in np.arange(-y1_range, y1_range, 0.0033):
        det = max(4*ex**2*ey**2/ ez**4 * y1**2 - 4*((1 + ey**2/ez**2)*y1**2 - d**2)*(1 + ex**2/ez**2),0)
        x1 = (-2*(ex*ey/ez**2*y1) + det**0.5)/2/(1+ex**2/ez**2)
        z1 = (-ex*x1 - ey*y1)/ez
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
        x1 = (-2*(ex*ey/ez**2*y1) - det**0.5)/2/(1+ex**2/ez**2)
        z1 = (-ex*x1 - ey*y1)/ez
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
    draw.line((start[0],start[1],end[0],end[1]),fill=rgb,width=5)

def arrowV2(draw, r, start, end, rgb = (0,255,0), scale = 200, shift = np.array([1000,1000,0])):
    rgba = rgb + (150,)
    [cx,cy,cz] = start + (end-start) * 0.8 # The base of the arrow.
    c_vec = np.dot(r, np.array([cx,cy,cz])) * scale + shift[:3]
    [ex,ey,ez] = (end - start)
    if abs(ey) < 1e-6:
        arrowV3(draw, r, start, end, rgb, shift = shift, scale = scale)
        return
    start = np.dot(r, start) * scale + shift[:3]
    end = np.dot(r, end) * scale + shift[:3]
    d = 0.08
    x1_range = abs(d * ey / (ex**2 + ey**2)**0.5)

    for x1 in np.arange(-x1_range, x1_range, x1_range/30):
        y1 = -ex/ey * x1
        z1 = max( (d**2 - x1**2*(1+ex**2/ey**2)), 0) **0.5
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
        z1 = -z1
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
    draw.line((start[0],start[1],end[0],end[1]),fill=rgb,width=5)

def arrowV3(draw, r, start, end, rgb = (0,255,0), scale = 200, shift = np.array([1000,1000,0])):
    rgba = rgb + (150,)
    [cx,cy,cz] = start + (end-start) * 0.8 # The base of the arrow.
    c_vec = np.dot(r, np.array([cx,cy,cz])) * scale + shift[:3]
    [ex,ey,ez] = (end - start)
    start = np.dot(r, start) * scale + shift[:3]
    end = np.dot(r, end) * scale + shift[:3]
    d = 0.08
    for y1 in np.arange(-d, d, 0.0002):
        z1 = np.sqrt(d**2-y1**2)
        x1 = 0
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
        z1 = -z1
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
    draw.line((start[0],start[1],end[0],end[1]),fill=rgb,width=5)

def paraboloidV2(im_ind = 0):
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    r = rotation(3,2*np.pi*4/30.0)
    parabola(draw, r)
    r1 = np.eye(4)
    r1[:3,:3] = r
    render_scene_4d_axis(draw,r1,4)
    for theta in np.arange(0, np.pi*2, 0.1):
        r2 = general_rotation(np.dot(r,np.array([0,0,1])),theta)
        r3 = np.dot(r2,r)
        parabola(draw, r3)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

'''
A sequence of intermediate rotations that take the system from an initial rotated state (oldr) to a final one (newr).
'''
def transition(im_ind = 0):
    oldr = general_rotation(np.array([1,0,0]),np.pi/2)
    newr = rotation(3,2*np.pi*4/30.0)
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

def parabola(draw=None, r=None, scale=200, shift=np.array([1000,1000,0])):
    im_ind = 14
    if r == None:
        update = True
    else:
        update = False
    for j in range(0,1):
        if update:
            im = Image.new("RGB", (2048, 2048), "black")
            draw = ImageDraw.Draw(im, 'RGBA')
            #r = rotation(3, 2*np.pi*j/30)
            r = general_rotation(np.array([1,0,0]),np.pi/2)
        pt1 = np.dot(r,[-2.0, 0, 2.0*2.0]) * scale + shift[:3]
        #pt1 = np.dot(r,[-2.0, -2.0*2.0, 0]) * scale + shift[:3]
        for x in np.arange(-2.0, 2.0, 0.01):
            pt2 = np.dot(r, [x, 0, x*x]) * scale + shift[:3]
            #pt2 = np.dot(r, [x, -x*x, 0]) * scale + shift[:3]
            draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (255,20,147,200), width=3)
            pt1 = pt2
        #draw.ellipse((1000-5,1000-5,1000+5,1000+5),fill="yellow")
        if update:
            im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
            im_ind = im_ind + 1

'''
Draws a curve described by the intersection of a plane with the paraboloid x^2+y^2 = z
params:
    r: The rotation matrix the whole scene is rotated by
    r2: The rotation matrix that the inetersecting plane is to be rotated by
'''
def curve(draw, r, r2, scale = 200, shift = np.array([1000,1000,0])):
    # Assume you start with the x-z plane
    orthogonal_vec = np.array([0,1,0])
    orthogonal_vec = np.dot(r2, orthogonal_vec)
    b = 1.5
    [thetax, thetay, thetaz] = orthogonal_vec
    c1 = -thetax/thetaz/2
    c2 = -thetay/thetaz/2
    c3 = np.sqrt(b + c1**2 + c2**2)
    x_min = max((c1 - abs(c3)),-np.sqrt(3.5))
    x_max = min((c1 + abs(c3)),np.sqrt(3.5))
    y = c2 + np.sqrt(c3*c3 - (x_min-c1)*(x_min-c1))
    pt1 = np.dot(r, [x_min, y, (x_min**2+y**2)]) * scale + shift[:3]
    for x in np.arange(x_min, x_max, 0.01):
        y = c2 + np.sqrt(c3*c3 - (x-c1)*(x-c1))
        pt2 = np.dot(r, [x, y, (x**2 + y**2)]) * scale + shift[:3]
        if x**2 + y**2 < 3.5:
            draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (204,102,255), width=5)
        pt1 = pt2
    y = c2 + np.sqrt(c3*c3 - (x_min-c1)*(x_min-c1))
    pt1 = np.dot(r, [x_min, y, (x_min**2+y**2)]) * scale + shift[:3]
    for x in np.arange(x_min, x_max, 0.01):
        y = c2 - np.sqrt(c3*c3 - (x-c1)*(x-c1))
        pt2 = np.dot(r, [x, y, (x**2 + y**2)]) * scale + shift[:3]
        if x**2 + y**2 < 3.5:
            draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (204,102,255), width=5)
        pt1 = pt2

'''
Same as curve but can't modify that for historical preservation.
params:
    r: The rotation matrix the whole scene is rotated by
    r2: The rotation matrix that the inetersecting plane is to be rotated by
'''
def curveV2(draw, r, r2, scale = 200, shift = np.array([1000,1000,0]), h = 0.1):
    # Assume you start with the x-z plane
    orthogonal_vec = np.array([0,1,0])
    orthogonal_vec = np.dot(r2, orthogonal_vec)
    b = 1.5
    [thetax, thetay, thetaz] = orthogonal_vec
    c1 = -thetax/thetaz/2
    c2 = -thetay/thetaz/2
    c3 = np.sqrt(b + c1**2 + c2**2)
    x_min = max((c1 - abs(c3)),-np.sqrt(3.5))
    x_max = min((c1 + abs(c3)),np.sqrt(3.5))
    y = c2 + np.sqrt(c3*c3 - (x_min-c1)*(x_min-c1))
    pt1 = np.dot(r, [x_min, y, (x_min**2+y**2)]) * scale + shift[:3]
    for x in np.arange(x_min, x_max, 0.01):
        y = c2 + np.sqrt(c3*c3 - (x-c1)*(x-c1))
        pt2 = np.dot(r, [x, y, (x**2 + y**2)]) * scale + shift[:3]
        if x**2 + y**2 < 3.5 and 0.87 < x and x < 1.31:
            draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (204,102,255), width=5)
            #continue
        pt1 = pt2
    x = 0.87
    y = c2 + np.sqrt(c3*c3 - (x-c1)*(x-c1))
    pt1 = np.dot(r, [x, y, (x**2 + y**2)]) * scale + shift[:3]
    x = 1.31
    y = c2 + np.sqrt(c3*c3 - (x-c1)*(x-c1))
    pt2 = np.dot(r, [x, y, (x**2 + y**2)]) * scale + shift[:3]
    draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (2,220,2), width=5)
    width = 5
    draw.ellipse((pt1[0]-width,pt1[1]-width,pt1[0]+width,pt1[1]+width), fill = (255,0,0), outline = (255,0,0))
    draw.ellipse((pt2[0]-width,pt2[1]-width,pt2[0]+width,pt2[1]+width), fill = (255,0,0), outline = (255,0,0))
    x1 = 0.87
    y1 = c2 + np.sqrt(c3*c3 - (x1-c1)*(x1-c1))
    z1 = x1**2 + y1**2
    pt1 = np.array([x1,y1,z1])
    x2 = 1.31
    y2 = c2 + np.sqrt(c3*c3 - (x2-c1)*(x2-c1))
    z2 = x2**2+y2**2
    pt2 = np.array([x2,y2,z2])
    pt = h * pt1 + (1-h) * pt2
    #arrowV3(draw, r, np.array([0,0,0]), pt, scale = scale, rgb = (0,255,0))
    x = h * 0.87 + (1-h) * 1.31
    y = c2 + np.sqrt(c3*c3 - (x-c1)*(x-c1))
    #arrowV3(draw, r, np.array([0,0,0]), np.array([x, y, x**2 + y**2]), scale = scale, rgb = (204,102,255))

'''
Takes an x-z plane, translates it by translate parameter, rotates it by r2 and draws it.
params:
    r: The amount by which the object our plane is cutting is already rotated.
    r2: The amount by which the plane is to be rotated on top of r.
    translate: The amount by which the center of the plane is to be roated.
'''
def plane(draw, r, r2, scale = 200, shift = np.array([1000,1000,0]), translate = np.array([0,0,0])):
    extent = 2.8
    pln = np.array(
            [
                [-extent,0,0],
                [extent,0,0],
                [extent,0,extent*2],
                [-extent,0,extent*2]
            ]
        )
    pln = np.array([i-translate for i in pln]) # translate every point on the plane.
    rr = np.dot(r,r2)
    pln = np.dot(pln, np.transpose(rr))
    pln = np.array([i + np.dot(r,translate) for i in pln])
    pln = pln * scale + shift[:3]
    draw.polygon([(pln[0][0],pln[0][1]),(pln[1][0],pln[1][1]),(pln[2][0],pln[2][1]),(pln[3][0],pln[3][1])], (204,0,255,70))

'''
'''
def plot_weib_parabola(draw = None, p = 0.001):
    im_ind = 0
    if draw == None:
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
    pt1 = np.array([-1000.0, (1-p)*weib(-1000.0)+ p*-0.005*1000**2])
    axis(draw)
    for x in np.arange(-999.7,1000,.3):
        y1 = weib(x)
        y2 = -0.005 * x**2
        y = (1-p)*y1 + p*y2
        pt2 = np.array([x, y])
        draw.line((pt1[0]+1000, pt1[1]+1000, pt2[0]+1000, pt2[1]+1000), fill = "orange", width=3)
        pt1 = pt2
    if draw == None:
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

def plot_weib(draw = None):
    im_ind = 0
    if draw == None:
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
    pt1 = np.array([-1000.0, weib(-1000.0)])
    axis(draw)
    for x in np.arange(-999.7,1000,.3):
        pt2 = np.array([x, weib(x)])
        draw.line((pt1[0]+1000, pt1[1]+1000, pt2[0]+1000, pt2[1]+1000), fill = "orange", width=3)
        pt1 = pt2
    if draw == None:
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

def weib(x):
    k = 2.0
    lmb = 600.0
    t = abs(x)
    if x < 0:
        return (t/lmb)**(k-1)*np.exp(-(t/lmb)**k ) * 600
    else:
        return -(t/lmb)**(k-1)*np.exp(-(t/lmb)**k ) * 600

def axis(draw, r=np.eye(3)):
    x_axis = np.array([[0,1000,0],[2047,1000,0]])
    y_axis = np.array([[1000,0,0],[1000,2047,0]])
    z_axis = np.array([[1000,1000,-1000],[1000,1000,1000]])
    x_axis = np.dot(x_axis, np.transpose(r))
    y_axis = np.dot(y_axis, np.transpose(r))
    z_axis = np.dot(z_axis, np.transpose(r))
    draw.line((x_axis[0][0],x_axis[0][1],x_axis[1][0],x_axis[1][1]),fill="grey",width=4)
    draw.line((y_axis[0][0],y_axis[0][1],y_axis[1][0],y_axis[1][1]),fill="grey",width=4)
    draw.line((z_axis[0][0],z_axis[0][1],z_axis[1][0],z_axis[1][1]),fill="grey",width=4)

def new_vector_4d(r, v):
    v = v - np.array([1000, 1000, 0, 0]) #1000,1000 should go to 0,0. 
    v = v / scale
    v = np.dot(r,v)
    v = v * scale
    v = v + np.array([1000, 1000, 0, 0])
    return v

def OneDOptimizn(im_ind = 0):
    font = ImageFont.truetype("arial.ttf", 100)
    #im1 = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\SamuraiBest\\lightning2.jpg')
    im2 = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Misc\\toycar.png')
    im2.thumbnail((200,200), Image.ANTIALIAS)
    #for x in np.concatenate((np.arange(-700,700,40), np.arange(700,300,-30),np.arange(300,500,20),np.arange(500,450,-5),np.arange(445,452,1)),axis=0):
    #for x in np.arange(700,-90,-10):
    x1 = -440
    for x in np.arange(0,1):
        im = Image.new("RGBA", (2048, 2048), (0,0,0))
        #im.paste(im1,(0,0))
        draw = ImageDraw.Draw(im, 'RGBA')
        #draw.text((1042, 48), "Debt you owe", font=font, fill = (120,80,200))
        slope = (weib(x+1e-5)-weib(x-1e-5))/1e-5/2
        angle = -np.arctan(slope)*180/np.pi
        angle2 = -np.arctan((weib(x1-90+1e-5)-weib(x1-90-1e-5))/1e-5/2)*180/np.pi
        im3 = im2.rotate(angle)
        im4 = im2.rotate(angle2)
        im4 = im4.point(lambda p: p*0.6)
        #im.paste(im2,(1000 + int(-90)-100, 1000 + int(weib(-90))-100))
        #im.paste(im2,(1000 + int(x)-100, 1000 + int(weib(x))-100))        
        #pasteImage(im4,im,(1000 + int(x1-90)-100, 1000 + int(weib(x1-90))-100))
        #pasteImage(im3,im,(1000 + int(x)-100, 1000 + int(weib(x))-100))
        #draw.line((1000 + x1, 1000, 1000 + x1, 1000 + weib(x1)), fill="green", width=5)
        curve_pt = [1000 + x1, 1000 + weib(x1)]
        #draw.ellipse((curve_pt[0]-7,curve_pt[1]-7,curve_pt[0]+7,curve_pt[1]+7), fill = "red", outline = "red")
        slope = (weib(x1 + 1e-5)-weib(x1 - 1e-5))/1e-5/2
        angle = -np.arctan(slope) * 180 / np.pi
        im3 = im2.rotate(angle)
        #im.paste(im3,(1000+int(x1)-100,1000+int(weib(x1))-100))
        #draw.line((1000 + x1, 1000, 1000 + x1, 1000 + weib(x1)), fill="green", width=5)
        curve_pt = [1000 + x1, 1000 + weib(x1)]
        #draw.ellipse((curve_pt[0]-7,curve_pt[1]-7,curve_pt[0]+7,curve_pt[1]+7), fill = "red", outline = "red")
        plot_weib_parabola(draw, (im_ind/30.0)**2)
        #sc = 0.0
        #drawDoubleArrowRevVer(draw, (1000, 1000 + weib(x1-90)), (weib(x1-90)-weib(x)))
        #draw.line((1000,1000+weib(x1-90),1000+x1-90,1000+weib(x1-90)),fill="white")
        #draw.line((1000,1000+weib(x),1000+x,1000+weib(x)),fill="white")
        #drawDoubleArrow(draw, (1000+x1-90, 1000), -(x1-90-x))
        im_math = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Math\\delX.png')
        #pasteImage(im_math,im,(1500,350))
        im_math = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Math\\delY.png')
        #pasteImage(im_math,im,(1500,280))
        #draw.line((1477,352,1615,352),fill="white",width=3)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1


'''
Draws a double arrow between two points.
'''
def drawDoubleArrow(draw, xy, span):
    arrow_size = min(40,span)
    draw.line((xy[0],xy[1],xy[0],xy[1]+arrow_size),fill="white",width=3)
    draw.line((xy[0],xy[1]+arrow_size/2,xy[0]+arrow_size/2,xy[1]),fill="white",width=3) #first diagonal
    draw.line((xy[0],xy[1]+arrow_size/2,xy[0]+arrow_size/2,xy[1]+arrow_size),fill="white",width=3) #first diagonal
    draw.line((xy[0]+span,xy[1]+arrow_size/2,xy[0]+span-arrow_size/2,xy[1]),fill="white",width=3) #second diagonal
    draw.line((xy[0]+span,xy[1]+arrow_size/2,xy[0]+span-arrow_size/2,xy[1]+arrow_size),fill="white",width=3) #second diagonal
    draw.line((xy[0],xy[1]+arrow_size/2,xy[0]+span,xy[1]+arrow_size/2),fill="white",width=3)
    draw.line((xy[0]+span,xy[1],xy[0]+span,xy[1]+arrow_size),fill="white",width=3)

def drawDoubleArrowVer(draw, xy, span):
    arrow_size = min(40,span)
    draw.line((xy[0],xy[1],xy[0]-arrow_size,xy[1]),fill="white", width=3)
    draw.line((xy[0]-arrow_size/2,xy[1],xy[0],xy[1]-arrow_size/2),fill="white", width=3) #first diagonal
    draw.line((xy[0]-arrow_size/2,xy[1],xy[0]-arrow_size,xy[1]-arrow_size/2),fill="white", width=3) #first diagonal
    draw.line((xy[0]-arrow_size/2,xy[1]-span,xy[0],xy[1]-span+arrow_size/2),fill="white", width=3) #second diagonal
    draw.line((xy[0]-arrow_size/2,xy[1]-span,xy[0]-arrow_size,xy[1]-span+arrow_size/2),fill="white",width=3) #second diagonal
    draw.line((xy[0]-arrow_size/2,xy[1],xy[0]-arrow_size/2,xy[1]-span),fill="white",width=3)
    draw.line((xy[0],xy[1]-span,xy[0]-arrow_size,xy[1]-span),fill="white",width=3)

def drawDoubleArrowRevVer(draw, xy, span):
    arrow_size = 40
    draw.line((xy[0],xy[1],xy[0]-arrow_size,xy[1]), fill = "white",width=3)
    draw.line((xy[0]-arrow_size/2,xy[1],xy[0],xy[1]+arrow_size/2), fill = "white",width=3)
    draw.line((xy[0]-arrow_size/2,xy[1],xy[0]-arrow_size,xy[1]+arrow_size/2), fill = "white",width=3)
    draw.line((xy[0]-arrow_size/2,xy[1],xy[0]-arrow_size/2,xy[1]+70), fill = "white",width=3)
    #
    draw.line((xy[0],xy[1]-span,xy[0]-arrow_size,xy[1]-span), fill = "white", width=3)
    draw.line((xy[0]-arrow_size/2,xy[1]-span,xy[0],xy[1]-span-arrow_size/2), fill = "white", width=3)
    draw.line((xy[0]-arrow_size/2,xy[1]-span,xy[0]-arrow_size,xy[1]-span-arrow_size/2), fill = "white", width=3)
    draw.line((xy[0]-arrow_size/2,xy[1]-span,xy[0]-arrow_size/2,xy[1]-span-70), fill = "white",width=3)

'''
Pastes a small image onto a bigger image at the coordinates specified by posn.
'''
def pasteImage(img, bigim, posn, whiteBackground = False, color = None):
    pixdata = img.load()
    width, height = img.size
    bw,bh = bigim.size
    mainpixdata = bigim.load()
    for y in xrange(height):
        for x in xrange(width):
            if x < bw - posn[0] and y < bh - posn[1] and x + posn[0] > 0 and y + posn[1] > 0:
                if sum(pixdata[x, y][:3]) != 0 and not (whiteBackground and sum(pixdata[x, y][:3]) == 255 * 3):
                    if color is None:
                        mainpixdata[x+posn[0], y+posn[1]] = pixdata[x,y]
                    else:
                        mainpixdata[x+posn[0], y+posn[1]] = color



def get_pixels(impath = 'C:\\Users\\rohit\\Desktop\Tetroid.PNG'):
    im = Image.open(impath)
    pixdata = im.load()

    width, height = im.size

    s = {}
    for i in range(height):
        for j in range(width):
            if pixdata[j,i] in s:
                s[pixdata[j,i]] += 1
            else:
                s[pixdata[j,i]] = 1
    print(sorted(dict.items(), key=lambda kv: kv[1], reverse=True))



'''
Obtains RGB values for a heatmap of values between min and max.
'''
def heat_rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return (r, g, b)

'''
'''
def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v


