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



