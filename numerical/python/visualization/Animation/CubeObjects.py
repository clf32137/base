import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
import sys
from HyperCube import *
from scipy.spatial import ConvexHull
from Sphere import *
from RotateCube import *

#shift = np.array([170,400, 380]) # (for 1024, 1024)
#scale = 300
dim = 4
shift = np.array([1000,1000, 0, 0, 0])
scale = 500

class Vertice():
    def __init__(self, i = 0, n = 4):
        self.dim = n
        self.index = i
        self.binary = self.to_binary()
        global scale

    def plot(self,r,draw,rgba,width=3):
        vv = np.dot(r,self.binary)
        [vx,vy] = (shift[:self.dim] + scale * vv)[0:2] # Projection on x-y plane
        draw.ellipse( (vx-width,vy-width,vx+width,vy+width), fill = rgba, outline = rgba)

    def plot_vid_ready(self,r,draw,rgba,width=9):
        dim = r.shape[0]
        reflection = np.ones(dim)
        reflection[1] = -1
        l = new_vector(r, (self.binary*reflection) * scale + shift[:dim] )
        draw.ellipse((l[0]-width,l[1]-width,l[0]+width,l[1]+width), fill = rgba, outline = rgba)

    def to_binary(self):
        raw=np.zeros(self.dim)
        temp = self.index
        indx = 0
        while temp > 0:
            raw[indx] = temp%2
            temp = temp/2
            indx = indx + 1
        return raw

    def rotated(r):
        return np.dot(r,self.binary)

class Edge():
    def __init__(self, v1, v2, is_inter_dim_connector = False):
        self.vertice1 = v1
        self.vertice2 = v2
        self.is_inter_dim_connector = is_inter_dim_connector
        self.dim = v1.dim
        global scale

    def plot(self, r, draw, rgba, width = 3):
        [v1, v2] = [np.dot(r, self.vertice1.binary), np.dot(r, self.vertice2.binary)]
        [v1x,v1y] = (shift[:self.dim] + scale * v1)[0:2]
        [v2x,v2y] = (shift[:self.dim] + scale * v2)[0:2]
        draw.line((v1x, v1y, v2x, v2y), fill=rgba, width=width)

    def plot_vid_ready(self,r,draw,rgba,width=2):
        reflection = np.ones(dim)
        reflection[1] = -1
        v1 = new_vector(r,self.vertice1.binary*reflection * scale + shift[:dim])
        v2 = new_vector(r,self.vertice2.binary*reflection * scale + shift[:dim])
        draw.line((v1[0],v1[1],v2[0],v2[1]), fill=rgba, width=width)

class Face():
    def __init__(self, vertices, is_inter_dim_connector = False):
        [v1,v2,v3,v4] = vertices
        self.vertice1 = v1
        self.vertice2 = v2
        self.vertice3 = v3
        self.vertice4 = v4
        self.is_inter_dim_connector = is_inter_dim_connector
        self.face_matrix = np.array([v1.binary, v2.binary, v3.binary, v4.binary]) # We can rotate the whole face in one shot.
        self.vertice_indices = np.array([v1.index,v2.index,v3.index,v4.index])
        global scale

    def add(self, a, dim):
        newv1 = Vertice(self.vertice1.index + a, dim)
        newv2 = Vertice(self.vertice2.index + a, dim)
        newv3 = Vertice(self.vertice3.index + a, dim)
        newv4 = Vertice(self.vertice4.index + a, dim)
        return Face([newv1, newv2, newv3, newv4])

    def expand_dim(self, dim2):
        vertice1 = Vertice(self.vertice1.index, dim2)
        vertice2 = Vertice(self.vertice2.index, dim2)
        vertice3 = Vertice(self.vertice3.index, dim2)
        vertice4 = Vertice(self.vertice4.index, dim2)
        return Face([vertice1, vertice2, vertice3, vertice4])

    def expand_to_body(self, n = 0):
        if n == 0:
            curr_dim = len(self.vertice1.binary)
        else:
            curr_dim = n
        original_face = self
        original_face = self.expand_dim(curr_dim + 1)
        new_face = original_face.add(2**curr_dim, curr_dim+1)
        composed_face1 = Face([original_face.vertice1, original_face.vertice2, Vertice(original_face.vertice1.index + 2**(curr_dim), curr_dim+1), Vertice(original_face.vertice2.index+ 2**(curr_dim), curr_dim+1)])
        composed_face2 = Face([original_face.vertice2, original_face.vertice4, Vertice(original_face.vertice2.index + 2**(curr_dim), curr_dim+1), Vertice(original_face.vertice4.index+ 2**(curr_dim), curr_dim+1)])
        composed_face3 = Face([original_face.vertice3, original_face.vertice4, Vertice(original_face.vertice3.index + 2**(curr_dim), curr_dim+1), Vertice(original_face.vertice4.index+ 2**(curr_dim), curr_dim+1)])
        composed_face4 = Face([original_face.vertice1, original_face.vertice3, Vertice(original_face.vertice1.index + 2**(curr_dim), curr_dim+1), Vertice(original_face.vertice3.index+ 2**(curr_dim), curr_dim+1)])
        return Body([original_face, new_face, composed_face1, composed_face2, composed_face3, composed_face4])

    def plot(self, r, draw, rgba, highlightPoints = False):
        rotated_face = np.transpose(np.dot(r, np.transpose(self.face_matrix)))
        [v1,v2,v3,v4] = shift + scale * rotated_face
        draw.polygon([(v1[0], v1[1]), (v2[0], v2[1]), (v4[0], v4[1]), (v3[0], v3[1])], rgba) #First v4 then v3 because edges are not in increasing order
        if highlightPoints:
            for vv in [v1, v2, v3, v4]:
                [vx,vy] = vv[:2]
                draw.ellipse( (vx-4,vy-4,vx+4,vy+4), fill = 'red', outline = 'red')
            Edge(self.vertice1, self.vertice2).plot(r,draw,rgba,5)
            Edge(self.vertice2, self.vertice4).plot(r,draw,rgba,5)
            Edge(self.vertice3, self.vertice4).plot(r,draw,rgba,5)
            Edge(self.vertice1, self.vertice3).plot(r,draw,rgba,5)

    def plot_vid_ready(self, r, draw, rgba):
        dim = r.shape[0]
        reflection = np.ones(dim)
        reflection[1] = -1
        v1 = new_vector(r,self.vertice1.binary * reflection * scale + shift[:dim])
        v2 = new_vector(r,self.vertice2.binary * reflection * scale + shift[:dim])
        v3 = new_vector(r,self.vertice3.binary * reflection * scale + shift[:dim])
        v4 = new_vector(r,self.vertice4.binary * reflection * scale + shift[:dim])
        draw.polygon([(v1[0],v1[1]), (v2[0],v2[1]), (v4[0],v4[1]), (v3[0],v3[1])], rgba)

class Body():
    def __init__(self, faces):
        [f1,f2,f3,f4,f5,f6] = faces
        self.face1 = f1
        self.face2 = f2
        self.face3 = f3
        self.face4 = f4
        self.face5 = f5
        self.face6 = f6
    
    def add(self, a, dim):
        newf1 = self.face1.add(a, dim)
        newf2 = self.face2.add(a, dim)
        newf3 = self.face3.add(a, dim)
        newf4 = self.face4.add(a, dim)
        newf5 = self.face5.add(a, dim)
        newf6 = self.face6.add(a, dim)
        return Body([newf1,newf2,newf3,newf4,newf5,newf6])

    def plot(self, r, draw, rgba):
        self.face1.plot(r, draw, rgba, True)
        self.face2.plot(r, draw, rgba, True)
        self.face3.plot(r, draw, rgba, True)
        self.face4.plot(r, draw, rgba, True)
        self.face5.plot(r, draw, rgba, True)
        self.face6.plot(r, draw, rgba, True)

class Cube():    
    def __init__(self, n = 4, r = None):
        self.dim = n
        if r == None:
            self.r = np.eye(n)
        else:
            self.r = r
        config = self.generate_edges(n)
        self.vertices = config['vertices']
        self.edges = config['edges']
        self.generate_vertice_matrix()
        self.faces = self.generate_faces(n)
        self.bodies = self.generate_bodies(n)
        global scale

    def generate_vertice_matrix(self):
        self.vertice_matrix = []
        self.vertice_coordinate_sums = []
        for v in self.vertices:
            self.vertice_matrix.append(v.binary)
            self.vertice_coordinate_sums.append( sum(v.binary))
        self.vertice_matrix = np.array(self.vertice_matrix)
        self.vertice_coordinate_sums = np.array(self.vertice_coordinate_sums)

    def generate_edges(self,n):
        if n == 1:
            v1 = Vertice(0, self.dim)
            v2 = Vertice(1, self.dim)
            return { 'vertices': np.array([v1, v2]), 'edges': np.array([Edge(v1, v2)]) }
        else:
            previous = self.generate_edges(n-1)
            vertices = previous['vertices']
            edges = previous['edges']
            for i in previous['vertices']:
                v_new = Vertice(i.index + 2**(n-1), self.dim)
                vertices = np.insert(vertices, len(vertices), v_new )
                edges = np.insert(edges,len(edges),Edge(i, v_new))
            for i in previous['edges']: #Loop through edges
                edges = np.insert(edges, len(edges), (Edge(vertices[i.vertice1.index + 2**(n-1)], vertices[i.vertice2.index + 2**(n-1)])) )
            return {'vertices' : vertices, 'edges' : edges}

    def generate_faces(self, n):
        if n < 2:
            return None
        elif n == 2:
            vertices = self.generate_edges(2)['vertices']
            return np.array([Face( [vertices[0], vertices[1], vertices[2], vertices[3]])])
        else:
            faces = previous_faces = self.generate_faces(n-1)
            previous_edges = self.generate_edges(n-1)['edges']
            current_edges = self.generate_edges(n)
            current_vertices = current_edges['vertices']
            for i in previous_faces:
                faces = np.insert(faces, len(faces), Face(current_vertices[i.vertice_indices + 2**(n-1)]))
            for i in previous_edges:
                new_face = Face([i.vertice1, i.vertice2, current_vertices[i.vertice1.index + 2**(n-1)], current_vertices[i.vertice2.index + 2**(n-1)] ])
                faces = np.insert(faces,len(faces), new_face)
            return faces

    def generate_bodies(self, n):
        if n < 3:
            return None
        elif n == 3:
            faces = self.generate_faces(3)
            return np.array([Body(faces)])
        else:
            bodies = previous_bodies = self.generate_bodies(n-1)
            previous_faces = self.generate_faces(n-1)
            for i in previous_bodies:
                bodies = np.insert(bodies, len(bodies), i.add(2**(n-1),n))
            for i in previous_faces:
                bodies = np.insert(bodies, len(bodies), i.expand_to_body(n-1))
            return bodies

    def generate_sequential_edges(self):
        self.sequential_edges = []
        for i in range(len(self.vertices) - 1):
            self.sequential_edges.append(Edge(self.vertices[i], self.vertices[i+1]))

    def generate_classic_edges(self):
        self.classic_edges = []
        for i in self.edges:
            self.classic_edges.append(np.array([i.vertice1.binary, i.vertice2.binary]))
        self.classic_edges = np.array(self.classic_edges)

    def plot_edges(self, r = None, seq = False, j = 0):
        if r == None:
            r = rotation(self.dim)
        im = Image.new("RGB", (2048, 2048), (1,1,1))
        draw = ImageDraw.Draw(im,'RGBA')
        if seq:
            self.generate_sequential_edges()
            edges = self.sequential_edges
        else:
            edges = self.edges
        for edge in edges:
            [v1, v2] = [ np.dot(r, edge.vertice1.binary), np.dot(r, edge.vertice2.binary)]
            [v1x,v1y] = (shift[:self.dim] + scale * v1)[0:2]
            [v2x,v2y] = (shift[:self.dim] + scale * v2)[0:2]
            draw.line((v1x, v1y, v2x, v2y), fill=(255,165,0), width=2)
        return [im, draw]
        #im.save('Images\\RotatingCube\\im' + str(j) + '.png')

    def plot_faces(self, r = None, j = 0, body_indice = None):
        if r == None:
            r = rotation(self.dim)
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im,'RGBA')
        for f in self.faces:
            f.plot(r, draw, (255, 55, 0, 22))
        for edge in self.edges:
            edge.plot(r, draw, (255,131,0))
        if body_indice != None:
            indx = 0
            colors = [(255, 255, 0, 100), (200, 80, 100, 100), (255,0,0,100), (0,255,0,100), (0,0,255,100), (0,255,255,100), (255,0,255,100), (120,80,200,100)]
            for bi in body_indice:
                j = j + bi * 10**indx + 1
                body = self.bodies[bi]
                body.plot(r, draw, colors[bi])
                indx = indx + 1        
        im.save('Images\\RotatingCube\\im' + str(j) + '.png')

def rotate_object(n=5):
    c1 = Cube(n)
    for j in range(80):
        r = rotation(n, np.pi*2*j/80.0)
        #c1.plot_edges(r,False,j)
        c1.plot_faces(r,j)

def circle_cubes(n=4, j = 29):
    c1 = Cube(n)
    r = rotation(n, np.pi*2*j/80.0)
    for b in range(8):
        c1.plot_faces(r, j, [b])
    c1.plot_faces(r, j)
    c1.plot_faces(r, j, range(8))

def zoom_in(width = 15):
    global scale
    c1 = Cube(3)
    font = ImageFont.truetype("arial.ttf", 150)
    im_ind = 0
    scale = 500
    for j in np.arange(0,10,0.5):
        r = rotation(3,np.pi*2*13/80.0)
        [im, draw] = c1.plot_edges(r)
        c1.vertices[0].plot(r, draw, "red", width)
        c1.vertices[7].plot(r, draw, "red", width)
        for vv in range(8):
            c1.vertices[vv].plot(r, draw, "red", width)
        rotated_vertices = np.transpose(np.dot(r,np.transpose(c1.vertice_matrix)))*scale + shift[:3]
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        scale = scale - 10
        im_ind = im_ind + 1

def zoom_out(width = 15):
    global scale
    c1 = Cube(3)
    font = ImageFont.truetype("arial.ttf", 150)
    im_ind = 0
    scale = 500
    for j in np.arange(0,10,0.5):
        r = rotation(3,np.pi*2*13/80.0)
        [im, draw] = c1.plot_edges(r)
        c1.vertices[0].plot(r, draw, "red", width)
        c1.vertices[7].plot(r, draw, "red", width)
        for vv in range(8):
            c1.vertices[vv].plot(r, draw, "red", width)
        rotated_vertices = np.transpose(np.dot(r,np.transpose(c1.vertice_matrix)))*scale + shift[:3]
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        scale = scale - 10
        im_ind = im_ind + 1

def cube_body_diagonal(width = 15):
    global scale
    c1 = Cube(3)
    font = ImageFont.truetype("arial.ttf", 150)
    im_ind = 10
    for j in np.arange(0,1.0,1):
        r = rotation(3,np.pi*2*3/20.0) # replace second 3 by j.
        [im, draw] = c1.plot_edges(r)
        #draw.text((250,200), "Next video - Pascals\n triangles in hyper cubes", (255,255,255), font=font)
        c1.vertices[0].plot(r, draw, "red", width)
        c1.vertices[7].plot(r, draw, "red", width)
        for vv in range(8):
            c1.vertices[vv].plot(r, draw, "red", width)
        rotated_vertices = np.transpose(np.dot(r,np.transpose(c1.vertice_matrix)))*scale + shift[:3]
        draw.polygon([(rotated_vertices[1][0], rotated_vertices[1][1]), (rotated_vertices[2][0], rotated_vertices[2][1]), (rotated_vertices[4][0], rotated_vertices[4][1])], (120,80,200,100))
        #c1.vertices[1].plot(r, draw, (120,80,200), width)
        #c1.vertices[2].plot(r, draw, (120,80,200), width)
        #c1.vertices[4].plot(r, draw, (120,80,200), width)
        #draw.polygon([(rotated_vertices[3][0], rotated_vertices[3][1]), (rotated_vertices[5][0], rotated_vertices[5][1]), (rotated_vertices[6][0], rotated_vertices[6][1])], (200, 80, 100, 100))
        #c1.vertices[3].plot(r, draw, (200, 80, 100), width)
        #c1.vertices[5].plot(r, draw, (200, 80, 100), width)
        #c1.vertices[6].plot(r, draw, (200, 80, 100), width)        
        #draw.line((rotated_vertices[0][0], rotated_vertices[0][1], rotated_vertices[7][0], rotated_vertices[7][1]), fill="yellow", width=1)
        first_intersection = np.dot(r,np.array([.3333,.3333,.3333])) * scale + shift[:3]
        for ind in [1,2,4]:
            draw.line((first_intersection[0], first_intersection[1], rotated_vertices[ind][0], rotated_vertices[ind][1]) , fill = "purple", width=4 )
        #draw.ellipse( (first_intersection[0]-width,first_intersection[1]-width,first_intersection[0]+width,first_intersection[1]+width), fill = (120,80,200), outline = (120,80,200))
        draw.ellipse( (first_intersection[0]-3,first_intersection[1]-3,first_intersection[0]+3,first_intersection[1]+3), fill = (0,0,0), outline = (0,0,0))
        first_intersection = np.dot(r,np.array([.6666,.6666,.6666])) * scale + shift[:3]
        #draw.ellipse( (first_intersection[0]-width,first_intersection[1]-width,first_intersection[0]+width,first_intersection[1]+width), fill = (200,80,100), outline = (120,80,200))
        draw.ellipse( (first_intersection[0]-3,first_intersection[1]-3,first_intersection[0]+3,first_intersection[1]+3), fill = (0,0,0), outline = (0,0,0))
        for ed in c1.edges:
            ed.plot(r,draw,'orange')
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

def cube_body_diagonal_scene(draw):
    global scale
    im_ind = 0
    r = rotation(3,np.pi*2*3/20.0)
    c1 = Cube(3)
    im = Image.new("RGB", (2048, 2048), "black")
    back = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\RotatingCube\Temp4\\im22.png')
    #draw = ImageDraw.Draw(im,'RGBA')
    '''
    #draw.text((580, 1400), "(a + a )", font=font, fill = "orange")
    #draw.text((580, 1400), "(a + a ) (a + a )", font=font, fill = "orange")
    #draw.text((580, 1400), "(a + a ) (a + a ) (a + a )", font=font, fill = "orange")
    draw.text((580, 1400), "(1 + a)", font=font, fill = "orange")
    draw.text((872, 1386), "3", font=font_small, fill = "orange")
    #draw.text((671, 1412), "0", font=font_small, fill = "orange")
    #draw.text((1010, 1412), "0", font=font_small, fill = "orange")
    #draw.text((1364, 1412), "0", font=font_small, fill = "orange")
    #draw.text((832, 1412), "1", font=font_small, fill = "orange")
    #draw.text((1010+161, 1412), "1", font=font_small, fill = "orange")
    #draw.text((1364+161, 1412), "1", font=font_small, fill = "orange")
    draw.text((372, 1611), "= 1", font=font, fill = "orange")
    draw.text((535, 1611), " + 3a", font=font, fill = "orange")
    draw.text((750, 1611), " + 3a", font=font, fill = "orange")
    draw.text((976, 1612), "2", font=font_small, fill = "orange")
    draw.text((1010, 1611), " + a", font=font, fill = "orange")
    draw.text((1184, 1612), "3", font=font_small, fill = "orange")
    '''
    rotated_vertices = np.transpose(np.dot(r, np.transpose(c1.vertice_matrix))) * scale + shift[:3]
    axis = rotated_vertices[7] - rotated_vertices[0]
    for j in range(0,1):        
        im = Image.new("RGB", (2048, 2048), "black")
        #draw = ImageDraw.Draw(im,'RGBA')
        angle = 2 * np.pi * j / 50.0
        #r1 = general_rotation(axis,angle)
        r1 = np.eye(3)
        r2 = np.dot(r1,r)
        rotated_vertices = np.transpose(np.dot(r2, np.transpose(c1.vertice_matrix))) * scale + shift[:3]
        first_intersection = np.dot(r2, np.array([.3333,.3333,.3333])) * scale + shift[:3]
        for_polygon = []
        for ind in [1,2,4]:
            center = first_intersection[:2]
            extent = rotated_vertices[ind][:2]
            reduced = center + (extent - center) * 1.0
            draw.line((center[0], center[1], reduced[0], reduced[1]) , fill = (120,80,200), width=4)
            for_polygon.append( (reduced[0], reduced[1]) )
        draw.polygon(for_polygon, (120,80,200,100))
        for ed in c1.edges:
            ed.plot(r2, draw,'yellow')
        for ver in c1.vertices:
            ver.plot(r2, draw,'red',15)
        first_intersection = np.dot(r2, np.array([.6666,.6666,.6666])) * scale + shift[:3]
        for_polygon = []
        for ind in [3,5,6]:
            center = first_intersection[:2]
            extent = rotated_vertices[ind][:2]
            reduced = center + (extent - center) * 1.0
            draw.line((center[0], center[1], reduced[0], reduced[1]) , fill = (200,80,100), width=4)
            for_polygon.append( (reduced[0], reduced[1]))
        draw.polygon(for_polygon, (200,80,100,100))
        center = rotated_vertices[0][:2]
        extent = rotated_vertices[7][:2]
        reduced = center + (extent - center) * (0.33333 + 0.66666)
        draw.line((center[0], center[1], reduced[0], reduced[1]) , fill = "green", width=5)
        c1.vertices[2].plot(r2, draw, (120,80,200), 15)
        c1.vertices[4].plot(r2, draw, (120,80,200), 15)
        c1.vertices[1].plot(r2, draw, (120,80,200), 15)
        c1.vertices[3].plot(r2, draw, (200,80,100), 15)
        c1.vertices[5].plot(r2, draw, (200,80,100), 15)
        c1.vertices[6].plot(r2, draw, (200,80,100), 15)
        #c1.vertices[0].plot(r2, draw, (64,224,208), 15)
        #c1.vertices[7].plot(r2, draw, (255,255,0), 15)
        #draw.text((1192, 1265), "(1, ", font=font, fill = (120,80,200))
        #im.paste(back,(1,1344))
        #im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        return draw
        #back.paste(im,mask=im)
        #back.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1
        #scale = scale - 20

'''
@MoneyShot
    Draws a four dimensional teserract with two tetrahedral and one octahedral planes visible.
'''
def teserract_body_diagonal(width = 15, im_ind = 70, scale = 500, shift = np.array([1000,1000,0,0,0])):
    c1 = Cube(4)
    #for j in range(45,46):
    r = np.eye(4)
    r[:3,:3] = rotation(3, np.pi*2*27/80.0)
    r1 = rotation(4, np.pi*2*im_ind/80.0)
    r = np.dot(r, r1)
    [im, draw] = c1.plot_edges(r)
    #write4DEqn(draw)
    rotated_vertices = np.transpose(np.dot(r,np.transpose(c1.vertice_matrix)))*scale + shift[:4]
    hexag = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 2]]]
    sqr1 = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 3]]]
    try:
        draw.polygon(jarvis_convex_hull(sqr1), (255,0,0,60))
    except:
        print "err"
    for ver in c1.vertices[c1.vertice_coordinate_sums == 3]:
        ver.plot(r, draw, (255,0,0), 10)
        for ver1 in c1.vertices[c1.vertice_coordinate_sums == 3]:
            e = Edge(ver,ver1)
            e.plot(r,draw,(255,0,0), width=2)
    try:
        draw.polygon(jarvis_convex_hull(hexag), (0,255,0,30))
    except:
        print "err"
    
    for ver in c1.vertices[c1.vertice_coordinate_sums == 1]:
        ver.plot(r, draw, (0,0,255), 10)
        for ver1 in c1.vertices[c1.vertice_coordinate_sums == 1]:
            e = Edge(ver,ver1)
            e.plot(r,draw,(0,0,255))
    for ed in [(5,3),(5,6),(5,9),(5,12),(10,3),(10,6),(10,9),(10,12),(3,6),(3,9),(12,6),(12,9)]:
        v1 = rotated_vertices[ed[0]]
        v2 = rotated_vertices[ed[1]]
        draw.line((v1[0], v1[1], v2[0], v2[1]), fill = (0,255,0), width=4)
    for ver in c1.vertices[c1.vertice_coordinate_sums==2]:
        ver.plot(r, draw, (0,255,0), 10)
    sqr2 = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 1]]]
    try:
        draw.polygon(jarvis_convex_hull(sqr2), (0,0,255,60))
    except:
        print "err"
    v1 = rotated_vertices[0]
    v2 = rotated_vertices[15]
    draw.line((v1[0], v1[1], v2[0], v2[1]), fill = (255,255,255), width=2)
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')


'''
@MoneyShot
    Draws a four dimensional teserract with two tetrahedral and one octahedral planes visible.
'''
def teserract_body_diagonal2(width = 15, im_ind = 70, scale = 500, shift = np.array([1000,1000,0,0,0])):
    c1 = Cube(4)
    r = np.eye(4)
    r[:3,:3] = rotation(3, np.pi*2*27/80.0)
    r1 = rotation(4, np.pi*2*im_ind/80.0)
    r = np.dot(r, r1)
    [im, draw] = c1.plot_edges(r)
    rotated_vertices = np.transpose(np.dot(r,np.transpose(c1.vertice_matrix)))*scale + shift[:4]
    hexag = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 2]]]
    sqr1 = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 3]]]
    try:
        draw.polygon(jarvis_convex_hull(sqr1), (255,0,0,60))
    except:
        print "err"
    for ver in c1.vertices[c1.vertice_coordinate_sums == 3]:
        ver.plot(r, draw, (255,0,0), 10)
        for ver1 in c1.vertices[c1.vertice_coordinate_sums == 3]:
            e = Edge(ver,ver1)
            e.plot(r,draw,(255,0,0), width=2)
    try:
        draw.polygon(jarvis_convex_hull(hexag), (0,255,0,30))
    except:
        print "err"
    
    for ver in c1.vertices[c1.vertice_coordinate_sums == 1]:
        ver.plot(r, draw, (0,0,255), 10)
        for ver1 in c1.vertices[c1.vertice_coordinate_sums == 1]:
            e = Edge(ver,ver1)
            e.plot(r,draw,(0,0,255))
    for ed in [(5,3),(5,6),(5,9),(5,12),(10,3),(10,6),(10,9),(10,12),(3,6),(3,9),(12,6),(12,9)]:
        v1 = rotated_vertices[ed[0]]
        v2 = rotated_vertices[ed[1]]
        draw.line((v1[0], v1[1], v2[0], v2[1]), fill = (0,255,0), width=4)
    for ver in c1.vertices[c1.vertice_coordinate_sums==2]:
        ver.plot(r, draw, (0,255,0), 10)
    sqr2 = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 1]]]
    try:
        draw.polygon(jarvis_convex_hull(sqr2), (0,0,255,60))
    except:
        print "err"
    v1 = rotated_vertices[0]
    v2 = rotated_vertices[15]
    draw.line((v1[0], v1[1], v2[0], v2[1]), fill = (255,255,255), width=2)
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')


def tetrahedron(draw, r, offset = [500,1000,0], rgb = (216,52,52)):
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
        for i in tet:
            ver = i * 300 + offset
            draw.ellipse((ver[0]-150,ver[1]-150,ver[0]+150,ver[1]+150), fill = rgba)
            draw.ellipse((ver[0]-5,ver[1]-5,ver[0]+5,ver[1]+5), fill = rgb)
        for i in range(len(tet)):
            for k in range(i,len(tet)):
                ver1 = tet[i] * 300 + offset
                ver2 = tet[k] * 300 + offset
                draw.line((ver1[0],ver1[1],ver2[0],ver2[1]), fill = rgb, width = 2)
        #im.save('Images\\RotatingCube\\im' + str(j) + '.png')

def octahedron(draw, r):
    tet_orig = np.array([
            [0,0,0],
            [1,0,0],
            [0,1,0],
            [1,1,0],
            [0.5,0.5,0.7071],
            [0.5,0.5,-0.7071]#0.7071
        ])
    offset = [1500,1000,0]
    for j in range(0,1):
        #r = general_rotation(np.array([1,2,0.4]), np.pi*2*j/80.0)
        #im = Image.new("RGB", (2048, 2048), "black")
        #draw = ImageDraw.Draw(im,'RGBA')
        tet = np.dot(tet_orig, r)
        for i in tet:
            ver = i * 300 + offset
            draw.ellipse((ver[0]-150,ver[1]-150,ver[0]+150,ver[1]+150), fill = (43,183,31,100))
            draw.ellipse((ver[0]-5,ver[1]-5,ver[0]+5,ver[1]+5), fill = (43,183,31))
        indxs = [0,1,3,2]
        for i in range(4):
            k = indxs[(i) % 4]
            l = indxs[(i+1) % 4]
            ver1 = tet[k] * 300 + offset
            ver2 = tet[l] * 300 + offset
            draw.line((ver1[0],ver1[1],ver2[0],ver2[1]), fill = (0,255,0,80), width = 2)
            ver_top = tet[4] * 300 + offset
            draw.line((ver1[0],ver1[1],ver_top[0],ver_top[1]), fill = (0,255,0,80), width = 2)
            ver_top = tet[5] * 300 + offset
            draw.line((ver1[0],ver1[1],ver_top[0],ver_top[1]), fill = (0,255,0,80), width = 2)
        #im.save('Images\\RotatingCube\\im' + str(j) + '.png')

def fourDExplanation(j = 0, k = 0):
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im,'RGBA')
    font = ImageFont.truetype("arial.ttf", 100)
    font_small = ImageFont.truetype("arial.ttf", 60)
    draw.text((282, 220), "(1 + a )", font=font, fill = "orange")
    draw.text((664, 220), " = 1 + 4a + 6a + 4a + a", font=font, fill = "orange")
    draw.text((944, 220), "4", font=font, fill = (216,52,52))
    draw.text((1401, 220), "4", font=font, fill = (0,0,255))
    draw.text((1175, 220), "6", font=font, fill = (0,255,0))
    draw.text((1281, 211), "2", font=font_small, fill = "orange")
    draw.text((1506, 211), "3", font=font_small, fill = "orange")
    draw.text((1674, 211), "4", font=font_small, fill = "orange")
    #draw.text((610,220), "0", font = font_small, fill = "orange")
    draw.text((600,211), "4", font = font_small, fill = "orange")
    r = general_rotation(np.array([1,2,0.4]), np.pi*2*k/80.0)
    octahedron(draw, r)
    tetrahedron(draw, np.eye(3))
    tetrahedron(draw, np.eye(3), [500,1550,0],(0,0,255))
    im.save('Images\\RotatingCube\\im' + str(j) + '.png')

def write4DEqn(draw):
    font = ImageFont.truetype("arial.ttf", 100)
    font_small = ImageFont.truetype("arial.ttf", 60)
    draw.text((282, 220), "(1 + a )", font=font, fill = "orange")
    draw.text((664, 220), " = 1 + 4a + 6a + 4a + a", font=font, fill = "orange")
    draw.text((944, 220), "4", font=font, fill = (216,52,52))
    draw.text((1401, 220), "4", font=font, fill = (0,0,255))
    draw.text((1175, 220), "6", font=font, fill = (0,255,0))
    draw.text((1281, 211), "2", font=font_small, fill = "orange")
    draw.text((1506, 211), "3", font=font_small, fill = "orange")
    draw.text((1674, 211), "4", font=font_small, fill = "orange")
    draw.text((600,211), "4", font = font_small, fill = "orange")

def make_transparent():
    img = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\RotatingCube\Temp4\\im22.png')
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\RotatingCube\Temp4\\im23.png')

'''
Returns points in the order required for a convex hull.
args:
    points: An array of numpy arrays representing the points to be convex hulled in any order.
'''
def jarvis_convex_hull(points):
    #for i in range(len(points)):
    #    points[i] = points[i] + np.random.randn()*1e-2
    start_indx = np.argmax(points[:,0]) #Point with the highest y-coordinate
    res = []
    res.append( (points[start_indx][0], points[start_indx][1]) )
    added_points = set()
    added_points.add(start_indx)
    while True:
        for i in range(len(points)):
            exit = True
            if i != start_indx and i not in added_points:
                signs = 0
                threshold = len(points) - 2
                for j in range(len(points)):
                    if j != i and j != start_indx:
                        m = (points[i][1] - points[start_indx][1] * 1.00001)/(points[i][0] - points[start_indx][0] * 1.00001)
                        check = points[j][1] - points[start_indx][1] - m * (points[j][0] - points[start_indx][0])
                        if abs(check) < 1e-2:
                            if dist(points[start_indx],points[j]) > dist(points[start_indx],points[i]):
                                threshold = threshold + 1 
                            else:
                                threshold = threshold - 1
                        elif  check > 0:
                            signs = signs + 1
                        else:
                            signs = signs - 1
                if abs(signs) >= threshold:
                    exit = False
                    res.append( (points[i][0], points[i][1]))
                    added_points.add(i)
                    start_indx = i
                    break
        if exit:
            return res

def dist(pt1,pt2):
    return (pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2

def render_intro():
    im_ind = 0
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im,'RGBA')
    if "linux" in sys.platform:
        font = ImageFont.truetype("FreeMono.ttf", 28, encoding = "unic")
    else:
        font = ImageFont.truetype("arial.ttf", 30)
    width = 9
    [vx,vy] = np.array([0,0])*scale + shift[:2]
    draw.ellipse( (vx-width,vy-width,vx+width,vy+width), fill = "red", outline = "red")
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    im_ind += 1
    draw.line((0,1000,2048,1000), fill="silver", width=1)
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    im_ind += 1
    #draw.text((vx, vy+20),"0",(255,255,255),font=font)
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    im_ind += 1
    ## Line from 0 to 1.
    for i in np.arange(0,1,0.1):
        [vx,vy] = np.array([i,0])*scale + shift[:2]
        draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = (255,0,0,80), outline = (255,0,0,80))
        if i > 0.1:
            vx = vx - 0.1*scale
            draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = "black", outline = "black")
            draw.line((0,1000,2048,1000), fill="silver", width=1)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1

    vx = 0.9 * scale + shift[:1]
    draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = "black", outline = "black")
    [vx,vy] = np.array([1,0])*scale + shift[:2]
    draw.line((0,1000,2048,1000), fill="silver", width=1)
    draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = "red", outline = "red")
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    im_ind += 1
    #draw.text((vx, vy+20),"1",(255,255,255),font=font)
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    im_ind += 1
    draw.line((1000,0,1000,2048), fill="silver", width=1)
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    im_ind += 1
    #draw.text((1018, 1020),",0",(255,255,255),font=font)
    #draw.text((scale + 1018, 1020),",0",(255,255,255),font=font)
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    im_ind += 1

    for i in np.arange(0,1.1,0.1):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im,'RGBA')
        draw = render_scene(draw)
        draw.line((1000, 1000 - i * scale, 1000 + scale, 1000 - i * scale), fill="silver", width=1)
        [vx, vy] = [1000, 1000 - i * scale]
        draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = (255,0,0,80), outline = (255,0,0,80))
        [vx, vy] = [1000 + scale, 1000 - i * scale]
        draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = (255,0,0,80), outline = (255,0,0,80))
        #draw.text((1018, 1020),",0",(255,255,255),font=font)
        #draw.text((scale + 1018, 1020),",0",(255,255,255),font=font)
        #draw.text((1000 + scale, 1000+20),"1",(255,255,255),font=font)
        #draw.text((1000, 1000+20),"0",(255,255,255),font=font)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1

    for j in range(0,10):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im,'RGBA')
        r = rotation(3, -j*np.pi/50.0)
        draw = render_scene(draw,r,9,True)
        #draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = (255,0,0), outline = (255,0,0))
        #vx = vx - scale
        #draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = (255,0,0), outline = (255,0,0))
        #vx = vx + scale
        #draw.text((1018, 1020),",0",(255,255,255),font=font)
        #draw.text((scale + 1018, 1020),",0",(255,255,255),font=font)
        #draw.text((1000 + scale, 1000+20),"1",(255,255,255),font=font)
        #draw.text((1000, 1000+20),"0",(255,255,255),font=font)
        #draw.text((1000, 1000-scale-42),"0,1",(255,255,255),font=font)
        #draw.text((1000+scale, 1000-scale-42),"1,1",(255,255,255),font=font)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1

    for k in np.arange(0,1.1,0.1):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im,'RGBA')
        r = rotation(3, -j*np.pi/50.0)
        draw = render_scene(draw,r,9,True)
        draw = translate_square(r, k, draw)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1

    for i in range(1,10):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        draw = render_scene(draw, r, 9, True)
        draw = translate_square(r, k, draw, i)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1


    ''' Rotate the cube and bring it back.
    for l in range(21):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        r = rotation(3, -9*np.pi/50.0 - l * np.pi/100.0)
        draw = render_scene(draw, r, 9, True)
        draw = translate_square(r, k, draw, 9)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1

    for l in range(21):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        r = rotation(3, -9*np.pi/50.0 - 20*np.pi/100.0 + l * np.pi/100.0)
        draw = render_scene(draw, r, 9, True)
        draw = translate_square(r, k, draw, 9)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1

    for i in range(-1,6):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        draw = render_scene(draw, r, 9, True)
        highlight_cube_edge(r, draw, i)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1

        c1 = Cube(3)
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        draw = render_scene(draw, r, 9, True)
        highlight_cube_edge(r, draw, -1)
        for i in [1,3,5]:
            c1.faces[i].plot_vid_ready(r,draw,(30,144,255,100))
        c1.vertices[6].plot_vid_ready(r,draw,(30,144,255),15)
        c1.vertices[2].plot_vid_ready(r,draw,"gold",15)
        c1.vertices[4].plot_vid_ready(r,draw,"gold",15)
        c1.vertices[7].plot_vid_ready(r,draw,"gold",15)
        for i in [6,9,11]:
            c1.edges[i].plot_vid_ready(r,draw,(30,144,255),5)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1
        #Vertice - 6
        #Connected vertices - 2,4,7
        #Edges - 6,9,11
        #Faces - 1,3,5
        # 6,9 -> 3
        # 9,11 -> 1
        # 6,11 -> 5
        '''

    #Now we move on to 4-d.
    r = rotation(3, -9*np.pi/50.0)
    r1 = np.eye(4)
    r1[0:3,0:3] = r
    r = r1
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    draw = render_scene_4d(draw, r)
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    im_ind += 1

    for j in range(10,19):
        theta = -j*np.pi/50.0
        gamma = -(j-9)*np.pi/50.0
        [r1,r2,r3,r4,r5,r6] = rotation_matrix(theta,theta,theta,gamma,gamma,gamma)
        r = np.dot(r6,np.dot(r5,np.dot(r4,np.dot(r3,np.dot(r1,r2)))))
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        draw = render_scene_4d(draw, r)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1

    for i in np.arange(0,1.1,0.1):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        draw = render_scene_4d(draw, r, 9, i)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1

    for k in range(2,8):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        draw = render_scene_4d(draw, r, 9, i, k)
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1

    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    #draw = render_scene_4d(draw, r, 9, i, np.array([2,3,4,5,6,7]))
    draw = render_scene_4d(draw, r, 9, 1.0)
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    im_ind += 1

    c1 = Cube(4)
    #for i in range(12,20):#edges
    #for i in range(12,23):#faces
    for i in range(2,8):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        render_scene_4d(draw, r, 9, 1.0, 0)
        #c1.edges[i].plot_vid_ready(r,draw,(255,215,0,100),5)
        #c1.faces[i].plot_vid_ready(r,draw,(255,215,0,100))
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind += 1

    c1 = Cube(4)
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    render_scene_4d_axis(draw, r, 9, 1.0)
    for i in c1.vertices:
        i.plot_vid_ready(r,draw,"red")
    for i in c1.edges:
        i.plot_vid_ready(r,draw,(192,192,192,100),4)
    for i in c1.faces:
        i.plot_vid_ready(r,draw,(192,192,192,80))
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    im_ind += 1


def render_scene(draw, r = np.eye(3), width = 9, renderCube = False):
    x_axis_start = new_vector(r, np.array([0, 1000, 0]))
    x_axis_end = new_vector(r, np.array([2048, 1000, 0]))
    y_axis_start = new_vector(r, np.array([1000, 0, 0]))
    y_axis_end = new_vector(r, np.array([1000, 2048, 0]))
    z_axis_start = new_vector(r, np.array([1000, 1000, -1000]))
    z_axis_end = new_vector(r, np.array([1000, 1000, 2048]))
    c1 = Cube(3)
    [v1,v2,v3] = new_vector(r, c1.vertice_matrix[0] * scale + shift[:3])
    draw.line((x_axis_start[0],x_axis_start[1],x_axis_end[0],x_axis_end[1]), fill="silver", width=1)
    draw.line((y_axis_start[0],y_axis_start[1],y_axis_end[0],y_axis_end[1]), fill="silver", width=1)
    draw.line((z_axis_start[0],z_axis_start[1],z_axis_end[0],z_axis_end[1]), fill="silver", width=1)
    draw.ellipse((v1-width,v2-width,v1+width,v2+width), fill = (255,0,0), outline = (255,0,0))
    [u1,u2,u3] = new_vector(r, c1.vertice_matrix[1] * scale + shift[:3])
    draw.ellipse((u1-width,u2-width,u1+width,u2+width), fill = (255,0,0), outline = (255,0,0))
    if renderCube:
        [l1,l2,l3] = new_vector(r, -c1.vertice_matrix[2] * scale + shift[:3])
        draw.ellipse((l1-width,l2-width,l1+width,l2+width), fill = (255,0,0), outline = (255,0,0))
        [m1,m2,m3] = new_vector(r, np.array([1,-1,0]) * scale + shift[:3])
        draw.ellipse((m1-width,m2-width,m1+width,m2+width), fill = (255,0,0), outline = (255,0,0))
        draw.polygon([(v1, v2), (u1, u2), (m1, m2), (l1, l2)], (192,192,192,80))
    return draw

def new_vector(r, v):
    translate = np.zeros(dim)
    translate[0] = 1000
    translate[1] = 1000
    v = v - translate #1000,1000 should go to 0,0. 
    v = v / scale
    v = np.dot(r,v)
    v = v * scale
    v = v + translate
    return v

def new_vector_4d(r, v):
    v = v - np.array([1000, 1000, 0, 0]) #1000,1000 should go to 0,0. 
    v = v / scale
    v = np.dot(r,v)
    v = v * scale
    v = v + np.array([1000, 1000, 0, 0])
    return v

def translate_square(r, z, draw, drawCubeConnectors = -1):
    rgba = (255,0,0,80)
    c1 = Cube(3)
    width = 9
    [v1,v2,v3] = new_vector(r, (c1.vertice_matrix[0] + np.array([0,0,z]))* scale + shift[:3])
    [vorig1,vorig2,vorig3] = new_vector(r, (c1.vertice_matrix[0]) * scale + shift[:3])
    draw.ellipse((v1-width,v2-width,v1+width,v2+width), fill = "red", outline = (255,0,0))
    [u1,u2,u3] = new_vector(r, (c1.vertice_matrix[1] + np.array([0,0,z])) * scale + shift[:3])
    [uorig1,uorig2,uorig3] = new_vector(r, (c1.vertice_matrix[1]) * scale + shift[:3])
    draw.ellipse((u1-width,u2-width,u1+width,u2+width), fill = "red", outline = (255,0,0))
    [l1,l2,l3] = new_vector(r, (c1.vertice_matrix[2]*np.array([1,-1,1]) + np.array([0,0,z])) * scale + shift[:3])
    [lorig1,lorig2,lorig3] = new_vector(r, (c1.vertice_matrix[2]*np.array([1,-1,1])) * scale + shift[:3])
    draw.ellipse((l1-width,l2-width,l1+width,l2+width), fill = "red", outline = (255,0,0))
    [m1,m2,m3] = new_vector(r, (np.array([1,-1,0]) + np.array([0,0,z])) * scale + shift[:3])
    [morig1,morig2,morig3] = new_vector(r, (c1.vertice_matrix[3]*np.array([1,-1,1])) * scale + shift[:3])
    draw.ellipse((m1-width,m2-width,m1+width,m2+width), fill = "red", outline = (255,0,0))
    draw.polygon([(v1, v2), (u1, u2), (m1, m2), (l1, l2)], (192,192,192,80))
    if drawCubeConnectors <= 0:
        return draw
    if drawCubeConnectors >= 5:
        if drawCubeConnectors >= 5:
            draw.polygon([(v1, v2), (u1, u2), (uorig1, uorig2), (vorig1, vorig2)], (192,192,192,80))
        if drawCubeConnectors >= 6:
            draw.polygon([(u1, u2), (m1, m2), (morig1, morig2), (uorig1, uorig2)], (192,192,192,80))
        if drawCubeConnectors >= 7:
            draw.polygon([(l1, l2), (m1, m2), (morig1, morig2), (lorig1, lorig2)], (192,192,192,80))
        if drawCubeConnectors >= 8:
            draw.polygon([(l1, l2), (v1, v2), (vorig1, vorig2), (lorig1, lorig2)], (192,192,192,80))
    #else:
    if drawCubeConnectors >= 1:
        draw.line((v1, v2, vorig1, vorig2), fill = "silver", width = 1)
    if drawCubeConnectors >= 2:
        draw.line((u1, u2, uorig1, uorig2), fill = "silver", width = 1)
    if drawCubeConnectors >= 3:
        draw.line((l1, l2, lorig1, lorig2), fill = "silver", width = 1)
    if drawCubeConnectors >= 4:
        draw.line((m1, m2, morig1, morig2), fill = "silver", width = 1)
    
    if drawCubeConnectors == 1:
        draw.line((v1, v2, vorig1, vorig2), fill = (255,0,0), width = 5)
    if drawCubeConnectors == 2:
        draw.line((u1, u2, uorig1, uorig2), fill = (255,0,0), width = 5)
    if drawCubeConnectors == 3:
        draw.line((l1, l2, lorig1, lorig2), fill = (255,0,0), width = 5)
    if drawCubeConnectors == 4:
        draw.line((m1, m2, morig1, morig2), fill = "silver", width = 1)
    if drawCubeConnectors == 5:
        draw.polygon([(v1, v2), (u1, u2), (uorig1, uorig2), (vorig1, vorig2)], (255,0,0,80))
    if drawCubeConnectors == 6:
        draw.polygon([(u1, u2), (m1, m2), (morig1, morig2), (uorig1, uorig2)], (255,0,0,80))
    if drawCubeConnectors == 7:
        draw.polygon([(l1, l2), (m1, m2), (morig1, morig2), (lorig1, lorig2)], (255,0,0,80))
    if drawCubeConnectors == 8:
        draw.polygon([(l1, l2), (v1, v2), (vorig1, vorig2), (lorig1, lorig2)], (255,0,0,80))
    if drawCubeConnectors > 8:
        for e in c1.edges:
            v1 = new_vector(r,e.vertice1.binary*np.array([1,-1,1])*scale+shift[:3])
            v2 = new_vector(r,e.vertice2.binary*np.array([1,-1,1])*scale+shift[:3])
            draw.line((v1[0],v1[1],v2[0],v2[1]), fill="silver", width=2)
    return draw

def highlight_cube_edge(r, draw, f_index = -1):
    c1 = Cube(3)
    for v in c1.vertices:
        v.plot_vid_ready(r,draw,"red")
    for e in c1.edges:
        e.plot_vid_ready(r,draw,"silver")
    for f in c1.faces:
        f.plot_vid_ready(r, draw, (192,192,192,80))
    if f_index >= 0:
        c1.faces[f_index].plot_vid_ready(r, draw, (0,255,0,80))


def render_scene_4d_axis(draw, r = np.eye(4), width = 9, scale = 200, shift = np.array([1000,1000,0])):
    shift2 = -shift + np.array([1000,1000,0])
    x_axis_start = new_vector_4d(r, np.array([0, 1000, 0, 0]))
    x_axis_end = new_vector_4d(r, np.array([2048, 1000, 0, 0]))
    y_axis_start = new_vector_4d(r, np.array([1000, 0, 0, 0]))
    y_axis_end = new_vector_4d(r, np.array([1000, 2048, 0, 0]))
    z_axis_start = new_vector_4d(r, np.array([1000, 1000, -1000, 0]))
    z_axis_end = new_vector_4d(r, np.array([1000, 1000, 2048, 0]))
    w_axis_start = new_vector_4d(r, np.array([1000, 1000, 0, -1000]))
    w_axis_end = new_vector_4d(r, np.array([1000, 1000, 0, 2048]))
    draw.line((x_axis_start[0]-shift2[0],x_axis_start[1]-shift2[1],x_axis_end[0]-shift2[0],x_axis_end[1]-shift2[1]), fill="silver", width=width)
    draw.line((y_axis_start[0]-shift2[0],y_axis_start[1]-shift2[1],y_axis_end[0]-shift2[0],y_axis_end[1]-shift2[1]), fill="silver", width=width)
    draw.line((z_axis_start[0]-shift2[0],z_axis_start[1]-shift2[1],z_axis_end[0]-shift2[0],z_axis_end[1]-shift2[1]), fill="silver", width=width)
    draw.line((w_axis_start[0],w_axis_start[1],w_axis_end[0],w_axis_end[1]), fill="gold", width=width)


def render_xy_plane(draw, r = np.eye(4), width = 5):
    print "rendering"
    for i in np.arange(0,2000,100)*1.0:
        x_axis_start = new_vector_4d(r, np.array([0, i, 0, 0]))
        x_axis_end = new_vector_4d(r, np.array([2048, i, 0, 0]))
        y_axis_start = new_vector_4d(r, np.array([i, 0, 0, 0]))
        y_axis_end = new_vector_4d(r, np.array([i, 2048, 0, 0]))
        draw.line((x_axis_start[0],x_axis_start[1],x_axis_end[0],x_axis_end[1]), fill=(248,50,0,70), width=width)
        draw.line((y_axis_start[0],y_axis_start[1],y_axis_end[0],y_axis_end[1]), fill=(248,50,0,70), width=width)

def render_scene_4d(draw, r = np.eye(4), width = 9, translate = 0, body = 0):
    x_axis_start = new_vector_4d(r, np.array([0, 1000, 0, 0]))
    x_axis_end = new_vector_4d(r, np.array([2048, 1000, 0, 0]))
    y_axis_start = new_vector_4d(r, np.array([1000, 0, 0, 0]))
    y_axis_end = new_vector_4d(r, np.array([1000, 2048, 0, 0]))
    z_axis_start = new_vector_4d(r, np.array([1000, 1000, -1000, 0]))
    z_axis_end = new_vector_4d(r, np.array([1000, 1000, 2048, 0]))
    w_axis_start = new_vector_4d(r, np.array([1000, 1000, 0, -1000]))
    w_axis_end = new_vector_4d(r, np.array([1000, 1000, 0, 2048]))
    draw.line((x_axis_start[0],x_axis_start[1],x_axis_end[0],x_axis_end[1]), fill="silver", width=1)
    draw.line((y_axis_start[0],y_axis_start[1],y_axis_end[0],y_axis_end[1]), fill="silver", width=1)
    draw.line((z_axis_start[0],z_axis_start[1],z_axis_end[0],z_axis_end[1]), fill="silver", width=1)
    draw.line((w_axis_start[0],w_axis_start[1],w_axis_end[0],w_axis_end[1]), fill="gold", width=1)
    c1 = Cube(4)
    c1.vertice_matrix[:,1] = -1*c1.vertice_matrix[:,1] # y-axis should be negated.
    for i in range(8):
        [v1,v2,v3,v4] = new_vector_4d(r, c1.vertice_matrix[i] * scale + shift[:4])
        draw.ellipse((v1-width,v2-width,v1+width,v2+width), fill = (255,0,0), outline = (255,0,0))
    for i in range(6):
        faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.faces[i].vertice_indices]]
        draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (192,192,192,80))
    if translate > 0:
        intermediate_vertices = c1.vertice_matrix
        intermediate_vertices[:,3] = intermediate_vertices[:,3] * translate
        if translate < 0.95:
            rgba = (255,0,0,30)
            alp = 30
        else:
            rgba = (255,0,0)
            alp = 80
        for i in range(8, 16):
            [v1,v2,v3,v4] = new_vector_4d(r, intermediate_vertices[i] * scale + shift[:4])
            draw.ellipse((v1-width,v2-width,v1+width,v2+width), fill = rgba, outline = rgba)
        for i in range(6, 12):
            faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in intermediate_vertices[c1.faces[i].vertice_indices]]
            draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (192,192,192,alp))
    for i in range(12):
        e = c1.edges[i]
        e.plot_vid_ready(r,draw,"silver")
    if hasattr(body, '__iter__'):
        for b in body:
            faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[b].face1.vertice_indices]]
            draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
            faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[b].face2.vertice_indices]]
            draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
            faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[b].face3.vertice_indices]]
            draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
            faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[b].face4.vertice_indices]]
            draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
            faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[b].face5.vertice_indices]]
            draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
            faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[b].face6.vertice_indices]]
            draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
    elif body > 0:
        faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[body].face1.vertice_indices]]
        draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
        faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[body].face2.vertice_indices]]
        draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
        faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[body].face3.vertice_indices]]
        draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
        faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[body].face4.vertice_indices]]
        draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
        faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[body].face5.vertice_indices]]
        draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
        faces =  [new_vector_4d(r,i*scale+shift[:4]) for i in c1.vertice_matrix[c1.bodies[body].face6.vertice_indices]]
        draw.polygon([(faces[0][0], faces[0][1]), (faces[1][0], faces[1][1]), (faces[3][0], faces[3][1]), (faces[2][0], faces[2][1])], (212,175,55,20))
    return draw

def tst():
    break_point = 10
    for j in range(0,40):
        im = Image.new("RGB", (2048, 2048), (1,1,1))
        draw = ImageDraw.Draw(im)
        theta = j/100.0 * np.pi*2
        phi = j/100.0 * np.pi*2
        alp = j/100.0 * np.pi*2
        beta = (j/100.0 - break_point/100.0) * np.pi*2
        gamma = (j/100.0 - break_point/100.0) * np.pi*2
        delta = (j/100.0 - break_point/100.0) * np.pi*2
        [r1,r2,r3,r4,r5,r6] = rotation_matrix(theta,phi,alp,beta,gamma,delta)
        if j < break_point:
            r = np.dot(r3,np.dot(r1,r2))
        else:
            r = np.dot(r6,np.dot(r5,np.dot(r4,np.dot(r3,np.dot(r1,r2)))))
        draw = render_scene_4d(draw, r)
        im.save('Images\\RotatingCube\\im' + str(j) + '.png')

'''
@MoneyShot
Generates larger and larger cubes showing their cutting planes representing polynomial terms.
args:
    numTerms: The number of values each dimension can take.
    pos: The position on the image where the leftmost edge of the cube should be.
'''
def General3DCube(numTerms, im_ind = 0, pos = [300,700,0], draw1 = None, scale1 = 100):
    global scale
    scale = scale1
    for j in range(30,31):
        if draw1 is None:
            im = Image.new("RGB", (2048, 2048), "black")
            draw = ImageDraw.Draw(im, 'RGBA')
        else:
            draw = draw1
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
        if draw1 is None:
            im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1


# Convert to video and gif.
#ffmpeg -framerate 10 -f image2 -i im%d.png -vb 20M vid.avi
#ffmpeg -i vid.avi -pix_fmt rgb24 -loop 0 out.gif



