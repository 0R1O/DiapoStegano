#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

imgPath = "Lenna.png"

img = Image.open(imgPath) # On ouvre l'image avec PIL
img.show() # On affiche l'image

imgnew = Image.eval(img,lambda x: x-x%2) # on fait une modification avec LSB = 0
imgnew.show() # On affiche l'image
imgnew.save("LSB_0.png")

imgnew2 = Image.eval(img,lambda x: x-x%2+1) # idem avec LSB = 1
imgnew2.show() # On affiche l'image
imgnew2.save("LSB_1.png")

