from PIL import Image, ImageDraw
from colour import Color
import numpy as np
from HyperCube import *
from scipy.spatial import ConvexHull


def tst():
    for j in range(0,50):
        im = Image.new("RGB", (2048, 2048), (1,1,1))
        draw = ImageDraw.Draw(im)

        theta = -j/50.0 * np.pi*1.5
        phi = -j/50.0 * np.pi*1.5
        alp = -j/50.0 * np.pi*1.5

        r1 = np.array(
        [
            [np.cos(theta), -np.sin(theta),0],
            [np.sin(theta), np.cos(theta),0],
            [0,0,1]
        ])
        r2 = np.array(
        [
            [1,0,0],
            [0, np.cos(phi), -np.sin(phi)],
            [0,np.sin(phi), np.cos(phi)]
        ])
        r3 = np.array(
        [
            [np.cos(alp), 0, -np.sin(alp)],
            [0, 1, 0],
            [np.sin(alp), 0, np.cos(alp)]
        ])

        r = np.dot(r3,np.dot(r1,r2))
        ## Edges
        edges = np.array([
            [[0,0,0], [0,1,0]],
            [[0,1,0], [0,1,1]],
            [[0,0,1], [0,1,1]],
            [[0,0,0], [0,0,1]],

            [[1,0,0], [1,1,0]],
            [[1,1,0], [1,1,1]],
            [[1,0,1], [1,1,1]],
            [[1,0,0], [1,0,1]],

            [[0,0,1], [1,0,1]],
            [[0,1,1], [1,1,1]],
            [[0,0,0], [1,0,0]],
            [[0,1,0], [1,1,0]]
        ])

        i = 0
        for e in edges:
            v1 = np.dot(r, e[0])
            v2 = np.dot(r, e[1])
            [v1x,v1y] = 1000 + 500 * v1[:2] # Projection on x-y plane
            [v2x,v2y] = 1000 + 500 * v2[:2] # Projection on x-y plane
            if is_inside(r, v1 - np.array([0,0,0.5]) ) or is_inside(r, v2 - np.array([0,0,0.5])):
                width = 1
            else:
                width = 3

            if i < 8:
                draw.line((v1x, v1y, v2x, v2y), fill='orange', width=width)
            else:
                draw.line((v1x, v1y, v2x, v2y), fill='orange', width=width)
            i = i + 1

        ## Vertices
        vertices = np.array([
            [0,0,0],
            [0,1,0],
            [0,1,1],
            [0,0,1],
            [1,0,0],
            [1,1,0],
            [1,1,1],
            [1,0,1]
        ])

        for v in vertices:
            vv = np.dot(r,v)
            [vx,vy] = 1000 + 500 * vv[:2] # Projection on y-z plane
            if not is_inside(r, vv - np.array([0,0,0.5])):
                draw.ellipse( (vx-3,vy-3,vx+3,vy+3), fill = 'red', outline = 'red')
        im.save('Images\\RotatingCube\\im' + str(j) + '.bmp')


def BiggerCube(im_ind = 12):
    for j in range(3,4):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        #draw = cube_body_diagonal_scene(draw)
        writeText(draw)
        theta = j/20.0 * np.pi*2
        phi = j/20.0 * np.pi*2
        alp = j/20.0 * np.pi*2
        r1 = np.array(
        [
            [np.cos(theta), -np.sin(theta),0],
            [np.sin(theta), np.cos(theta),0],
            [0,0,1]
        ])
        r2 = np.array(
        [
            [1,0,0],
            [0, np.cos(phi), -np.sin(phi)],
            [0,np.sin(phi), np.cos(phi)]
        ])
        r3 = np.array(
        [
            [np.cos(alp), 0, -np.sin(alp)],
            [0, 1, 0],
            [np.sin(alp), 0, np.cos(alp)]
        ])
        r = np.dot(r3,np.dot(r1,r2))
        #r = general_rotation(np.array([-1,1,0]),-np.arccos(1/3**0.5)*j/30.0)
        r = rotation(3,np.pi*2*3/20.0)
        #r = general_rotation(np.array([-1,1,0]), -np.arccos(1/3**0.5))
        ## Vertices
        vertices = [Base3(i) for i in range(27)]
        rotated_vertices = np.transpose(np.dot(r,np.transpose(vertices))) * 300 + 1000

        for i in range(len(vertices)):
            draw.ellipse( (rotated_vertices[i][0]-11,rotated_vertices[i][1]-11,rotated_vertices[i][0]+11,rotated_vertices[i][1]+11), fill = "red", outline = "red")
            if vertices[i][0] < 2 and i + 1 <= len(vertices) - 1: 
                v1 = rotated_vertices[i]
                v2 = rotated_vertices[i + 1]
                draw.line((v1[0], v1[1], v2[0], v2[1]), fill="yellow", width=2)
            if vertices[i][1] < 2 and i + 3 <= len(vertices) - 1:
                v1 = rotated_vertices[i]
                v2 = rotated_vertices[i + 3]
                draw.line((v1[0], v1[1], v2[0], v2[1]), fill="yellow", width=2)
            if vertices[i][2] < 2 and i + 9 <= len(vertices) - 1:
                v1 = rotated_vertices[i]
                v2 = rotated_vertices[i + 9]
                draw.line((v1[0], v1[1], v2[0], v2[1]), fill="yellow", width=2)            
        '''
        v1 = rotated_vertices[0]
        v2 = rotated_vertices[26]
        for v in vertices:
            vv = np.dot(r,v)
            [vx,vy] = 1000 + 300 * vv[:2] # Projection on x-y plane
            draw.ellipse( (vx-5,vy-5,vx+5,vy+5), fill = 'red', outline = 'red')
        draw.polygon([(rotated_vertices[11][0], rotated_vertices[11][1]), (rotated_vertices[5][0], rotated_vertices[5][1]), (rotated_vertices[7][0], rotated_vertices[7][1]), (rotated_vertices[15][0], rotated_vertices[15][1]),(rotated_vertices[21][0], rotated_vertices[21][1]),(rotated_vertices[19][0], rotated_vertices[19][1])], (120,80,200,80))
        for vv in [5,7,11,13,15,19,21]:
            ver = np.dot(r,vertices[vv])
            [vx,vy] = 1000 + 300 * ver[:2]
            draw.ellipse( (vx-11,vy-11,vx+11,vy+11), fill = (120,80,200), outline = (120,80,200))
        first_intersection = np.dot(r, np.array([.3333,.3333,.3333]))*300 + 1000    
        draw.ellipse( (first_intersection[0]-10,first_intersection[1]-10,first_intersection[0]+10,first_intersection[1]+10), fill = (0,0,0))
        draw.line((v1[0], v1[1], v2[0], v2[1]), fill="green", width=7)
        draw.polygon([(rotated_vertices[17][0], rotated_vertices[17][1]), (rotated_vertices[23][0], rotated_vertices[23][1]), (rotated_vertices[25][0], rotated_vertices[25][1])], (42,106,255,80))
        for vv in [17,23,25]:
            ver = np.dot(r,vertices[vv])
            [vx,vy] = 1000 + 300 * ver[:2]
            draw.ellipse( (vx-11,vy-11,vx+11,vy+11), fill = (42,106,255), outline = (42,106,255))
        '''
        draw.polygon([(rotated_vertices[1][0], rotated_vertices[1][1]), (rotated_vertices[3][0], rotated_vertices[3][1]), (rotated_vertices[9][0], rotated_vertices[9][1])], (120,80,200,100))
        for vv in [1, 3, 9]:
            ver = np.dot(r,vertices[vv])
            [vx,vy] = 1000 + 300 * ver[:2]
            draw.ellipse( (vx-11,vy-11,vx+11,vy+11), fill = (120,80,200), outline = (120,80,200))
        '''
        draw.polygon([(rotated_vertices[2][0], rotated_vertices[2][1]), (rotated_vertices[6][0], rotated_vertices[6][1]), (rotated_vertices[18][0], rotated_vertices[18][1])], (68,193,195,80))
        for vv in [2, 6, 18]:
            ver = np.dot(r,vertices[vv])
            [vx,vy] = 1000 + 300 * ver[:2]
            draw.ellipse( (vx-11,vy-11,vx+11,vy+11), fill = (68,193,195), outline = (68,193,195))
        draw.polygon([(rotated_vertices[8][0], rotated_vertices[8][1]), (rotated_vertices[20][0], rotated_vertices[20][1]), (rotated_vertices[24][0], rotated_vertices[24][1])], (192,255,0,80))
        for vv in [8, 20, 24]:
            ver = np.dot(r,vertices[vv])
            [vx,vy] = 1000 + 300 * ver[:2]
            draw.ellipse( (vx-11,vy-11,vx+11,vy+11), fill = (192,255,0), outline = (192,255,0))
        '''
        first_intersection = np.dot(r, np.array([1.3333,1.3333,1.3333]))*300 + 1000
        second_intersection = np.dot(r, np.array([1.6666,1.6666,1.6666]))*300 + 1000     
        fourthTriangle(draw, rotated_vertices,second_intersection)
        thirdTriangle(draw, rotated_vertices,first_intersection)
        hexagon(draw, rotated_vertices, vertices, r)
        secondTriangle(draw,rotated_vertices, im_ind - 8)        
        #createCircle(draw, (rotated_vertices[26] - rotated_vertices[0]), vertices, r)
        draw.line((rotated_vertices[0][0], rotated_vertices[0][1], rotated_vertices[26][0], rotated_vertices[26][1]) , fill = "green", width=5)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

def firstTriangle(draw, rotated_vertices):
    for ind in [1,3,9]:
        extent = rotated_vertices[ind][:2]
        for_polygon.append( (extent[0], extent[1]))
    draw.polygon(for_polygon, (120,80,200,100))

def secondTriangle(draw, rotated_vertices, indx):
    for_polygon = []
    for ind in [4,10,12,2,6,18]:
        [vx,vy,vz] = rotated_vertices[ind]
        draw.ellipse( (vx-11,vy-11,vx+11,vy+11), fill = (200,80,100))
    
    for ind in [(2,6),(6,18),(2,18)]:
        pt1 = rotated_vertices[ind[0]][:2]
        pt2 = rotated_vertices[ind[1]][:2]
        slope = pt2 - pt1
        factor = (10.0 - indx)/20.0
        factor = max(factor,0)
        factor = 0
        x1 = pt2 - slope * factor
        x2 = pt1 + slope * factor
        for_polygon.append([x1[0], x1[1]])
        for_polygon.append([x2[0], x2[1]])
    hull = ConvexHull(for_polygon).vertices
    poly = [(for_polygon[i][0],for_polygon[i][1]) for i in hull]
    draw.polygon(poly, (200,80,100,100))

def thirdTriangle(draw, rotated_vertices, center):
    for_polygon = []
    for vv in [20, 8, 24]:
        ver = center + (rotated_vertices[vv]  - center) * 1.0
        [vx,vy] = ver[0:2]
        for_polygon.append((vx,vy))
        draw.ellipse( (vx-11,vy-11,vx+11,vy+11), fill = (255,255,255), outline = (255,255,255))
    draw.polygon(for_polygon, (255,255,255,100))

def fourthTriangle(draw, rotated_vertices, center):
    for_polygon = []
    for vv in [17, 23, 25]:
        ver = center + (rotated_vertices[vv]  - center) * 1.0
        [vx,vy] = ver[0:2]
        for_polygon.append((vx,vy))
        draw.ellipse( (vx-11,vy-11,vx+11,vy+11), fill = (54,209,46), outline = (54,209,46))
    draw.polygon(for_polygon, (54,209,46,100))

def hexagon(draw, rotated_vertices, vertices, r, extent = 1.0):
    #draw.polygon([(rotated_vertices[11][0], rotated_vertices[11][1]), (rotated_vertices[5][0], rotated_vertices[5][1]), (rotated_vertices[7][0], rotated_vertices[7][1]), (rotated_vertices[15][0], rotated_vertices[15][1]),(rotated_vertices[21][0], rotated_vertices[21][1]),(rotated_vertices[19][0], rotated_vertices[19][1])], (255,255,51,100))
    [vx,vy] = rotated_vertices[13][:2]
    draw.ellipse( (vx-11,vy-11,vx+11,vy+11), fill = (255,255,51), outline = (255,255,51))
    for_polygon = []
    for vv in [5,7,11,15,19,21]:
        ver1 = rotated_vertices[13]
        ver2 = rotated_vertices[vv]
        ver = ver1 + (ver2 - ver1) * extent
        [vx,vy] = ver[0:2]
        for_polygon.append([vx,vy])
        draw.ellipse((vx-11,vy-11,vx+11,vy+11), fill = (255,255,51), outline = (255,255,51))
    hull = ConvexHull(for_polygon).vertices
    poly = [(for_polygon[i][0],for_polygon[i][1]) for i in hull]
    draw.polygon(poly, (255,255,51,100))    
    ''' pt1 = np.dot(r,vertices[5]) * 300 + 1000
    for j in range(51):
        theta = np.pi * 2 * j / 50.0
        r1 = general_rotation(vec,theta)
        r2 = np.dot(r1,r)
        pt2 = np.dot(r2,vertices[5]) * 300 + 1000
        #draw.ellipse( (pt2[0]-5,pt2[1]-5,pt2[0]+5,pt2[1]+5), fill = (68,193,195), outline = (68,193,195))
        #draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill=(200,80,100), width=5)
        draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill="white", width=5)
        pt1 = pt2 '''

def createCircle(draw, vec, vertices, r):
    for ind in [2,6,18]:
        center = np.dot(r,np.array([.666666,.666666,.66666])) * 300 + 1000
        rim = np.dot(r,vertices[ind]) * 300 + 1000
        #draw.line((center[0], center[1], rim[0], rim[1]), fill = (200,80,100), width = 3)
    pt1 = np.dot(r,vertices[2]) * 300 + 1000
    for j in range(51):
        theta = np.pi * 2 * j / 50.0
        r1 = general_rotation(vec,theta)
        r2 = np.dot(r1,r)
        pt2 = np.dot(r2,vertices[2]) * 300 + 1000
        #draw.ellipse( (pt2[0]-5,pt2[1]-5,pt2[0]+5,pt2[1]+5), fill = (68,193,195), outline = (68,193,195))
        #draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill=(200,80,100), width=5)
        draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill="white", width=5)
        pt1 = pt2
    pt1 = np.dot(r,vertices[4]) * 300 + 1000
    for j in range(51):
        theta = np.pi * 2 * j / 50.0
        r1 = general_rotation(vec,theta)
        r2 = np.dot(r1,r)
        pt2 = np.dot(r2,vertices[4]) * 300 + 1000
        #draw.ellipse( (pt2[0]-5,pt2[1]-5,pt2[0]+5,pt2[1]+5), fill = (68,193,195), outline = (68,193,195))
        #draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill=(200,80,100), width=5)
        draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill="white", width=5)
        pt1 = pt2

def writeText(draw):
    font = ImageFont.truetype("arial.ttf", 100)
    font_small = ImageFont.truetype("arial.ttf", 60)
    draw.text((267, 1540), "(1 +a +6a +7a +6a +3a + a )", font=font, fill = "orange")
    draw.text((443, 1540), "3", font=font, fill = (120,80,200))
    draw.text((641, 1540), "6", font=font, fill = (200,80,100))
    draw.text((840, 1540), "7", font=font, fill = (255,255,0))
    draw.text((1040, 1540), "6", font=font, fill = (255,255,255))
    draw.text((1240, 1540), "3", font=font, fill = (54,209,46))
    draw.text((60, 83), "(1 + a + a )", font=font, fill = "orange")
    draw.text((745, 1535), "2", font=font_small, fill = "orange")
    draw.text((948, 1535), "3", font=font_small, fill = "orange")
    draw.text((1140, 1535), "4", font=font_small, fill = "orange")
    draw.text((1340, 1535), "5", font=font_small, fill = "orange")
    draw.text((1511, 1535), "6", font=font_small, fill = "orange")
    draw.text((480, 80), "2", font=font_small, fill = "orange")
    draw.text((545, 72), "3", font=font_small, fill = "orange")
    #draw.text((990, 790), "(1,1,1)", font=font, fill = "white")

def General3DCube(numTerms, im_ind = 0, pos = [300,700,0]):
    for j in range(30,31):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        r = rotation(3, j/80.0 * np.pi*2)
        ## Vertices
        vertices = [GeneralBase(i,numTerms) for i in range(numTerms**3)]
        rotated_vertices = np.transpose(np.dot(r,np.transpose(vertices))) * 150 + pos
        colors = [(120,80,200),(200,80,100),(0,255,128),(0,0,255),(255,153,31),(51,153,255),(0,255,0),(255,255,255),(255,255,0),(255,153,153),(174,87,209),(100,149,237),(210,105,30),(176,196,202)]
        # Draw edges.
        for i in range(len(vertices)):
            for dim in range(3):
                if vertices[i][dim] < (numTerms - 1) and i + numTerms**dim <= len(vertices) - 1: 
                    v1 = rotated_vertices[i]
                    v2 = rotated_vertices[i + numTerms**dim]
                    draw.line((v1[0], v1[1], v2[0], v2[1]), fill="yellow", width=2)
        for v in rotated_vertices:
            draw.ellipse((v[0]-5, v[1]-5, v[0]+5, v[1]+5), fill = 'red', outline = 'red')
        for power in range(1, (numTerms-1)*3):
            rgb = colors[(power-1)%14]
            rgba = colors[(power-1)%14] + (100,)
            #rgb = (255,255,255)
            #rgba = (255,255,255,100)
            sqr1 = rotated_vertices[np.array(range(len(vertices)))[np.array([sum(i)==power for i in vertices])]]
            hull = ConvexHull([i[:2] for i in sqr1]).vertices
            poly = [(sqr1[i][0],sqr1[i][1]) for i in hull]
            draw.polygon(poly, rgba)
            for vv in sqr1:
                [vx,vy] = vv[:2]
                draw.ellipse( (vx-11,vy-11,vx+11,vy+11), fill = rgb, outline = rgb)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

def GeneralBase(n, b):
    res = np.zeros(3)
    indx = 0
    while(n > 0):
        res[indx] = (n % b)
        indx = indx + 1
        n = n / b
    return res

def Base3(n):
    res = np.zeros(3)
    indx = 0
    while(n > 0):
        res[indx] = (n % 3)
        indx = indx + 1
        n = n / 3
    return res

def prnt(j):
    for i in range(27):
        if sum(vertices[i])==j:
            print i

