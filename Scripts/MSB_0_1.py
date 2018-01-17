#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

imgPath = "Lenna.png"

img = Image.open(imgPath) # On ouvre l'image avec PIL
img.show() # On affiche l'image

imgnew = Image.eval(img,lambda x: x%128) # on fait une modification avec MSB = 0
imgnew.show() # On affiche l'image
imgnew.save("MSB_0.png")

imgnew2 = Image.eval(img,lambda x: x%128+128) # idem avec MSB = 1
imgnew2.show() # On affiche l'image
imgnew2.save("MSB_1.png")

