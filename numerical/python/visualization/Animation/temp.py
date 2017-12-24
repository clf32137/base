
import numpy as np
#from CubeObjects import *

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


'''
@MoneyShot
    Draws a four dimensional teserract with two tetrahedral and one octahedral planes visible.
'''
def teserract_body_diagonal2(im_ind = 70, width = 15, scale1 = 500, shift1 = np.array([1000,1000,0,0,0]), move = 0.0):
    global scale
    scale = scale1
    c1 = Cube(4)
    r = np.eye(4)
    r[:3,:3] = rotation(3, np.pi*2*(27.0-im_ind)/80.0)
    #r[:3,:3] = general_rotation(np.array([1,-1,0]),np.pi/2 + np.arccos(np.sqrt(0.666666)))
    newr = general_rotation(np.array([1,-1,0]), (np.pi/2 + np.arccos(np.sqrt(0.666666)))*4.35/10.0)
    oldr = rotation(3, np.pi*2*(27.0)/80.0)
    #r[:3,:3] = rotation_transition(im_ind/10.0, newr, oldr)
    
    r1 = rotation(4, np.pi*2*(im_ind)/80.0)
    r[:3,:3] = oldr
    #r = np.dot(r, r1)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    #render_scene_4d_axis(draw, r, 4)
    rotated_vertices = np.transpose(np.dot(r,np.transpose(c1.vertice_matrix)))*scale1 + shift1[:4]
    #tetrahedron(draw, rotation(3, np.pi*2*(27.0)/80.0), offset = [500,1500,0], dist = 300, w = int(im_ind/3.0), rgb=(0,0,255))
    #tetrahedron(draw, rotation(3, np.pi*2*(27.0)/80.0), dist = 300, w = int(im_ind/3.0), offset = [500,500,0])
    #octahedron(draw, rotation(3, np.pi*2*(27)/80.0), w = 5, alp=0, offset = [500,1000,0])
    body_diag = (c1.vertices[0].to_binary() - c1.vertices[15].to_binary())
    c1.plot_edges2(draw, r, offset = body_diag * move, fill = (255,165,100, 150),scale=scale1,shift=shift1)
    
    #frst = [1,2,4,8]
    #scnd = [3,5,6,9,10,12]
    #thrd = [7,11,13,14]
    frst = [1,2,4]
    scnd = [3,5,6]
    
    for e in c1.edges:
        if e.vertice1.index ==0 and e.vertice2.index in frst:
            pt1 = rotated_vertices[e.vertice1.index]
            pt2 = rotated_vertices[e.vertice2.index]
            center = (pt1 + pt2)/2.0
            p = im_ind/10.0
            pp1 = (1-p)*pt1 + p*pt2
            p = p + 0.08
            pp2 = (1-p)*pt1 + p*pt2
            draw.line((pp1[0], pp1[1], pp2[0], pp2[1]), fill=(200,220,5), width = int(10))
            #draw.line((pp1[0], pp1[1], pp2[0], pp2[1]), fill=(200,220,5), width= int(10))
    
    tri = []
    for j in frst:
        tri.append((rotated_vertices[j][0], rotated_vertices[j][1]))

    im = im.crop((852, 565, 1915, 1446))
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')


    '''
    draw.polygon(tri, (200-10*20,220-10*20,5+10*20, 30+10*4))
    
    tri = []
    for j in scnd:
        tri.append((rotated_vertices[j][0], rotated_vertices[j][1]))

    draw.polygon(tri, (200,220-im_ind*20,5, 30+10*4))
    '''
    
    sqr1 = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 3]]] + (rotated_vertices[0] - rotated_vertices[15]) * -move
    sqr1_orig = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 3]]]
    
    try:
        draw.polygon(jarvis_convex_hull(sqr1), (255,0,0,int(65)))
    except:
        print "err"

    i = 0
    a = range(4)
    a.pop(i)
    tri = []
    tri_orig = []
    for j in a:
        tri.append((sqr1[j][0], sqr1[j][1]))
        tri_orig.append((sqr1_orig[j][0], sqr1_orig[j][1]))
    #draw.polygon(tri, (255,150,0,60))
    #draw.polygon(tri_orig, (255,150,0,70))

    for ver in c1.vertices[c1.vertice_coordinate_sums == 3]:
        ver.plot(r, draw, (255,0,0), 10, offset = -body_diag * move, scale=scale1, shift=shift1)
        for ver1 in c1.vertices[c1.vertice_coordinate_sums == 3]:
            e = Edge(ver,ver1)
            e.plot(r,draw,(255,0,0), width=2, offset = -body_diag * move, scale=scale1, shift=shift1)
            #e.plot(r,draw,(255,165-im_ind*12,0), width=2, offset = -body_diag * move,scale=scale1, shift=shift1)

    hexag = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 2]]]
    for ed in [(5,3),(5,6),(5,9),(5,12),(10,3),(10,6),(10,9),(10,12),(3,6),(3,9),(12,6),(12,9)]:
        v1 = rotated_vertices[ed[0]]
        v2 = rotated_vertices[ed[1]]
        draw.line((v1[0], v1[1], v2[0], v2[1]), fill = (0,255,0), width=4)
        #draw.line((v1[0], v1[1], v2[0], v2[1]), fill = (255-im_ind*10,165+im_ind,0), width=4)
    for ver in c1.vertices[c1.vertice_coordinate_sums==2]:
        ver.plot(r, draw, (0,255,0), 10,scale=scale1,shift=shift1)
        #ver.plot(r, draw, (255-im_ind*25,im_ind*25,0), 10, scale=scale1, shift=shift1)

    try:
        draw.polygon(jarvis_convex_hull(hexag), (0,255,0,int(65)))
    except:
        print "err"

    for ver in c1.vertices[c1.vertice_coordinate_sums == 1]:
        #ver.plot(r, draw, (0,0,255), 10, offset = body_diag * move)
        ver.plot(r, draw, (255,0,0), 10, offset = body_diag * move,scale=scale1, shift=shift1)
        #ver.plot(r, draw, (0,0,255), 10)
        for ver1 in c1.vertices[c1.vertice_coordinate_sums == 1]:
            e = Edge(ver,ver1)
            e.plot(r,draw,(0,0,255), offset = body_diag * move,scale=scale1, shift=shift1)
            #e.plot(r,draw,(255-im_ind*16,165-im_ind*13,im_ind*25), offset = body_diag * move,scale=scale1, shift=shift1)

    sqr2 = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 1]]] + (rotated_vertices[0] - rotated_vertices[15]) * move
    sqr2_orig = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 1]]]
    try:
        draw.polygon(jarvis_convex_hull(sqr2), (0,0,255,int(65)))
    except:
        print "err"
    
    i = 3
    a = range(4)
    a.pop(i)
    tri = []
    tri_orig = []
    for j in a:
        tri.append((sqr2[j][0], sqr2[j][1]))
        tri_orig.append((sqr2_orig[j][0], sqr2_orig[j][1]))
    #draw.polygon(tri, (150,0,255,60))
    #draw.polygon(tri_orig, (150,0,255,70))

    v1 = rotated_vertices[0]
    v2 = rotated_vertices[15]
    #draw.line((v1[0], v1[1], v2[0], v2[1]), fill = (255,255,255), width=2)
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')


#teserract_body_diagonal2(im_ind=i,scale1=500+i*20,shift1=np.array([1000-50*i, 1000+50*i,0,0]))
#i = 10
