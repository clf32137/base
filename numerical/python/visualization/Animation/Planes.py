import numpy as np
import math
from Sphere import *
from CubeObjects import *
from scipy.spatial import ConvexHull

def plane(im_ind = 0, rgba = (120,80,200,150)):
    j = 4
    r = rotation(3, 2 * np.pi*j/30.0)
    r1 = np.eye(4)
    r1[:3,:3] = r
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    render_scene_4d_axis(draw, r1, 4)
    poly = np.array(
            [
                [0,0,0],
                [0,1.0,1.0],
                [1.0,0,1.0]
            ]
        )
    np.dot(np.transpose(poly),np.array([1,1,1]))
    poly = np.array([np.dot(r,i)*scale+shift[:3] for i in poly])
    centroid = np.dot(np.transpose(poly),np.array([1,1,1])) / 3.0
    poly = np.array([(centroid + (i - centroid) * im_ind) for i in poly])
    poly = [(i[0],i[1]) for i in poly]
    draw.polygon(poly, rgba)
    arrowV1(draw, r, np.array([0,0,0]), np.array([1,1,0]), (204,102,255))
    arrowV1(draw, r, np.array([0,0,0]), np.array([-1,-1,0]), (204,102,255))
    arrowV1(draw, r, np.array([0,0,0]), np.array([-1,1,0]), (147,112,219))
    arrowV1(draw, r, np.array([0,0,0]), np.array([1,-1,0]), (147,112,219))
    drawLine(draw, r, np.array([1,0,0]), np.array([1,0,1]))
    drawLine(draw, r, np.array([0,1,0]), np.array([0,1,1]))
    drawLine(draw, r, np.array([0,0,1]), np.array([0,1,1]))
    drawLine(draw, r, np.array([0,0,1]), np.array([1,0,1]))
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    im_ind = im_ind + 1

def drawLine(draw, r, pt1, pt2):
    pt1 = np.dot(r, pt1) * scale + shift[:3]
    pt2 = np.dot(r, pt2) * scale + shift[:3]
    draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (255,102,55,100), width = 3)

'''
A visualization of a plane and its gradient.
'''
def threePointPlane(j = 4, im_ind = 0):
    font = ImageFont.truetype("arial.ttf", 75)
    #dimn = (np.cos(im_ind * np.pi /10.0))
    #dimn = 1 + 10.0 * np.sin(im_ind * np.pi /60.0)
    #if abs(dimn) < 0.1:
    #    dimn = np.sign(dimn)*0.1    
    [a,b,c] = np.array([2.5, 2.5, -2.5*10.0/10.0])*410/200
    #b = 2.5 + 2 * np.tan(im_ind * (np.pi+1e-3) / 30.0)
    rot = general_rotation(np.array([0,0,1]), np.pi/40.0 * 0 )
    r = rotation(3, 2 * np.pi*j/30.0)
    r = np.dot(r, rot)
    r1 = np.eye(4)
    r1[:3,:3] = r
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    render_scene_4d_axis(draw, r1, 4)
    pt1 = np.dot(r,np.array([a,0,0])) * scale + shift[:3]
    pt2 = np.dot(r,np.array([0,b,0])) * scale + shift[:3]
    pt3 = np.dot(r,np.array([0,0,c])) * scale + shift[:3]
    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(200,80,100), width = 3)
    draw.polygon([(pt1[0],pt1[1]),(pt2[0],pt2[1]),(pt3[0],pt3[1])], (200,80,100,100))
    draw.line((shift[0],shift[1],pt3[0],pt3[1]), fill = "yellow",width=7)
    draw.line((shift[0],shift[1],pt1[0],pt1[1]), fill = "yellow",width=7)
    draw.line((shift[0],shift[1],pt2[0],pt2[1]), fill = "yellow",width=7)
    #draw_circle(draw, r)
    #project_circle_on_plane(draw, r, plane = np.array([a,b,c]))
    grad = np.array([c/a, c/b, 0])
    grad = grad / np.sqrt(sum(grad**2))
    #arrowV1(draw,r,np.array([1,1,0]), np.array([1,1,0]) - grad, (204,102,255))
    polyg = []
    edge_z = c * (1 - (1-grad[0])/a - (1-grad[1])/b)
    center_z = c * (1 - 1/a - 1/b)
    for i in [[1,1,0],[1-grad[0],1-grad[1],0],[1-grad[0],1-grad[1],edge_z],[1,1,center_z]]:
        pt = np.dot(r,np.array(i)) * scale + shift[:3]
        polyg.append([pt[0],pt[1]])
    #hull = ConvexHull(polyg).vertices
    hull = range(len(polyg))
    polyg = [(polyg[i][0], polyg[i][1]) for i in hull]
    #drawXYGrid(draw, r)
    #for i in range(len(polyg)):
    #    draw.line((polyg[i][0], polyg[i][1], polyg[(i+1)%len(polyg)][0], polyg[(i+1)%len(polyg)][1]), fill = (204, 102, 255, 150), width = 4)
    #draw.polygon(polyg, (204, 102, 255, 70))
    pt_1 = np.array([1.1,1.1,0])*410/200
    pt = np.dot(r,pt_1)*scale + shift[:3]
    theta = np.pi/4 - np.pi*2.0*im_ind/15.0
    pt_2 = pt_1 + 1.1*np.array([np.cos(theta), np.sin(theta), 0])
    arrowV1(draw, r, pt_1, pt_2)
    width = 3*(0.0 % 3) + 10
    draw.ellipse((pt[0]-width,pt[1]-width,pt[0]+width,pt[1]+width),fill=(102,255,51))
    im = im.rotate(180)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    draw = ImageDraw.Draw(im, 'RGBA')
    #if im_ind < 43:
    #    writeStaggeredText("Question: Why is the gradient the direction of \n\nmaximum ascent?", draw, im_ind)
    #else:
    #    writeStaggeredText("In other words, why does a function increase \nthe most in the direction of its gradient?", draw, im_ind-43)
    draw.text((830, 160), 'z', font=font)
    #draw.text((935,545), '(0,0,c)', font=font)
    #draw.text((1265,805), '(a,0,0)', font=font)
    #draw.text((465,1075), '(0,b,0)', font=font)
    #draw_equation(draw, im_ind)
    writeLatex(im,'z = c \\left( 1 - \\frac{x}{a} - \\frac{y}{b} \\right)',(1268,293),(253,253,253))
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')

def draw_equation(draw, im_ind = 0):
    font = ImageFont.truetype("arial.ttf", 75)
    draw.text((1277,273),"x + y + z", font=font)
    x_below = np.array([1270,340])
    y_below = np.array([1388,360])
    z_below = np.array([1509,360])
    x_above = np.array([1270,295])
    y_above = np.array([1388,295])
    z_above = np.array([1509,295])
    a_pos = np.array([1293,829])
    b_pos = np.array([558,1085])
    c_pos = np.array([1089,568])
    phantom_a = a_pos + (x_below - a_pos) * im_ind / 10.0
    phantom_b = b_pos + (y_below - b_pos) * im_ind / 10.0
    phantom_c = c_pos + (z_below - c_pos) * im_ind / 10.0
    draw.text((x_above[0], x_above[1]-10), '_',font=font)
    draw.text((y_above[0], y_above[1]-10), '_',font=font)
    draw.text((z_above[0], z_above[1]-10), '_',font=font)
    draw.text((x_below[0],x_below[1]), 'a', font=font)
    draw.text((y_below[0],y_below[1]), 'b', font=font)
    draw.text((z_below[0],z_below[1]), 'c', font=font)
    draw.text((1600,340),'= 1', font=font)


def twoDimensionalFunction(j=0, im_ind=0, shift=np.array([1000,1000,0]), scale = 200):
    font = ImageFont.truetype("arial.ttf", 75)
    font_big = ImageFont.truetype("arial.ttf", 110)
    r = rotation(3, 2 * np.pi*j/30.0)
    rot = general_rotation(np.array([0,0,1]), np.pi/40.0 * 0 )
    r = np.dot(r, rot)
    r1 = np.eye(4)
    r1[:3,:3] = r
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    im_laz = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\Objects\lazer\lazer_dot' + str(im_ind % 2) + '.png')
    render_scene_4d_axis(draw, r1, 4)
    [a,b,c] = [10.0/10.0*2.5, 10.0/10.0*2.5, 2.5]
    pt1 = np.dot(r,np.array([a,0,0])) * scale + shift[:3]
    pt2 = np.dot(r,np.array([0,b,0])) * scale + shift[:3]
    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(200,80,100), width = 3)
    draw.ellipse((pt1[0]-10,pt1[1]-10,pt1[0]+10,pt1[1]+10),fill="yellow")
    draw.ellipse((pt2[0]-10,pt2[1]-10,pt2[0]+10,pt2[1]+10),fill="yellow")
    #drawDoubleArrow(draw, shift[:2]-np.array([-5,40]), (a)*scale-5)
    p1, p2 = 0.1, 0.7
    inter_1 = pt1 + (pt2-pt1)*p1
    inter_2 = pt1 + (pt2-pt1)*p2
    intersecnx = min(inter_1[0], inter_2[0])
    intersecny = min(inter_1[1], inter_2[1])
    #draw.line((intersecnx, intersecny, inter_1[0], inter_1[1]), fill="orange", width=5)
    #draw.line((intersecnx, intersecny, inter_2[0], inter_2[1]), fill="orange", width=5)
    pos = np.array([1.25,0])*scale+shift[:2]
    #draw.text((pos[0],pos[1]),'x',font=font,fill='yellow')
    x = (pos - shift[:2]) / scale
    y = b*(1-x/a)
    y_pos = y * scale + shift[:2]
    draw.line((pos[0],pos[1],pos[0],y_pos[0]),fill='orange')
    im = im.rotate(180)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    draw = ImageDraw.Draw(im, 'RGBA')
    #drawDoubleArrowVer(draw, shift[:2]+np.array([0,0.25*scale]), (b)*scale+5)
    linear_path = np.array([0,2047]) + im_ind / 30.0 * (np.array([2047,0])  - np.array([0,2047]))
    ##pasteImage(im_laz, im, (linear_path[0] - 45.0, linear_path[1]- 60.0), True)
    ##draw.line((0, 2047, linear_path[0], linear_path[1]), fill = (255,255,0), width = 3)
    ##writeLatex(im, 'a', coordn = (1250,1111), color = (120,80,200))
    ##draw.text((1234,1100), 'a', (255,255,255), font=font)
    ##draw.text((1520,952), '(a,0)', (255,255,0), font=font)
    ##draw.text((902,729), 'b', (255,255,255), font=font)
    ##draw.text((825,470), '(0,b)', (255,255,0), font=font)
    move = 32 * 5.0
    move2 = 21*3.2
    a_pos = np.array([1234,1100]) + 10.0/10.0 * (np.array([1455,520])-np.array([1234,1100]))
    b_pos = np.array([902,729]) + 10.0/10.0 * (np.array([1455+130,520])-np.array([902,729])) + np.array([-move,0])
    b_pos = b_pos + (np.array([1554,480]) - b_pos)*21/20.0
    draw.text((1455+move*1.2+move2,451), 'x', (255,255,255), font=font)
    draw.text((1455+move*1.2+move2,460), '_', (255,255,255), font=font)
    draw.text((a_pos[0]+move*1.2+move2,a_pos[1]), 'a', (255,255,255), font=font)
    draw.text((1455+130-move,451 + move2/4.0), 'y', (255,255,255), font=font)
    draw.text((1455+65+move/2.0+move2,480), '-', (255,255,255), font=font)
    draw.text((b_pos[0],b_pos[1]), 'b', (255,255,255), font=font)
    draw.text((1455+188-move,490), '= ', (255,255,255), font=font)
    draw.text((1552+move2,503-move2/6), '1', (255,255,255), font=font)
    draw.text((1604, 477), '(', font=font_big)
    draw.text((1769, 477), ')', font=font_big)
    draw.text((1418, 660), 'dy', font=font)
    draw.text((1418, 660+15), '__', font=font)
    draw.text((1418, 660+80), 'dx', font=font)
    draw.text((1418+120, 660+35), '= -', font=font)
    draw.text((1418+210, 660), 'b', font=font)
    draw.text((1418+210, 660+15), '_', font=font)
    draw.text((1418+210, 660+80), 'a', font=font)
    draw.text((1222,1061),'x',font=font)
    #pos = np.array([1222,1061]) + im_ind/10.0*(np.array([1706,473])-np.array([1222,1061]))
    pos = np.array([1420,490]) + (10.0)/10.0*(np.array([1186,897]) - np.array([1420,490]))
    decr = 2.5*(11.0*1.0)**1.7 + (np.sin(im_ind/3.0 + np.pi/4) - np.sin(np.pi/4)) * 200.0
    draw.text((pos[0] - decr, pos[1]),'y',font=font,fill='red')
    shift = np.array([1000.0, 1048.0])
    p1 = np.array([1250.0, 1048.0])
    p1_shrunk = (p1*1.0 - shift[:2])/scale
    p2 = np.array([p1[0], -b*(1-p1_shrunk[0]/a)*scale+shift[1]])
    p3 = p1 - np.array([decr, 0])
    p3_shrunk = (p3 - shift[:2]) / scale
    p4 = np.array([p3[0], -b*(1-p3_shrunk[0]/a)*scale+shift[1]])
    draw.polygon(((p1[0],p1[1]),(p2[0],p2[1]),(p4[0],p4[1]),(p3[0],p3[1])), (120,180,20,100))
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')


'''
Types text onto an image, filling part by part to give the impression of it being typed.
args:
    txt: The text to be typed onto the image.
    im: The image object.
    im_ind: How far in the animation are we?
    pos: The position in the image at which the text is to be typed.
'''
def writeStaggeredText(txt, draw, im_ind, pos = (250,200)):
    font = ImageFont.truetype("arial.ttf", 78)
    draw.text(pos, txt[:min(im_ind*2, len(txt))], (255,255,255), font=font)


'''
Draws an x-y grid over the x-y plane
'''
def drawXYGrid(draw, r, meshLen = 0.5, extent = 1.0, shift = np.array([1000.0,1000.0,0.0]),scale=200.0):
    upper = 5.5*extent
    #First, draw some lines parallel to the x-axis
    for x in np.arange(-5.0,upper,meshLen):
        pt1 = np.dot(r, np.array([x,-5.0,0]))*scale + shift[:3]
        pt2 = np.dot(r,np.array([x,5.0,0]))*scale + shift[:3]
        draw.line((pt1[0],pt1[1],pt2[0],pt2[1]),(102,255,51, 120),width=2)
    for y in np.arange(-5.0,upper,meshLen):
        pt1 = np.dot(r, np.array([-5.0,y,0]))*scale + shift[:3]
        pt2 = np.dot(r,np.array([5.0,y,0]))*scale + shift[:3]
        draw.line((pt1[0],pt1[1],pt2[0],pt2[1]),(102,255,51, 120),width=2)

'''
@MoneyShot
    A visualization of a plane and its gradient.
'''
def threePointPlane(j = 4 + 46/3.0, im_ind = 0, draw1 = None, im = None):
    global scale
    scale = 60
    global shift
    shift = np.array([1200, 580, 0])
    font = ImageFont.truetype("arial.ttf", 75)
    #dimn = (np.cos(im_ind * np.pi /10.0))
    #dimn = 1 + 10.0 * np.sin(im_ind * np.pi /60.0)
    #if abs(dimn) < 0.1:
    #    dimn = np.sign(dimn)*0.1
    [a,b,c] = np.array([2.5, 2.5, -2.5 * 10.0 / 10.0]) * 410 / 200
    #b = 2.5 + 2 * np.tan(im_ind * (np.pi+1e-3) / 30.0)
    rot = general_rotation(np.array([0,0,1]), np.pi/40.0 * 0)
    r = rotation(3, 2 * np.pi*j/30.0)
    r = np.dot(r, rot)
    r1 = np.eye(4)
    r1[:3,:3] = r
    if draw1 is None:
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
    else:
        draw = draw1
    render_scene_4d_axis(draw, r1, 4, scale = scale, shift = shift)
    pt1 = np.dot(r,np.array([a,0,0])) * scale + shift[:3]
    pt2 = np.dot(r,np.array([0,b,0])) * scale + shift[:3]
    pt3 = np.dot(r,np.array([0,0,c])) * scale + shift[:3]
    pt4 = np.dot(r,np.array([a,b,-c])) * scale + shift[:3]
    d = 1 / (a**-2 + b**-2 + c**-2)
    pt_centroid = np.dot(r, d * np.array([1/(a), 1/(b), 1/(c)])) * scale + shift[:3]
    width = 20 + 10 * np.sin(im_ind)
    #draw.ellipse((pt_centroid[0]-width,pt_centroid[1]-width,pt_centroid[0]+width,pt_centroid[1]+width),fill=(0, 128, 255))
    #draw.line((pt_centroid[0], pt_centroid[1], shift[0], shift[1]), fill=(0, 128, 255), width = 5)
    ## Draw the normal vector from origin onto the plane.
    #arrowV1(draw, r, np.array([0,0,0]), d * np.array([1/(a), 1/(b), 1/(c)]), rgb = (0,128,255), scale = scale, shift = shift)
    tr1 = np.dot(r, np.array([0,0,0])) * scale + shift[:3]
    tr2 = np.dot(r, d * np.array([1/(a), 1/(b), 1/(c)])) * scale + shift[:3]
    tr3 = np.dot(r, d * np.array([1/(a), 1/(b), 0])) * scale + shift[:3]
    p = 10.0 / 10.0
    tr_intr = (p) * tr3 + (1-p) * tr2
    #draw.polygon([(tr1[0], tr1[1]), (tr2[0], tr2[1]), (tr_intr[0], tr_intr[1])], fill = (204, 0, 204, 80))
    ext1 = 3.0 * tr1 + (1 - 3.0) * tr3
    ext2 = -3.0 * tr1 + (1 + 3.0) * tr3
    #draw.line((ext1[0], ext1[1], ext2[0], ext2[1]), fill = (204, 0, 204), width = 3)
    p = im_ind / 15.0
    intermediate = (1-p) * ext1 + p * ext2
    #draw.ellipse((intermediate[0]-width, intermediate[1]-width, intermediate[0]+width, intermediate[1]+width), fill = (204, 0, 204))
    drawRandomVecOnPlane(draw, r, pt_centroid = d * np.array([1/(a), 1/(b), 1/(c)]), im_ind = 29.0/2.0)
    #intermeriateWhiteEffect(draw, r, im_ind, a, b, c)
    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(200,80,100), width = 3)
    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill='orange', width = 3)
    mid_pt = pt2 + (pt1 - pt2) * (im_ind-3) / 15.0
    #draw.ellipse((mid_pt[0]-width,mid_pt[1]-width,mid_pt[0]+width,mid_pt[1]+width),fill='orange')
    draw.polygon([(pt1[0],pt1[1]),(pt3[0],pt3[1]),(pt2[0],pt2[1])], (200,80,100,100))
    draw.polygon([(pt1[0],pt1[1]),(pt4[0],pt4[1]),(pt2[0],pt2[1])], (200,80,100,120))
    #draw.polygon([(pt1[0],pt1[1]),(pt6[0],pt6[1]),(pt5[0],pt5[1]),(pt2[0],pt2[1])], (130,80,30,100))
    draw.line((shift[0],shift[1],pt3[0],pt3[1]), fill = "yellow", width=7)
    draw.line((shift[0],shift[1],pt1[0],pt1[1]), fill = "yellow", width=7)
    draw.line((shift[0],shift[1],pt2[0],pt2[1]), fill = "yellow", width=7)
    drawXYGrid(draw, r, 1.25, scale = scale, shift = shift)
    pt_1 = np.array([a/2.0, b/2.0, 0])
    #projectArrowOnPlane(draw, r)
    ## draw the circles
    arxExt = 180
    draw_circle(draw=draw, r = r, center=pt_1[:2], radius=1, start = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0]), arcExtent = arxExt, scale = scale, shift=shift)
    project_circle_on_plane(draw=draw, r = r, center=pt_1[:2], radius=1, plane = np.array([a,b,c]), 
        start = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0]), arcExtent=arxExt, scale = scale, shift = shift)
    pt = np.dot(r, pt_1)*scale + shift[:3]
    theta = np.arctan(a/b) #+ im_ind * 10 * (np.pi * 2.0 / 180)
    pt_2 = pt_1 + 1.0 * np.array([np.cos(theta), np.sin(theta), 0])
    pt_3 = pt_1 + np.cos(theta + np.pi/4) * np.array([b, -a, 0]) / np.sqrt(a**2 + b**2)
    tail = np.dot(r, pt_1) * scale + shift[:3]
    head = np.dot(r, pt_2) * scale + shift[:3]
    p = -7.0
    tail1 = p * tail + (1-p) * head
    p = 7.0
    head1 = p * tail + (1-p) * head
    #draw.line((tail1[0], tail1[1], head1[0], head1[1]), width = 2, fill = (204, 51, 255))
    arrowV1(draw, r, pt_1, pt_2, scale = scale, shift = shift)
    arrowWithProjection(im, draw, r, pt_1, pt_2, plane = np.array([a,b,c]))
    width = 3 *(0.0 % 3) + 10
    draw.ellipse((pt[0]-width,pt[1]-width,pt[0]+width,pt[1]+width),fill=(102,255,51))
    #arrowV1(draw, r, pt_1, pt_1 - 6*np.array([1/a,1/b,1/c]), rgb = (136, 77, 255))
    #snapGridToPoint(draw, r, im_ind)
    if draw1 is not None:
        im = im.rotate(180)
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        draw = ImageDraw.Draw(im, 'RGBA')
        z_top_pos = np.dot(r, np.array([0, 0, -5])) * np.array([1,-1,0]) * scale + shift[:3]
        draw.text((z_top_pos[0] - 40, z_top_pos[1] + 40), 'z', font=font, fill='yellow')
        x_top_pos = np.dot(r, np.array([5, 0, 0])) * np.array([1,-1,0]) * scale + shift[:3]
        draw.text((x_top_pos[0] - 40, x_top_pos[1] + 40), 'x', font=font, fill='yellow')
        y_top_pos = np.dot(r, np.array([0, 5, 0])) * np.array([1,-1,0]) * scale + shift[:3]
        draw.text((y_top_pos[0] - 40, y_top_pos[1] + 40), 'y', font=font, fill='yellow')
        #writeStaggeredText("In summary, direction perpendicular to orange subspace\n 1) Causes z to change the most.\n 2) Is the gradient", draw, im_ind, pos = (30,1270))
        #draw.text((935,545), '(0,0,c)', font=font)
        #draw.text((1265,805), '(a,0,0)', font=font)
        #draw.text((465,1075), '(0,b,0)', font=font)
        #draw_equation(draw, im_ind)    
        writeLatex(im,'z = c \\left( 1 - \\frac{x}{a} - \\frac{y}{b} \\right)', (40,40), (253,253,253))
        '''
        writeLatex(im, '\\frac{\\partial z}{\\partial x} = - \\frac{c}{a}', (1550, 90), (253,253,253))
        writeLatex(im, '\\frac{\\partial z}{\\partial y} = - \\frac{c}{b}', (1550, 250), (253,253,253))
        writeLatex(im, '\\vec{\\Delta}z = -c[\\frac{1}{a},\\frac{1}{b}]', (1450, 250+170), (253,253,253))
        writeLatex(im, '\\vec{\\Delta}z \propto [\\frac{1}{a},\\frac{1}{b}]', (1450, 250+340), (253,253,253))
        #writeLatex(im, '\\frac{\\partial z}{\\partial y} = - \\frac{c}{b}', (1550, 250), (253,253,253))
        #writeLatex(im, '\\left[\\frac{1}{a}, \\frac{1}{b}\\right]', (1550, 210), (0,255,0))
        #writeLatex(im,'\\frac{x}{a} + \\frac{y}{b} + \\frac{z}{c} = 1', (40, 40), (253,253,253))    
        pp = np.array([810,180]) + (np.array([5,660]) - np.array([810,180])) *10.0/10.0
        writeLatex(im,'[x, y, z]', (pp[0], pp[1]), (253,253,253))
        writeLatex(im,': \\vec{v}', (pp[0]+330, pp[1]), (255,20,147))
        pp_1 = np.array([810,180]) + (np.array([5,860]) - np.array([810,180])) * 10.0/10.0
        writeLatex(im, '\\left[ \\frac{1}{a}, \\frac{1}{b}, \\frac{1}{c}\\right]', (pp_1[0], pp_1[1]), (253,253,253))
        writeLatex(im, ': \\vec{n}', (pp_1[0] + 330, pp_1[1]), (0,128,255))
        writeLatex(im, '\\vec{v} .', (910, 370), (255,20,147))
        writeLatex(im, '\\vec{n}', (910 + 100, 370), (0,128,255))
        writeLatex(im, ' = 1', (910 + 2*100, 370), (253,253,253))
        writeLatex(im, '\\vec{p}.', (940 , 500), (255,0,0))
        writeLatex(im, '\\vec{n}', (940+70 , 500), (0,128,255))
        writeLatex(im, ' = 0', (940+2*70 , 500), (253,253,253))
        #writeLatex(im, '\\vec{p}.', (940 , 500), (255,0,0))
        #writeLatex(im, '\\vec{n} + s \\vec{n}.\\vec{n} ', (940+70 , 500), (0,128,255))
        #writeLatex(im, ' = 1', (940+2*220 , 500), (253,253,253))
        #writeLatex(im, '2\\vec{p}.', (1000 , 630), (255,0,0))
        #writeLatex(im, '\\vec{n} + s \\vec{n}.\\vec{n} ', (1000 + 110 , 630), (0,128,255))
        #writeLatex(im, ' = 1', (1000+2*250 , 630), (253,253,253))
        '''
        im.thumbnail((512, 512), Image.ANTIALIAS)
        #im = im.crop((0,0,2048,1200))
        #im.save('Images\\RotatingCube\\im' + str(20 + 19 - im_ind) + '.png')
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')

'''
    Returns a triangular function oscillating between an upper and lower bound (hard coded for now).
'''
def zigzag(x):
    if x < 1:
        return 1 + x
    elif 1 <= x and x < 10:
        return 3 - x
    elif 10 <= x and x <= 22:
        return -17 + x
    else:
        return zigzag(x%22)


def drawRandomVecOnPlane(draw, r, plane = np.array([2.5 , 2.5, -2.5])*410/200, im_ind = 0, pt_centroid = None):
    s1 = np.sin( (im_ind+3)*np.pi/6 )
    s2 = np.cos( (im_ind+3)*np.pi/6 )
    s3 = 1-s1-s2
    softsum = np.exp(s1) + np.exp(s2) + np.exp(s3)
    [p1, p2, p3] = [np.exp(s1)/softsum, np.exp(s2)/softsum, np.exp(s3)/softsum]
    [a,b,c] = plane
    pt1 = np.array([a,0,0])
    pt2 = np.array([0,b,0])
    pt3 = np.array([0,0,c])
    pt = p1 * pt1 + p2 * pt2 + p3* pt3
    #arrowV1(draw, r, np.array([0,0,0]), pt, rgb = (255,20,147))
    #if pt_centroid is not None:
    #    arrowV1(draw, r, pt_centroid, pt, rgb = (255,0,0))

'''
@OneOff
    Shows off properties of dot products.
'''
def demonstrateDotProduct(im_ind = 0):
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    writeStaggeredText("Vectors and dot products", draw, im_ind, pos = (608,401))
    if im_ind > 1:
        arrowV1(draw, np.eye(3), np.array([0,0,0]), np.array([4,0,0]))
    if im_ind > 2:
        arrowV1(draw, np.eye(3), np.array([0,0,0]), np.array([3,2,0]), rgb = (0,128,255))
    pt1 = np.array([0,0,0]) * scale + shift
    pt2 = np.array([3,0,0]) * scale + shift
    pt3 = np.array([3,2,0]) * scale + shift
    if im_ind > 3:
        draw.polygon([(pt1[0],pt1[1]),(pt2[0],pt2[1]),(pt3[0],pt3[1])], (204, 102, 255, 120))
    if im_ind > 4:
        writeLatex(im, '\\vec{a}', (1820,950), (0,255,0))
    if im_ind > 5:
        writeLatex(im, '\\vec{b}', (pt3[0], pt3[1]), (0,128,255))
    if im_ind > 6:
        writeLatex(im, '\\theta', (1201,1025), (253,253,253))
    if im_ind > 8:
        writeLatex(im, '\\vec{a}.\\vec{b} ', (200,1300), (253,253,253))        
    if im_ind > 9:
        writeLatex(im, '\\vec{a}.\\vec{b} = \\vec{b}.\\vec{a} ', (200,1300), (253,253,253))
    if im_ind > 10:
        writeLatex(im, '\\vec{a}.\\vec{b} = \\vec{b}.\\vec{a} = |\\vec{a}||\\vec{b}|', (200,1300), (253,253,253))
    if im_ind > 11:
        writeLatex(im, 'cos(\\theta)', (918,1300), (253,253,253))
    if im_ind > 12:
        writeLatex(im, ' = (a_x b_x + a_y b_y + a_z b_z)', (200,1400), (253,253,253))
    if im_ind > 13:
        writeLatex(im, 'a_z b_z)', (932,1400), (253,253,253))
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')

def intermeriateWhiteEffect(draw, r, im_ind, a, b, c):
    pt1 = np.dot(r,np.array([a,0,0])) * scale + shift[:3]
    pt2 = np.dot(r,np.array([0,b,0])) * scale + shift[:3]
    pt3 = np.dot(r,np.array([0,0,c])) * scale + shift[:3]
    pt4 = np.dot(r,np.array([a,b,-c])) * scale + shift[:3]
    pt5_1 = pt3 + (pt1 - pt3) * im_ind / 12.0
    pt6_1 = pt3 + (pt2 - pt3) * im_ind / 12.0
    pt5_2 = pt3 + (pt1 - pt3) * im_ind / 10.0
    pt6_2 = pt3 + (pt2 - pt3) * im_ind / 10.0
    draw.polygon([ (pt5_1[0], pt5_1[1]), (pt6_1[0], pt6_1[1]), (pt6_2[0], pt6_2[1]), (pt5_2[0], pt5_2[1])], 'white')
    pt5_1 = pt4 + (pt1 - pt4) * im_ind / 12.0
    pt6_1 = pt4 + (pt2 - pt4) * im_ind / 12.0
    pt5_2 = pt4 + (pt1 - pt4) * im_ind / 10.0
    pt6_2 = pt4 + (pt2 - pt4) * im_ind / 10.0
    draw.polygon([ (pt5_1[0], pt5_1[1]), (pt6_1[0], pt6_1[1]), (pt6_2[0], pt6_2[1]), (pt5_2[0], pt5_2[1])], 'white')

def projectArrowOnPlane(draw, r, a=2.5*410/200, b=2.5*410/200, c=-2.5*410/200, pt = np.array([1.25,1.25,0])*410/200):
    grad = np.array([c/a, c/b, 0])
    grad = grad / np.sqrt(sum(grad**2))
    #arrowV1(draw,r,np.array([1,1,0]), np.array([1,1,0]) - grad, (204,102,255))
    polyg = []
    edge_z = c * (1 - (pt[0]-grad[0])/ a - (pt[1]-grad[1])/b)
    center_z = c * (1 - 1/a - 1/b)
    for i in [[pt[0],pt[1],0], [pt[0]-grad[0],pt[1]-grad[1],0], [pt[0]-grad[0],pt[1]-grad[1],edge_z]]:
        point = np.dot(r,np.array(i)) * scale + shift[:3]
        polyg.append([point[0],point[1]])
    #hull = ConvexHull(polyg).vertices
    hull = range(len(polyg))
    polyg = [(polyg[i][0], polyg[i][1]) for i in hull]
    for i in range(len(polyg)):
        draw.line((polyg[i][0], polyg[i][1], polyg[(i+1)%len(polyg)][0], polyg[(i+1)%len(polyg)][1]), fill = (204, 102, 255, 150), width = 4)
    draw.polygon(polyg, (204, 102, 255, 120))

def arrowWithProjection(im, draw, r, pt_1, pt_2, pt_proj = None, plane = np.array([2.5,2.5,-2.5])*410.0/200.0):
    [a,b,c] = plane    
    z_pt_3 = c * (1 - pt_2[0]/a - pt_2[1]/b)
    pt_3 = np.array([pt_2[0], pt_2[1], z_pt_3])
    pt_3_big = np.dot(r, np.array([pt_2[0], pt_2[1], z_pt_3])) * scale + shift[:3]
    pt_2_big = np.dot(r, pt_2) * scale + shift[:3]
    pt_1_big = np.dot(r, pt_1) * scale + shift[:3]
    draw.polygon(((pt_1_big[0],pt_1_big[1]),(pt_2_big[0],pt_2_big[1]),(pt_3_big[0],pt_3_big[1])), (204,102,255,120))
    #if z_pt_3 > 0:
    #    draw.line((pt_1_big[0], pt_1_big[1], pt_3_big[0], pt_3_big[1]), fill = (130,80,30), width = 5 )
    #else:
    #    draw.line((pt_1_big[0], pt_1_big[1], pt_3_big[0], pt_3_big[1]), fill = (200,80,100), width = 5 )
    pt_2_forward = pt_2 + (pt_2 - pt_1) * 0.15
    pt_3_forward = pt_3 + (pt_2 - pt_1) * 0.15
    #arrowV1(draw, r, pt_2_forward, pt_3_forward,(0,102,255), scale = scale, shift = shift)
    #arrowV1(draw, r, pt_3_forward, pt_2_forward,(0,102,255), scale = scale, shift = shift)
    del_pos = np.dot(r, (pt_2_forward+pt_3_forward)/2 ) * scale + shift[:3]
    coordn = (del_pos[0], del_pos[1])
    im_math = Image.open(".\\Images\\Math\\temp1.png")
    im_math = im_math.rotate(180)
    im_math = im_math.transpose(Image.FLIP_LEFT_RIGHT)
    color = heat_rgb(-1.2,1.2,z_pt_3)
    #pasteImage(im_math,im,coordn,True,color=color)
    if pt_proj is not None:
        pt_proj_big = np.dot(r, pt_proj) * scale + shift[:3]
        draw.line((pt_1_big[0], pt_1_big[1], pt_proj_big[0], pt_proj_big[1]), fill = 'pink', width = 7)
        draw.line((pt_2_big[0], pt_2_big[1], pt_proj_big[0], pt_proj_big[1]), fill = 'pink', width = 7)

'''
@OneOff
    Shows x-y grid drawing into a single point, where we can write its equation.
'''
def snapGridToPoint(draw, r, im_ind, pt = np.array([ 0.65196929, -1.17690135,  2.86178952])):
    grid_edge_1 = np.dot(r, np.array([-5,-5,0])) * scale + shift[:3]
    grid_edge_2 = np.dot(r, np.array([-5,5,0])) * scale + shift[:3]
    grid_edge_3 = np.dot(r, np.array([5,5,0])) * scale + shift[:3]
    grid_edge_4 = np.dot(r, np.array([5,-5,0])) * scale + shift[:3]
    pt_big = np.dot(r, pt) * scale + shift[:3]
    grid_edges = [grid_edge_1, grid_edge_2, grid_edge_3, grid_edge_4]
    if im_ind <= 10:
        for i in grid_edges:
            draw.line((i[0], i[1], pt_big[0], pt_big[1]), fill = 'green', width = 3)
        for i in range(len(grid_edges)):
            p1 = grid_edges[i%len(grid_edges)]
            p2 = grid_edges[(i+1)%len(grid_edges)]
            p1_1 = p1 + (pt_big - p1) * im_ind / 10.0
            p2_1 = p2 + (pt_big - p2) * im_ind / 10.0
            p1_2 = p1 + (pt_big - p1) * im_ind / 12.0
            p2_2 = p2 + (pt_big - p2) * im_ind / 12.0
            draw.polygon([ (p1_1[0], p1_1[1]), (p1_2[0], p1_2[1]), (p2_2[0], p2_2[1]), (p2_1[0], p2_1[1])], (20,255,20,70))
    else:
        font = ImageFont.truetype("arial.ttf", 75)
        draw.text((pt_big[0], pt_big[1]), 'z = 0', font = font, fill = 'green')



