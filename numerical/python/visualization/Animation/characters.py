from Paraboloid import *
import matplotlib.pyplot as plt
import sympy

def bird_motion(im_ind=0):
    im_bird_0 = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\\BirdFlying\\brd0.png')
    im_bird_1 = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\\BirdFlying\\brd1.png')
    birds = [im_bird_0, im_bird_1]
    for i in range(10):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        bird = birds[i%2]
        pasteImage(bird,im,(i*50,1165))
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

def samurai_walk(im_ind=0):
    for i in range(7):
        im = Image.new("RGB", (2048, 2048), "black")
        if i < 35:
            im_sam = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\\SamuraiBest\\SamuraiWalking\\Turning\\im' +  str(i%7) + '.png')
        else:
            im_sam = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\\SamuraiBest\\SamuraiWalking\\im' +  str(7) + '.png')
        im_sam.thumbnail((750*0.6,1000*0.6), Image.ANTIALIAS)
        draw = ImageDraw.Draw(im, 'RGBA')
        pasteImage(im_sam,im,(35*30,1195))
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

'''
Pastes a flapping origami bird onto an image.
'''
def bird_flight(im_ind = 0, pt1 = np.array([1300.0,1300.0]), pt2 = np.array([1000.0,1000.0]), im = None):
    save_im = False
    if im is None:
        im = Image.new("RGB", (2048, 2048), "black")
        save_im = True
    [a,b,c] = two_pt_parabola(pt1, pt2)
    x = (pt1 + im_ind/20.0 * (pt2 - pt1))[0]
    y = (a*x**2 + b*x + c)
    im_bird = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\\BirdFlying\\origami\\im' +  str(im_ind % 3) + '.png')
    im_bird.thumbnail((150,150), Image.ANTIALIAS)
    slope = (parabola(a,b,c,x+1e-5) - parabola(a,b,c,x-1e-5))/1e-5/2
    angle = -np.arctan(slope)*180/np.pi
    im3 = im_bird.rotate(angle)
    pasteImage(im3, im, (x,y))
    if save_im:
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
        im_ind = im_ind + 1

'''
Given a rotation matrix and an image, draws a paraboloid made of origami birds on the image.
'''
def draw_bird_paraboloid(r, im):
    pts = get_parabola_points(r, 0)
    for pt in pts:
        try:
            bird_flight(im_ind = 19, pt1 = np.array([1169,1452]), pt2 = pt, im = im)
        except:
            pass

'''
Only works well for ind = 0. Origami birds fly up and create a parabola.
'''
def bird_storm(ind=0):
    j = 4
    r = rotation(3, 2 * np.pi*j/30.0)
    rot = general_rotation(np.dot(r,np.array([0,0,1])), np.pi*2*ind / 5.0)
    r1 = np.dot(rot,r)
    pts = get_parabola_points(r1, 0)
    im_ball = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\\Objects\\SoccerBall.png')
    im_ball.thumbnail((80.0,80.0), Image.ANTIALIAS)
    theta = np.random.rand() * np.pi * 2
    rot1 = general_rotation(np.dot(r,np.array([0,0,1])),theta)
    for im_ind in range(44 , 44 + 10):
        angle = 180 * (im_ind - 44) / 20.0
        #coeff = 0.3 * np.cos( (im_ind - 44)*2*np.pi/20.0 ) + 0.7 # Here, coeff remains positive. For x^2 and y^2.
        coeff = 0.6 * np.sin( (im_ind - 44)*2*np.pi/20.0 )
        font = ImageFont.truetype("arial.ttf", 100 + (im_ind - 44) % 4 * 10)
        im_sam = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\\SamuraiBest\\SamuraiWalking\\Shrugging\\im' +  str(0) + '.png')
        im_sam.thumbnail((750*0.6,1000*0.6), Image.ANTIALIAS)
        im_ball = im_ball.rotate(angle)
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        #draw.text((60, 60), "Paraboloid", font=font, fill = (120,80,200))
        #draw.text((1870, 1006), "x", font=font, fill = (0,255,64))
        #draw.text((1472, 1522), "y", font=font, fill = (0,255,64))
        #draw.text((1267, 60), "z", font=font, fill = (120,80,200))
        rollBallDownCurve(im, np.dot(rot1, r), 0, im_ball, p = (im_ind - 44.0)/20.0)
        for ii in range(ind):
            rot = general_rotation(np.dot(r,np.array([0,0,1])), 2*np.pi*ii/5.0)
            r2 = np.dot(rot,r)
            draw_bird_paraboloid(r2, im)
        if im_ind <= 20:
            for pt2 in pts:
                bird_flight(im_ind = im_ind, pt1 = np.array([1169,1452]), pt2 = pt2, im = im)
        else:
            #xzcurve(draw, r, 0)
            #paraboloidSection((im_ind - 21) * np.pi * 2 / 20.0, draw)
            #paraboloidSection(np.pi * 2, draw)
            #generalParaboloid(coeffs = [1.0,1.0, coeff], draw = draw, j = 0.5)
            #generalParaboloid(coeffs = [1.0, coeff, 0.0], draw = draw, j=0.5)
            #generalParaboloid(coeffs = [1.0,1.0,0.0], draw = draw, j = (im_ind - 44 + 1) * 0.6666666)
            generalParaboloid(coeffs = [1.0,1.0,0.0], draw = draw, j = 4)
        dotsize = 7 + 12 * np.sin((im_ind - 44) * np.pi / 4.0)
        #draw.ellipse((1000-dotsize,1000-dotsize,1000+dotsize,1000+dotsize),fill="yellow")
        pasteImage(im_sam,im,(35*30,1195))
        writeLatex(im, 'z = ', (115, 261), (120,80,200))
        writeLatex(im, 'x^2 + ' + 'y^2', (156 + 120, 261), (0,255,64))
        #draw.text((700, 700), "CONVEX", font=font, fill = (102,102,255))        
        im.save('Images\\RotatingCube\\im' + str(im_ind + (ind) * 20 - 44)  + '.png')


def pasteSamurai(im, posn = (35*30,1195), ind = 0):
    im_sam = Image.open('C:\Users\\rohit\Documents\GitHub\\base\\numerical\python\\visualization\Animation\Images\\SamuraiBest\\SamuraiWalking\\Drawing\\im' +  str(min(ind, 10)) + '.png')
    im_sam.thumbnail((750*0.6,1000*0.6), Image.ANTIALIAS)
    pasteImage(im_sam, im, posn)


'''
Gets some points on a rotated parabola.
'''
def get_parabola_points(r, y):
    minx = np.sqrt(3.5 - y*y)
    z = minx * minx + y * y
    curve_pts = []
    for x in np.arange(-minx, minx, 0.35):
        z = x*x + y*y
        pt2 = np.dot(r, [ y, x, z]) * scale + shift[:3]
        curve_pts.append(np.array([pt2[0],pt2[1]]))
    return np.array(curve_pts)

#(1460,1527)
#(1000,1000)

'''
Given two points, gives us the coefficients for a parabola.
'''
def two_pt_parabola(pt1,pt2):
    [x1, y1] = pt1 * 1.0
    [x2, y2] = pt2 * 1.0
    a = (y2-y1)/(x2-x1)**2
    c = y1 + a*x1*x1
    b = -2*a*x1
    return [a,b,c]

'''
Evaluates a parabola with coefficients a,b and c at point x.
'''
def parabola(a,b,c,x):
    return (a*x**2 + b*x + c)

'''
Given an image and pair of coordinates, writes out a Math equation at said coordinates.
Tools taken from - https://stackoverflow.com/questions/1381741/converting-latex-code-to-images-or-other-displayble-format-with-python
args:
    lat: The equation as a latex string. For example, '\\sin{\\left (\\sqrt{ \\frac{x^{2}}{y} + 20} \\right )} + 1'
'''
def writeLatex(im, lat, coordn = (50,50), color = (120,80,200), flip_im = False):
    lst = list(coordn)
    lst[0] = lst[0] - 139 + 50
    lst[1] = lst[1] - 475 + 50
    coordn = tuple(lst)
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    lst = np.array(list(color))
    lst = lst / 255.0
    color = tuple(lst)
    plt.text(0, 0, r"$%s$" % lat, fontsize = 70, color = color)
    #fig = plt.gca()
    #fig.axes.get_xaxis().set_visible(False)
    #fig.axes.get_yaxis().set_visible(False)
    plt.savefig(".\\Images\\Math\\temp.png")
    im_math = Image.open(".\\Images\\Math\\temp.png")
    #coordn = (coordn[0] - im_math.size[0]/2.0, coordn[1] - im_math.size[1]/2.0)
    pasteImage(im_math,im,coordn,True)
    plt.close()


def test(im_ind = 0):
    #j = max(0,(8.0 - im_ind)/2.0)
    j = 0.0
    r = rotation(3, 2 * np.pi*j/30.0)
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    font = ImageFont.truetype("arial.ttf", 100 + (im_ind) % 4 * 10)
    writeLatex(im, 'z = x^2 + y^2', (50,50))
    curveV2(draw,r,general_rotation(np.array([1.0,0,0]),np.pi/4), scale = 260, h = im_ind/10.0)
    generalParaboloid(coeffs = [1.0,1.0,0.0], draw = draw, j = j, scale = 260)
    im.save('Images\\RotatingCube\\im' + str(im_ind)  + '.png')


