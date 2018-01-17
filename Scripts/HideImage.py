#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

imgPath = "Lenna.png"
imgPathHide = "Hide.png"

img = Image.open(imgPath) # On ouvre l'image avec PIL
w,h = img.size
pxs = list(img.getdata())


imgHide = Image.open(imgPathHide) # On ouvre l'image avec PIL
wHide,hHide = imgHide.size
pxsHide = list(imgHide.getdata())

def toBin(i):
    r = "{0:b}".format(i)
    r = "0"*(8-len(r))+r # Padding with 0
    return r

def toInt(s):
    if s == '':
        return 0
    return int(s,2)


if(w == wHide and h == hHide):
    for i in range(1,9):
        newdata = []
        for y in range(h):
            for x in range(w):
                c = pxs[y*w+x] # Current pixel
                cHide = pxsHide[y*w+x] # Current pixel
                
                # print(toBin(c[0])[:-i])
                # print(toBin(cHide[0])[:i])
                
                r = toInt(toBin(c[0])[:-i]+toBin(cHide[0])[:i])
                g = toInt(toBin(c[1])[:-i]+toBin(cHide[1])[:i])
                b = toInt(toBin(c[2])[:-i]+toBin(cHide[2])[:i])
                
                newdata.append((r,g,b))
                x += 3

        new = Image.new(img.mode,img.size)
        new.putdata(newdata)

        new.show()
        new.save("HideImage"+str(i)+".png")
