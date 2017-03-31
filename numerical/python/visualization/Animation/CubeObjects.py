import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath

class Vertice():
    def __init__(self, i = 0, n = 4):
        self.dim = n
        self.index = i
        self.binary = self.to_binary()

    def plot(self,r,draw,rgba,width=3):
        vv = np.dot(r,self.binary)
        [vx,vy] = (shift + scale * vv)[0:2] # Projection on x-y plane
        draw.ellipse( (vx-width,vy-width,vx+width,vy+width), fill = rgba, outline = rgba)

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

    def plot(self, r, draw, rgba, width = 3):
        [v1, v2] = [np.dot(r, self.vertice1.binary), np.dot(r, self.vertice2.binary)]
        [v1x,v1y] = (shift + scale * v1)[0:2]
        [v2x,v2y] = (shift + scale * v2)[0:2]
        draw.line((v1x, v1y, v2x, v2y), fill=rgba, width=width)

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
            [v1x,v1y] = (shift + scale * v1)[0:2]
            [v2x,v2y] = (shift + scale * v2)[0:2]
            draw.line((v1x, v1y, v2x, v2y), fill='orange', width=3)
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

#shift = np.array([170,400, 380]) # (for 1024, 1024)
#scale = 300
shift = np.array([1000,1000, 0, 0])
scale = 500

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


def cube_body_diagonal(width = 15):
    c1 = Cube(3)
    for j in range(80):
        r = rotation(3,np.pi*2*j/80.0)
        [im, draw] = c1.plot_edges(r)
        c1.vertices[0].plot(r, draw, "red", width)
        c1.vertices[7].plot(r, draw, "red", width)
        rotated_vertices = np.transpose(np.dot(r,np.transpose(c1.vertice_matrix)))*scale + shift
        draw.polygon([(rotated_vertices[1][0], rotated_vertices[1][1]), (rotated_vertices[2][0], rotated_vertices[2][1]), (rotated_vertices[4][0], rotated_vertices[4][1])], (120,80,200,100))
        c1.vertices[1].plot(r, draw, (120,80,200), width)
        c1.vertices[2].plot(r, draw, (120,80,200), width)
        c1.vertices[4].plot(r, draw, (120,80,200), width)
        draw.polygon([(rotated_vertices[3][0], rotated_vertices[3][1]), (rotated_vertices[5][0], rotated_vertices[5][1]), (rotated_vertices[6][0], rotated_vertices[6][1])], (200, 80, 100, 100))
        c1.vertices[3].plot(r, draw, (200, 80, 100), width)
        c1.vertices[5].plot(r, draw, (200, 80, 100), width)
        c1.vertices[6].plot(r, draw, (200, 80, 100), width)        
        draw.line((rotated_vertices[0][0], rotated_vertices[0][1], rotated_vertices[7][0], rotated_vertices[7][1]), fill="yellow", width=5)
        first_intersection = np.dot(r,np.array([.3333,.3333,.3333]))*scale + shift
        draw.ellipse( (first_intersection[0]-width,first_intersection[1]-width,first_intersection[0]+width,first_intersection[1]+width), fill = (120,80,200), outline = (120,80,200))
        first_intersection = np.dot(r,np.array([.6666,.6666,.6666]))*scale + shift
        draw.ellipse( (first_intersection[0]-width,first_intersection[1]-width,first_intersection[0]+width,first_intersection[1]+width), fill = (200,80,100), outline = (120,80,200))
        im.save('Images\\RotatingCube\\im' + str(j) + '.png')


def teserract_body_diagonal(width = 15, j = 70):
    c1 = Cube(4)
    for j in range(80):
        r = rotation(4,np.pi*2*j/80.0)
        [im, draw] = c1.plot_edges(r)
        #c1.vertices[0].plot(r, draw, (255,0,0,90), width)
        #c1.vertices[15].plot(r, draw, (255,0,0,90), width)
        rotated_vertices = np.transpose(np.dot(r,np.transpose(c1.vertice_matrix)))*scale + shift
        hexag = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums==2]]]
        rgba = (124,252,0,60)
        draw.polygon([(hexag[0][0], hexag[0][1]), (hexag[1][0], hexag[1][1]), (hexag[3][0], hexag[3][1]), (hexag[5][0], hexag[5][1]), (hexag[4][0], hexag[4][1]), (hexag[2][0], hexag[2][1])], rgba)
        draw.polygon([(hexag[0][0], hexag[0][1]), (hexag[4][0], hexag[4][1]), (hexag[3][0], hexag[3][1]), (hexag[5][0], hexag[5][1]), (hexag[1][0], hexag[1][1]), (hexag[2][0], hexag[2][1])], rgba)
        #c1.vertices[3].plot(r, draw, "red", width)#1
        #c1.vertices[5].plot(r, draw, "green", width)#2
        #c1.vertices[9].plot(r, draw, "blue", width)#3
        #c1.vertices[12].plot(r, draw, "yellow", width)#4
        #c1.vertices[10].plot(r, draw, "orange", width)#5
        #c1.vertices[6].plot(r, draw, "purple", width)#6
        sqr1 = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums==3]]]
        sqr2 = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums==1]]]
        #draw.polygon([(sqr1[0][0], sqr1[0][1]), (sqr1[1][0], sqr1[1][1]), (sqr1[2][0], sqr1[2][1]), (sqr1[3][0], sqr1[3][1])], (255,0,0,60))
        #draw.polygon([(sqr2[0][0], sqr2[0][1]), (sqr2[1][0], sqr2[1][1]), (sqr2[2][0], sqr2[2][1]), (sqr2[3][0], sqr2[3][1])], (0,0,255,60))
        #c1.vertices[7].plot(r, draw, "red", width)#
        #c1.vertices[11].plot(r, draw, "blue", width)#
        #c1.vertices[13].plot(r, draw, "green", width)#
        #c1.vertices[14].plot(r, draw, "yellow", width)#
        #draw.polygon([(rotated_vertices[3][0], rotated_vertices[3][1]), (rotated_vertices[5][0], rotated_vertices[5][1]), (rotated_vertices[6][0], rotated_vertices[6][1])], (200, 80, 100, 100))
        #draw.line((rotated_vertices[0][0], rotated_vertices[0][1], rotated_vertices[7][0], rotated_vertices[7][1]), fill="yellow", width=5)
        im.save('Images\\RotatingCube\\im' + str(j) + '.png')

def render_intro():
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im,'RGBA')
    font = ImageFont.truetype("arial.ttf", 30)
    width = 9
    [vx,vy] = np.array([0,0])*scale + shift[:2]
    draw.ellipse( (vx-width,vy-width,vx+width,vy+width), fill = "red", outline = "red")
    im.save('Images\\RotatingCube\\im' + str(0) + '.png')
    draw.line((0,1000,2048,1000), fill="silver", width=1)
    im.save('Images\\RotatingCube\\im' + str(1) + '.png')
    draw.text((vx, vy+20),"0",(255,255,255),font=font)
    im.save('Images\\RotatingCube\\im' + str(2) + '.png')

    for i in np.arange(0,1,0.1):
        [vx,vy] = np.array([i,0])*scale + shift[:2]
        draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = (255,0,0,80), outline = (255,0,0,80))
        if i > 0.1:
            vx = vx - 0.1*scale
            draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = "black", outline = "black")
        im.save('Images\\RotatingCube\\im' + str(i*10+3) + '.png')

    vx = 0.9*scale + shift[:1]
    draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = "black", outline = "black")
    [vx,vy] = np.array([1,0])*scale + shift[:2]
    draw.line((0,1000,2048,1000), fill="silver", width=1)
    draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = "red", outline = "red")
    im.save('Images\\RotatingCube\\im' + str(13) + '.png')
    draw.text((vx, vy+20),"1",(255,255,255),font=font)
    im.save('Images\\RotatingCube\\im' + str(14) + '.png')
    draw.line((1000,0,1000,2048), fill="silver", width=1)
    im.save('Images\\RotatingCube\\im' + str(15) + '.png')
    draw.text((1018, 1020),",0",(255,255,255),font=font)
    draw.text((scale + 1018, 1020),",0",(255,255,255),font=font)
    im.save('Images\\RotatingCube\\im' + str(16) + '.png')

    for i in np.arange(0,1,0.1):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im,'RGBA')
        draw = render_scene(draw)
        draw.line((1000, 1000 - i * scale, 1000 + scale, 1000 - i * scale), fill="silver", width=1)
        [vx, vy] = [1000, 1000 - i * scale]
        draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = (255,0,0,80), outline = (255,0,0,80))
        [vx, vy] = [1000 + scale, 1000 - i * scale]
        draw.ellipse((vx-width,vy-width,vx+width,vy+width), fill = (255,0,0,80), outline = (255,0,0,80))
        im.save('Images\\RotatingCube\\im' + str(17 + int(i*10)) + '.png')

    for j in range(0,10):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im,'RGBA')
        r = rotation(3, -j*np.pi/50.0)
        draw = render_scene(draw,r,9,True)
        im.save('Images\\RotatingCube\\im' + str(27 + int(j)) + '.png')

    for k in np.arange(0,1,0.1):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im,'RGBA')
        r = rotation(3, -j*np.pi/50.0)
        draw = render_scene(draw,r,9,True)
        draw = translate_square(k, draw)
        im.save('Images\\RotatingCube\\im' + str(37 + int(k*10)) + '.png')
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im,'RGBA')
    draw = translate_square(k, draw, 1)
    im.save('Images\\RotatingCube\\im' + str(47) + '.png')

def render_scene(draw, r = np.eye(3), width = 9, renderCube = False, drawCubeConnectors = -1):
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
    draw.ellipse((v1-width,v2-width,v1+width,v2+width), fill = (255,0,0,80), outline = (255,0,0))
    [u1,u2,u3] = new_vector(r, c1.vertice_matrix[1] * scale + shift[:3])
    draw.ellipse((u1-width,u2-width,u1+width,u2+width), fill = (255,0,0,80), outline = (255,0,0))
    if renderCube:
        [l1,l2,l3] = new_vector(r, -c1.vertice_matrix[2] * scale + shift[:3])
        draw.ellipse((l1-width,l2-width,l1+width,l2+width), fill = (255,0,0,80), outline = (255,0,0, 80))
        [m1,m2,m3] = new_vector(r, np.array([1,-1,0]) * scale + shift[:3])
        draw.ellipse((m1-width,m2-width,m1+width,m2+width), fill = (255,0,0,80), outline = (255,0,0, 80))
        draw.polygon([(v1, v2), (u1, u2), (m1, m2), (l1, l2)], (192,192,192,80))
    return draw

def new_vector(r, v):
    v = v - np.array([1000, 1000, 0]) #1000,1000 should go to 0,0. 
    v = v / scale
    v = np.dot(r,v)
    v = v * scale
    v = v + np.array([1000, 1000, 0])
    return v

def translate_square(z, draw, drawCubeConnectors = -1):
    rgba = (255,0,0,80)
    [v1,v2,v3] = new_vector(r, (c1.vertice_matrix[0] + np.array([0,0,z]))* scale + shift[:3])
    draw.ellipse((v1-width,v2-width,v1+width,v2+width), fill = "red", outline = (255,0,0))
    [u1,u2,u3] = new_vector(r, (c1.vertice_matrix[1] + np.array([0,0,z])) * scale + shift[:3])
    draw.ellipse((u1-width,u2-width,u1+width,u2+width), fill = "green", outline = (255,0,0))
    [l1,l2,l3] = new_vector(r, (-c1.vertice_matrix[2] + np.array([0,0,z])) * scale + shift[:3])
    draw.ellipse((l1-width,l2-width,l1+width,l2+width), fill = "blue", outline = (255,0,0, 80))
    [m1,m2,m3] = new_vector(r, (np.array([1,-1,0]) + np.array([0,0,z])) * scale + shift[:3])
    draw.ellipse((m1-width,m2-width,m1+width,m2+width), fill = "orange", outline = (255,0,0, 80))
    draw.polygon([(v1, v2), (u1, u2), (m1, m2), (l1, l2)], (192,192,192,80))
    if drawCubeConnectors > -1:
        draw.line((v1,v2,u1,u2), fill = "orange", width = 1)
    return draw


# Convert to video and gif.
#ffmpeg -framerate 10 -f image2 -i im%d.png vid.avi
#ffmpeg -i vid.avi -pix_fmt rgb24 -loop 0 out.gif



