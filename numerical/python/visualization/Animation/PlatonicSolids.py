import numpy as np
from scipy.spatial import ConvexHull

def tetrahedron(draw, r, offset = [500,1000,0], rgb = (216,52,52), dist = 300, w=2, tet_orig = None):
    if tet_orig is None:
        tet_orig = np.array([
                [0,0,0],
                [1,0,0],
                [0.5,0.866025,0],
                [0.5,0.288675,0.8164925]
            ])
    rgba = rgb + (100,)
    for j in range(0,1):
        #r = general_rotation(np.array([1,1,0]), np.pi*2*j/80.0)
        #im = Image.new("RGB", (2048, 2048), "black")
        #draw = ImageDraw.Draw(im,'RGBA')
        tet = np.dot(tet_orig,r)
        k = 0
        for i in tet:
            if k == 3:
                ver = i * dist + offset
            else:
                ver = i * 300 + offset
            #draw.ellipse((ver[0]-150,ver[1]-150,ver[0]+150,ver[1]+150), fill = rgba)
            draw.ellipse((ver[0]-5,ver[1]-5,ver[0]+5,ver[1]+5), fill = rgb)
            k += 1
        for i in range(len(tet)):
            for k in range(i,len(tet)):
                ver1 = tet[i] * 300 + offset
                ver2 = tet[k] * 300 + offset
                draw.line((ver1[0],ver1[1],ver2[0],ver2[1]), fill = rgb, width = 5)
        
        #tri = [(tet[w%4][0]*300+offset[0], tet[w%4][1]*300+offset[0]), (tet[(w+1)%4][0]*300+offset[0], tet[(w+1)%4][1]*300+offset[0]), (tet[(w+2)%4][0]*300+offset[0], tet[(w+2)%4][1]*300+offset[0])]
        #draw.polygon(tri, (216,52,52,100))
        #im.save('Images\\RotatingCube\\im' + str(j) + '.png')

'''
Creates a tetrahedron with centroid at the origin. Also draws a cutting plane
'''
def tetrahedron2(draw, r, shift = [1000,1000,0], scale = 300, plane_normal = np.array([.5,.5,.5]), rgb = (216,52,52), offset = 150):
    tet_orig = np.array([
            [1,1,1],
            [-1,-1,1],
            [1,-1,-1],
            [-1,1,-1]
        ])
    tet_rot = np.dot(tet_orig, r)
    tet = tet_rot * scale + shift[:3]
    [a,b,c] = plane_normal
    poly = []
    poly1 = []
    poly2 = []
    ipos = 0
    jpos = 0
    for i in range(4):
        ver1 = tet[i]
        if np.dot(tet_rot[i], plane_normal) > 0:
            ipos = 1
        else:
            ipos = -1
        ver1 = ver1 + ipos * plane_normal * offset
        draw.ellipse((ver1[0]-7,ver1[1]-7,ver1[0]+7,ver1[1]+7), fill = (255,0,0))
        for j in range(i,4):
            ver2 = tet[j]
            if np.dot(tet_rot[j], plane_normal) > 0:
                jpos = 1
            else:
                jpos = -1
            ver2 = ver2 + jpos * plane_normal * offset
            [x1, y1, z1] = tet_rot[i]
            [x2, y2, z2] = tet_rot[j]
            p = -(a*x2+b*y2+c*z2)/(a*(x1-x2)+b*(y1-y2)+c*(z1-z2))
            if 0 < p and p < 1:
                pt = p * (ver1 - ipos * plane_normal * offset) + (1-p) * (ver2 - jpos * plane_normal * offset)
                draw.ellipse((pt[0]-7,pt[1]-7,pt[0]+7,pt[1]+7), fill = (255,152,0))
                pt1 = pt + ipos * plane_normal * offset
                pt2 = pt + jpos * plane_normal * offset
                draw.line((ver1[0],ver1[1],pt1[0],pt1[1]), fill = rgb, width = 5)
                draw.line((ver2[0],ver2[1],pt2[0],pt2[1]), fill = rgb, width = 5)
                poly.append((pt[0], pt[1]))
                poly1.append((pt[0] + plane_normal[0] * offset, pt[1] + plane_normal[1] * offset))
                poly2.append((pt[0] - plane_normal[0] * offset, pt[1] - plane_normal[1] * offset))
            else:
                draw.line((ver1[0],ver1[1],ver2[0],ver2[1]), fill = rgb, width = 5)
    hull = ConvexHull([[i[0], i[1]] for i in poly]).vertices
    poly = [(poly[i][0], poly[i][1]) for i in hull]
    hull = ConvexHull([[i[0], i[1]] for i in poly1]).vertices
    poly1 = [(poly1[i][0], poly1[i][1]) for i in hull]
    hull = ConvexHull([[i[0], i[1]] for i in poly2]).vertices
    poly2 = [(poly2[i][0], poly2[i][1]) for i in hull]
    draw.polygon(poly, (152, 204, 0, 90))
    draw.polygon(poly1, (152, 204, 0, 45))
    draw.polygon(poly2, (152, 204, 0, 45))
    plane = np.array([
            [2,2,0],
            [-2,2,0],
            [-2,-2,0],
            [2,-2,0]
        ])
    r2 = rotate_vec2vec(np.array([0,0,1]), plane_normal)
    plane2 = np.dot(plane, r2) * scale + shift[:3]
    poly = [(i[0],i[1]) for i in plane2]
    draw.polygon(poly, (152, 204, 52, 60))


def tetrahedron3(draw, r, theta = np.pi/12, offset = np.array([1000,1000,0]), scale = 150, rgb = (216,52,52)):
    tet_orig = np.array([
            [1,1,1],
            [-1,-1,1],
            [1,-1,-1],
            [-1,1,-1]
        ])
    rgba = rgb + (100,)
    tet = np.dot(tet_orig,r)
    for i in tet:
        ver = i * scale + offset
        draw.ellipse((ver[0]-5,ver[1]-5,ver[0]+5,ver[1]+5), fill = rgb)
    bulb = np.array([-2.5,0,0,]) * scale + shift[:3]
    draw.ellipse((bulb[0]-5,bulb[1]-5,bulb[0]+5,bulb[1]+5), fill = rgb)
    for i in range(len(tet)):
        for k in range(i,len(tet)):
            ver1 = tet[i] * scale + offset
            ver2 = tet[k] * scale + offset
            draw.line((ver1[0],ver1[1],ver2[0],ver2[1]), fill = rgb, width = 5)
            ver1prime = project_on_plane(bulb, ver1)
            ver2prime = project_on_plane(bulb, ver2)
            draw.line((ver1prime[0],ver1prime[1],ver2prime[0],ver2prime[1]), fill = rgb, width = 2)
    draw_plane(draw, scale)

'''
'''
def tetrahedron4(draw, r, scale = 235.5, shift = np.array([1009, 998, 0])):
    tri = (np.arange(3)+1)*2*np.pi/3
    scatter1 = assign(3,3)
    thetas = np.array([tri[int(i)] for i in scatter1])
    ht = np.sqrt(2)
    pt1 = np.array([np.cos(thetas[0]), np.sin(thetas[0]), 0])
    pt2 = np.array([np.cos(thetas[1]), np.sin(thetas[1]), 0])
    pt3 = np.array([np.cos(thetas[2]), np.sin(thetas[2]), 0])
    pt4 = (pt1 + pt2 + pt3) / 3
    pt4[2] = ht
    tet_orig = np.array([pt1, pt2, pt3, pt4])
    tet = np.dot(tet_orig, np.transpose(r)) * scale + shift
    centroid = sum(tet) / 4
    tet1 = tet - centroid
    for i in range(4):
        indxs = [j for j in range(4) if j != i]
        poly = [(tet[j][0], tet[j][1]) for j in indxs]
        outwardPlaneVec = sum(tet1[indxs])
        if outwardPlaneVec[2] > 0:
            draw.polygon(poly, (0 + int(outwardPlaneVec[2]/50.0),162+ int(outwardPlaneVec[2]/50.0),232+ int(outwardPlaneVec[2]/50.0),180))
            for ii in range(3):
                for jj in range(ii+1,3):
                    draw.line((tet[indxs[ii]][0], tet[indxs[ii]][1], tet[indxs[jj]][0], tet[indxs[jj]][1]), fill = (255,255,0), width = 5)
        else:
            for ii in range(3):
                for jj in range(ii+1,3):
                    draw.line((tet[indxs[ii]][0], tet[indxs[ii]][1], tet[indxs[jj]][0], tet[indxs[jj]][1]), fill = (255,255,0,120), width = 3)

def tetrCircumSphrRad(z):
    return np.sqrt(1+1/8.0-(1/np.sqrt(8)-z)**2)

'''
'''
def draw_plane(draw, theta = np.pi/12, scale = 150):
    plane = np.array([
            [4.0*(1+np.cos(theta)),4 + 2,-2],
            [3.0*(1-np.cos(theta)),4,2],
            [3.0*(1-np.cos(theta)),-4,-2],
            [4.0*(1+np.cos(theta)),-4 - 2,2]
        ])
    #plane_normal = np.array([np.sin(theta), 0, np.cos(theta)])
    #r2 = rotate_vec2vec(np.array([1,0,0]), plane_normal)
    #plane2 = np.dot(plane, r2) * scale + shift[:3]
    plane = plane * scale + shift[:3]
    poly = [(i[0],i[1]) for i in plane]
    draw.polygon(poly, (152, 204, 52, 100))

'''
'''
def project_on_plane(x1, x2, theta = np.pi/12, scale = 150, shift=np.array([1000,1000,0])):
    n = np.array([np.cos(theta), 0, np.sin(theta)])
    c = 2.5*np.cos(theta) * scale + shift[0]
    p = (c - np.dot(x1,n))/(np.dot(x2-x1, n))
    return (1-p) * x1 + p * x2


def octahedron(draw, r, alp = 100, w = 2, ind = 0, offset = [1000,1000,0]):
    tet_orig = np.array([
            [0,0,0],
            [1,0,0],
            [0,1,0],
            [1,1,0],
            [0.5,0.5,0.7071],
            [0.5,0.5,-0.7071]
        ])
    for j in range(0,1):
        #r = general_rotation(np.array([1,2,0.4]), np.pi*2*j/80.0)
        #im = Image.new("RGB", (2048, 2048), "black")
        #draw = ImageDraw.Draw(im,'RGBA')
        tet = np.dot(tet_orig, r)
        for i in tet:
            ver = i * 300 + offset
            draw.ellipse((ver[0]-150,ver[1]-150,ver[0]+150,ver[1]+150), fill = (43,183,31,alp))
            draw.ellipse((ver[0]-5,ver[1]-5,ver[0]+5,ver[1]+5), fill = (43,183,31))
        indxs = [0,1,3,2]
        for i in range(4):
            k = indxs[(i) % 4]
            l = indxs[(i+1) % 4]
            ver1 = tet[k] * 300 + offset
            ver2 = tet[l] * 300 + offset
            draw.line((ver1[0],ver1[1],ver2[0],ver2[1]), fill = (0,255,0,255), width = w)
            ver_top = tet[4] * 300 + offset
            draw.line((ver1[0],ver1[1],ver_top[0],ver_top[1]), fill = (0,255,0,255), width = w)
            ver_top = tet[5] * 300 + offset
            draw.line((ver1[0],ver1[1],ver_top[0],ver_top[1]), fill = (0,255,0,255), width = w)
        #im.save('Images\\RotatingCube\\im' + str(j) + '.png')


def dodecahedron(draw, r, tet_orig, offset = [1000,1000,0]):
    phi = (1+np.sqrt(5)) / 2
    tet_orig = []
    for i in [-1,1]:
        for j in [-1,1]:
            for k in [-1,1]:
                tet_orig.append(np.array([i,j,k]))
    phi = (1+np.sqrt(5))/2
    for i in [-1,1]:
        for j in [-1,1]:
            tet_orig.append(np.array([0,i*phi,j/phi]))
            tet_orig.append(np.array([i/phi,0,j*phi]))
            tet_orig.append(np.array([i*phi,j/phi,0]))
    tet_orig = np.array(tet_orig)
    plot_polyhedron(draw, tet_orig, r, offset)
    dodecahedron_planes(draw, r, tet_orig)


def icosahedron(draw, r, offset = [1000,1000,0]):
    phi = (1+np.sqrt(5))/2
    tet_orig = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            tet_orig.append(np.array([0,i,j*phi]))
            tet_orig.append(np.array([j*phi,0,i]))
            tet_orig.append(np.array([i,j*phi,0]))
    plot_polyhedron(draw, tet_orig, r, offset, thresh = 2.01)
    icosahedron_planes(draw, r)


def plot_polyhedron(draw, tet_orig, r, offset, thresh = 1.24):
    font = ImageFont.truetype("arial.ttf", 25)
    tet = np.dot(tet_orig, r)
    j = 0
    for i in tet:
        ver = i * 300 + offset
        #draw.ellipse((ver[0]-150,ver[1]-150,ver[0]+150,ver[1]+150), fill = (43,183,31,150))
        draw.ellipse((ver[0]-9,ver[1]-9,ver[0]+9,ver[1]+9), fill = (255,183,31))
        draw.text((ver[0],ver[1]), str(round(tet_orig[j][0],2) ) + "," + str(round(tet_orig[j][1],2 )) + "," + str(round(tet_orig[j][2],2)), font=font, fill = (255,255,255))
        j = j + 1    

def dodecahedron_planes(draw, r, tet_orig, scale = 300, shift = np.array([1000,1000,0])):
    colors = [(120,80,200),(200,80,100),(0,255,128),(0,0,255),(255,153,31),(51,153,255),(0,255,0),(255,255,255),(255,255,0),(255,153,153),(174,87,209),(100,149,237),(210,105,30),(176,196,202)]
    cind = -1
    for pm1 in [-1,1]:
        coeff1 = np.array([1, pm1 * phi, 0])
        for i1 in range(3):
            for pm2 in [-1,1]:
                cind += 1
                coeff = np.array([coeff1[ (i1+jj)%3] for jj in range(3)])
                penta = np.array([i for i in tet_orig if (np.dot(i, coeff ) + pm2*phi*phi == 0)])
                penta = np.dot(penta, r)
                try:
                    hull = ConvexHull([i[:2] for i in penta]).vertices
                    sqr1 = penta * scale + shift[:3]
                    poly = [(sqr1[i][0],sqr1[i][1]) for i in hull]
                    rgba = colors[cind % 14] + (100,)
                    forward_face = np.dot(sum(penta), np.array([0,0,1])) > -1e-3
                    if forward_face: #Meaning the plane is facing forward.
                        draw.polygon(poly, rgba)
                    for i in range(len(poly)):
                        vv1 = poly[i]
                        vv2 = poly[(i+1)%5]
                        if forward_face:
                            draw.line((vv1[0],vv1[1],vv2[0],vv2[1]), fill = (0,255,0,255), width = 3)
                        else:
                            draw.line((vv1[0],vv1[1],vv2[0],vv2[1]), fill = (0,255,0,255), width = 3)
                except:
                    continue

def icosahedron_planes(draw, r, scale = 300, shift = np.array([1000,1000,0])):
    colors = [(120,80,200),(200,80,100),(0,255,128),(0,0,255),(255,153,31),(51,153,255),(0,255,0),(255,255,255),(255,255,0),(255,153,153),(174,87,209),(100,149,237),(210,105,30),(176,196,202)]
    cind = -1
    phi = (1 + np.sqrt(5)) / 2.0
    mat_orig = np.array([
            [1, phi, 0],
            [0, 1, phi],
            [phi, 0, 1]
        ])
    for ii in [1, -1]:
        for jj in [1, -1]:
            for kk in [1, -1]:
                cind += 1
                mat = np.copy(mat_orig)
                mat[0,0] = mat[0,0] * ii
                mat[1,0] = mat[1,0] * ii
                mat[2,0] = mat[2,0] * ii
                mat[0,1] = mat[0,1] * jj
                mat[1,1] = mat[1,1] * jj
                mat[2,1] = mat[2,1] * jj
                mat[0,2] = mat[0,2] * kk
                mat[1,2] = mat[1,2] * kk
                mat[2,2] = mat[2,2] * kk
                mat1 = np.dot(mat, r) * scale + shift[:3]
                forward_face = np.dot(sum(mat1), np.array([0,0,1])) > -1e-3
                if forward_face:
                    poly = [(mat1[i][0],mat1[i][1]) for i in range(len(mat1))]
                    rgba = colors[cind % 14] + (100,)
                    draw.polygon(poly, rgba)
                    for line in range(len(mat1)):
                        draw.line((mat1[line][0],mat1[line][1],mat1[(line+1)%3][0],mat1[(line+1)%3][1]), fill = (0,255,0,255), width = 5)
                else:
                    for line in range(len(mat1)):
                        draw.line((mat1[line][0],mat1[line][1],mat1[(line+1)%3][0],mat1[(line+1)%3][1]), fill = (0,255,0,255), width = 3)
    for ii in range(3):
        for kk in [1, -1]:
            for ll in [1, -1]:
                cind += 1
                mat = np.copy(mat_orig)
                mat[0, ii] = kk * mat[0, ii]
                mat[1, ii] = kk * mat[1, ii]
                mat[2, ii] = kk * mat[2, ii]
                mat[0, (ii+2)%3] = ll * mat[0, (ii+2)%3]
                mat[1, (ii+2)%3] = ll * mat[1, (ii+2)%3]
                mat[2, (ii+2)%3] = ll * mat[2, (ii+2)%3]
                for jj in range(3):
                    mat[ii,jj] = mat[(ii+1)%3,jj]
                mat[ii, (ii+1)%3] = -1 * mat[ii, (ii+1)%3]
                mat1 = np.dot(mat, r) * scale + shift[:3]
                forward_face = np.dot(sum(mat1), np.array([0,0,1])) > -1e-3
                if forward_face:
                    poly = [(mat1[i][0],mat1[i][1]) for i in range(len(mat1))]
                    rgba = colors[cind % 14] + (100,)
                    draw.polygon(poly, rgba)
                    for line in range(len(mat1)):
                        draw.line((mat1[line][0],mat1[line][1],mat1[(line+1)%3][0],mat1[(line+1)%3][1]), fill = (0,255,0,255), width = 5)
                else:
                    for line in range(len(mat1)):
                        draw.line((mat1[line][0],mat1[line][1],mat1[(line+1)%3][0],mat1[(line+1)%3][1]), fill = (0,255,0,255), width = 3)

#[0, np.pi/6, np.pi/4, np.pi/3, np.pi/2, 2*np.pi/3, np.pi, np.pi*1.1, np.pi*1.6, 0]
def circle(draw, r, extent, ind = 0):
    center = np.array([1009,998])
    draw.ellipse((center[0] - 241, center[1]-241, center[0] + 241, center[1] + 241), fill = (255,0,0,255-180))
    draw.ellipse((center[0] - 230, center[1]-230, center[0] + 230, center[1] + 230), fill = (0,162,232,255-180))
    #tri1 = np.array([0, np.pi/2, np.pi, 3*np.pi/2]) - np.pi/4
    #tri1 = np.array([np.pi/2, 7*np.pi/6,11*np.pi/6])
    tri1 = (np.arange(4)+1)*2*np.pi/4
    tri2 = (np.arange(3)+1)*2*np.pi/3
    scatter1 = assign(10,4)
    scatter2 = assign(10,3)
    thetas = np.array([tri1[int(i)] for i in scatter1])
    nxttheta = np.array([tri2[int(i)] for i in scatter2])
    #theta = move_to_closest(thetas[0], tri, ind/10.0)
    theta = move_angle_to_angle(thetas[0], nxttheta[0], ind/10.0)
    pt1 = center + 235.5*np.array([np.cos(theta), np.sin(theta)])
    draw.ellipse((pt1[0]-7,pt1[1]-7,pt1[0]+7,pt1[1]+7),(255,255,0))
    poly = [(pt1[0], pt1[1])]
    for i in range(1,extent):
        #theta = move_to_closest(thetas[i], tri, ind/10.0)
        theta = move_angle_to_angle(thetas[i], nxttheta[i], ind/10.0)
        #ptheta = move_to_closest(thetas[i-1], tri, ind/10.0)
        ptheta = move_angle_to_angle(thetas[i-1], nxttheta[i-1], ind/10.0)
        pt = center + 235.5*np.array([np.cos(theta), np.sin(theta)])
        pt0 = center + 235.5*np.array([np.cos(ptheta), np.sin(ptheta)])
        draw.ellipse((pt[0]-7,pt[1]-7,pt[0]+7,pt[1]+7),(255,255,0))
        draw.line((pt[0],pt[1],pt0[0],pt0[1]), fill = (255,255,0), width = 7)
        poly.append((pt[0],pt[1]))
    draw.line((pt[0], pt[1], pt1[0], pt1[1]), fill = (255,255,0), width = 5)
    draw.polygon(poly, (0,162,232,250))

def triangle(draw,r,ind=0):
    center = np.array([1009, 998, 0])
    tri = (np.arange(3)+1)*2*np.pi/3
    scatter1 = assign(3,3)
    thetas = np.array([tri[int(i)] for i in scatter1])
    poly = []
    for i in range(3):
        pt1 = center + 235.5 * np.dot(r, np.array([np.cos(thetas[i]), np.sin(thetas[i]),0]))
        pt1_orig = np.array([np.cos(thetas[i]), np.sin(thetas[i]),0])
        poly.append((pt1[0],pt1[1]))
        draw.ellipse((pt1[0]-7,pt1[1]-7,pt1[0]+7,pt1[1]+7),(255,255,0))
        for j in range(i+1,3):
            pt2 = center + 235.5 * np.dot(r, np.array([np.cos(thetas[j]), np.sin(thetas[j]),0]))
            pt2_orig = np.array([np.cos(thetas[j]), np.sin(thetas[j]),0])
            draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill = (255,255,0), width = 7)
            k = 3 - i - j # The index of the third point. Sum of all three indices minus the two that are considered here.
            pt3 = center + 235.5 * np.dot(r, np.array([np.cos(thetas[k]), np.sin(thetas[k]),0]))
            pt3_orig = np.array([np.cos(thetas[k]), np.sin(thetas[k]),0])
            mid_pt = (pt1 + pt2) / 2
            mid_pt_orig = (pt1_orig + pt2_orig) / 2
            p = 2 # 2 will help us get to the other side.
            extendedpt = ((1-p) * pt3 + p * mid_pt)
            extendedpt_orig = ((1-p) * pt3_orig + p * mid_pt_orig)
            extendedpt_orig = extendedpt_orig * np.cos(np.pi * ind / 30.0)
            extendedpt_orig[2] = 1.5 * np.sin(np.pi * ind / 30.0)
            extendedpt = center + 235.5 * np.dot(r, extendedpt_orig)
            vec = 2.5 * (mid_pt - pt3) * 0
            draw.polygon([(pt1[0]+vec[0], pt1[1]+vec[1]), (pt2[0]+vec[0], pt2[1]+vec[1]), (extendedpt[0]+vec[0], extendedpt[1]+vec[1])], (0,162,232,180))
            draw.line((extendedpt[0] + vec[0], extendedpt[1]+vec[1], pt1[0]+vec[0], pt1[1]+vec[1]), fill = (255,255,0), width = 5)
            draw.line((extendedpt[0] + vec[0], extendedpt[1]+vec[1], pt2[0]+vec[0], pt2[1]+vec[1]), fill = (255,255,0), width = 5)
            draw.line((pt1[0] + vec[0], pt1[1]+vec[1], pt2[0]+vec[0], pt2[1]+vec[1]), fill = (255,255,0), width = 5)
    draw.polygon(poly, (0,162,232,180))


def move_to_closest(theta, tri, p):
    final = tri[np.argmin((tri-theta)**2)]
    return theta + (final - theta) * p

def move_angle_to_angle(theta1, theta2, p):
    return theta1 + (theta2-theta1) * p

def scatter(n = 8, l = 5):
    res = np.ones(l) * int(n/l)
    excess = n - sum(res)
    i = 0
    while excess > 0:
        res[i] += 1
        excess -= 1
        if excess > 0:
            res[len(res)-1-i] += 1
            excess -= 1
        i = i + 1
    return res

def assign(n = 10, level = 3):
    res = np.zeros(n)
    res[n-1] = level-1
    sct = scatter(n-2, level-2)
    k = 1
    l = 0
    for i in sct:
        l = l + 1
        for j in range(int(i)):
            res[k] = l
            k = k + 1
    return res


def main_plot():
    for i in range(11):
        im = Image.new("RGB", (2048, 2048), (1,1,1))
        draw = ImageDraw.Draw(im,'RGBA')
        r = np.transpose(rotation(3,np.pi*i/60)) #i=9
        #drawXYGrid(draw, r, 1.25, scale = scale, shift = shift)
        r1 = np.eye(4)
        r1[:3,:3] = r
        render_scene_4d_axis(draw, r1, 4, scale = scale, shift = shift[:3])
        #icosahedron(draw, r)
        #tetrahedron3(draw, r, offset = [1000,1000,0])
        #circle(draw, r, 10, ind = i)
        #triangle(draw, r, i)
        rr = general_rotation(np.dot(r, np.array([0,0,1])), np.pi*i/20)
        r2 = np.dot(rr, r)
        tetrahedron4(draw, r2)
        generalized_circle(draw, np.array([0,0,0]), np.array([0,0,1]),1,r,235.5,np.array([1009, 998, 0]), (255,0,0), 7)
        #for z in [0.1, 0.5, 0.9, 1.3, 1.4, 1.4142135]:
        for z in [1.4]:
            generalized_circle2(draw, np.array([0,0,z]), np.array([0,0,1]), tetrCircumSphrRad(z), r, 235.5, np.array([1009, 998, 0]), (255,0,0,150), 5)
        #triangle(draw, r, i)
        im.save('Images\\RotatingCube\\im' + str(i) + '.png')


