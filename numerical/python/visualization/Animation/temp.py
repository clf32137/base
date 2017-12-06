import numpy as np

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


def createChannelArt(im_ind = 0):
    im = Image.new("RGB", (2560, 1440), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    threePointPlane(draw1 = draw, im = im)
    #General3DCube(numTerms = 10, pos = [2000, 20,0], draw1 = draw, scale1 = 20)
    General3DCube(numTerms=8, im_ind = 3)
    im1 = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\RotatingCube\\im3.png')
    im1.thumbnail((300, 300), Image.ANTIALIAS)
    pasteImage(im1, im, posn = np.array([1350,480,0]))
    im_sam = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\SamuraiBest\SamuraiWalking\Waving\\im0.png')
    im_sam.thumbnail((256, 330), Image.ANTIALIAS)
    pasteImage(im_sam, im, posn = np.array([913,520,0]))
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')



