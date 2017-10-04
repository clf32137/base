from PIL import Image
from PIL import ImageDraw

back = Image.open('C:\\Users\\rohit\\Documents\\GitHub\\base\\numerical\\python\\visualization\\Animation\\Images\\Logo6.png')

poly = Image.new('RGBA', back.size)
pdraw = ImageDraw.Draw(poly)
pdraw.polygon([(21, 34), (331, 34), (172, 278)], fill = (51,153,255,180), outline = (51,153,255))
back.paste(poly,mask=poly)
back.save('Images\\RotatingCube\\im' + str(50) + '.png')


import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('C:\\Users\\rohit\\Documents\\GitHub\\base\\numerical\\python\\visualization\\Animation\\Images\\SamuraiBest\\Samurai.jpg',0)
edges = cv2.Canny(img,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()

