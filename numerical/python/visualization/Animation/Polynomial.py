import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath

def polynomialFn(x, grad = np.matrix([0, 0]), 
    hess = np.matrix([
    [.2, 0],
    [0, 0.2]
]), jerk1 = np.matrix([
    [0.0, 0],
    [0, 0.0]
]), jerk2 = np.matrix([
    [0.0, 0],
    [0.0, 0.0]
])
):
    res = (grad * x.T)[0,0] + (x*hess*x.T)[0,0]
    jerkvec = np.matrix([(x*jerk1*x.T)[0,0], (x*jerk2*x.T)[0,0]])
    res = res + (jerkvec * x.T)[0,0]
    return res

def plotPolynomial(im_ind = 0, j = 0, scale = 300, shift = np.array([1000, 1000, 0])):
    r = rotation(3, 2*np.pi*j/30.0)
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    iih1 = 0.0
    iih2 = 0.0
    ii = im_ind
    ii1 = 0.0
    ii2 = 0.0
    if im_ind > 20:
        ii1 = im_ind - 20
        #iih2 = im_ind - 20
        #[iih1, ii, ii1, ii2] = np.zeros(4)
    if im_ind > 40:
        ii2 = im_ind - 40
        #ii = im_ind - 40
        #[iih1, iih2, ii1, ii2] = np.zeros(4)
    '''
    if im_ind > 60:
        ii1 = im_ind - 60
        #[iih1, iih2, ii, ii2] = np.zeros(4)
        iih1 = im_ind - 60
        iih2 = im_ind - 60
        ii = im_ind - 60
    if im_ind > 80:
        ii2 = im_ind - 80
        #[iih1, iih2, ii, ii1] = np.zeros(4)
        ii = im_ind - 80
        iih2 = im_ind - 80
        iih1 = im_ind - 80
        ii1 = im_ind - 80
    '''
    hess = np.matrix([
        [np.sin(iih1*np.pi/20.0), np.sin(iih2*np.pi/20.0)],
        [0.0, -np.sin(iih1*np.pi/20.0)]
    ])
    jerk1 = np.matrix([
        [np.sin(ii2*np.pi/20.0), np.sin(ii*np.pi/20.0)],
        [np.sin(ii*np.pi/20.0), np.sin(ii1*np.pi/20.0)]
    ])
    jerk2 = np.matrix([
        [np.sin(ii*np.pi/20.0), np.sin(ii1*np.pi/20.0)],
        [np.sin(ii1*np.pi/20.0), np.sin(ii2*np.pi/20.0)]
    ])
    r1 = np.eye(4)
    r1[:3,:3] = r
    render_scene_4d_axis(draw, r1, 4, scale = scale, shift = shift)
    drawXYGrid(draw, r, 1.25, scale = scale, shift = shift)
    for rad in np.concatenate((np.arange(0.0,0.1,0.05), np.arange(0.5,0.6,0.05),np.arange(1.0,1.1,0.05)),axis=0):
        x = np.matrix([rad*np.cos(0), rad*np.sin(0)])
        z = polynomialFn(x, hess = hess, jerk1 = jerk1, jerk2 = jerk2)
        pt1 = np.dot(r, np.array([x[0,0], x[0,1], z])) * scale + shift[:3]
        for theta in np.arange(np.pi/40.0, 2*np.pi, np.pi/40.0):
            x = np.matrix( [rad*np.cos(theta), rad*np.sin(theta)])
            z = polynomialFn(x, hess = hess, jerk1 = jerk1, jerk2 = jerk2)
            pt2 = np.dot(r, np.array([x[0,0], x[0,1], z])) * scale + shift[:3]
            if z >= 0:
                draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (255,20,147,120), width=5)
            else:
                draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (153,50,204,120), width=5)
            pt1 = pt2
    for rad in np.arange(0.01, 1.0, 0.01):
        x = np.matrix([rad*np.cos(0), rad*np.sin(0)])
        z = polynomialFn(x, hess = hess, jerk1 = jerk1, jerk2 = jerk2)
        pt1 = np.dot(r, np.array([x[0,0], x[0,1], z])) * scale + shift[:3]
        for theta in np.arange(np.pi/40.0, 2*np.pi, np.pi/40.0):
            x = np.matrix( [rad*np.cos(theta), rad*np.sin(theta)])
            z = polynomialFn(x, hess = hess, jerk1 = jerk1, jerk2 = jerk2)
            pt2 = np.dot(r, np.array([x[0,0], x[0,1], z])) * scale + shift[:3]
            if z >= 0:
                draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (255,20,147,70), width=3)
            else:
                draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (153,50,204,70), width=3)
            pt1 = pt2
    def fn(x):
        return polynomialFn(x, hess = hess, jerk1 = jerk1, jerk2 = jerk2)
    project_circle_on_surface(draw, r, fn)
    #writeQuadratic(draw, im_ind)
    #im = im.resize((512,512),Image.ANTIALIAS)
    im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png',optimize=True,quality=20)

def writeQuadratic(draw, im_ind):
    font = ImageFont.truetype("arial.ttf", 125)
    font1 = ImageFont.truetype("arial.ttf", 55)
    #fillcoeff = int(255*im_ind / 10.0)
    fillcoeff = 255
    draw.text((500,125), "z = ax + 2cxy - ay"  , font=font, fill = (fillcoeff,fillcoeff,fillcoeff))
    draw.text((850,125), "2", font=font1, fill = (fillcoeff,fillcoeff,fillcoeff))
    draw.text((1524,125), "2", font=font1, fill = (fillcoeff,fillcoeff,fillcoeff))
    #draw.text((500,125), "z = ax"  , font=font, fill = (fillcoeff,fillcoeff,fillcoeff))

def oneDimCubic(x, coeff = np.matrix([0.0,0.0,1e-3,0.0])):
    xvec = np.matrix([1, x, x*x, x*x*x])
    return (xvec*coeff.T)[0,0]

def plot_fn(fn, draw = None, im_ind = 0, coeff = np.matrix([0.0,0.0,5e-3,0.0])):
    font = ImageFont.truetype("arial.ttf", 125)
    font1 = ImageFont.truetype("arial.ttf", 55)
    font2 = ImageFont.truetype("arial.ttf", 125)
    if draw is None:
        im = Image.new("RGB", (2048, 2048), "black")
        draw1 = ImageDraw.Draw(im, 'RGBA')
    pt1 = np.array([-1000.0, fn(-1000.0, coeff)])
    axis(draw1)
    for x in np.arange(-999.7,1000,.3):
        pt2 = np.array([x, fn(x, coeff)])
        draw1.line((pt1[0]+1000, pt1[1]+1000, pt2[0]+1000, pt2[1]+1000), fill = "orange", width=3)
        pt1 = pt2
    #draw1.text((500,25), "%0.2f" %(coeff[0,0]) + ' + ' + "%0.2f" %(coeff[0,1]) + 'x + ' + "%0.2f" %(coeff[0,2]) + 'x'  , font=font)
    draw1.text((500,25), "a" + ' + ' + "b" + 'x + ' + "c" + 'x'  , font=font)
    draw1.text((1131,15), "2" , font=font1)
    #draw1.text((1465,15), "3" , font=font1)
    fillcoeff = int(255 * (10.0 - im_ind) / 10.0)
    draw1.text((512,800), "Quadratic forms" , font = font2, fill = (fillcoeff,fillcoeff,fillcoeff))
    if draw is None:
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')

def intro(im_ind = 0, draw = None):
    font = ImageFont.truetype("arial.ttf", 125)
    font1 = ImageFont.truetype("arial.ttf", 35)
    fillcoeff = int(255*im_ind / 10.0)
    if draw is None:
        im = Image.new("RGB", (2048, 2048), "black")
        draw1 = ImageDraw.Draw(im, 'RGBA')
        draw1.text((512,1024), "Quadratic forms" , font=font, fill = (fillcoeff,fillcoeff,fillcoeff))
        im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
    else:
        draw.text((512,1024), "Quadratic forms" , font=font, fill = (fillcoeff,fillcoeff,fillcoeff))


