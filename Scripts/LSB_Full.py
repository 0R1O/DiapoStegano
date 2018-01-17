#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import random
import string
from Crypto.Cipher import AES

imgPath = "Lenna.png"

img = Image.open(imgPath) # On ouvre l'image avec PIL
w,h = img.size
pxs = list(img.getdata())


################################################################################
# On crééer l'image en codant "Lorem Ipsum" en boucle (motif)
################################################################################

lorem = "0100110001101111011100100110010101101101001000000100100101\
110000011100110111010101101101" # "Lorem Ipsum" en binaire

newdata = []

l = len(lorem)
x = 0
for i in range(h):
    for j in range(w):
        c = pxs[i*w+j] # Current
        r = c[0] - c[0]%2 + int(lorem[(x)%l]) # On force LSB à 0 puis on ajoute
        g = c[1] - c[1]%2 + int(lorem[(x+1)%l]) # le bon LSB en fonction de
        b = c[2] - c[2]%2 + int(lorem[(x+2)%l]) # string (lettre courrante)
        newdata.append((r,g,b))
        x += 3

new = Image.new(img.mode,img.size)
new.putdata(newdata)

new.show()
new.save("LSB_LoremIpsum.png")


################################################################################
# On crééer l'image en codant de l'ASCII aussi grand que l'image
################################################################################

# Texte aléatoire de taille w*h (largement sufisant)

text = "".join([random.choice(string.printable) for i in range(w*h)]) 
binary = ''.join('{:08b}'.format(ord(c)) for c in text)
newdata = []

x = 0
for i in range(h):
    for j in range(w):
        c = pxs[i*w+j] # Current
        r = c[0] - c[0]%2 + int(binary[x]) # On force MSB à 0 puis on ajoute
        g = c[1] - c[1]%2 + int(binary[x+1]) # le bon MSB en fonction de
        b = c[2] - c[2]%2 + int(binary[x+2]) # binary (lettre courrante)
        newdata.append((r,g,b))
        x += 3

new = Image.new(img.mode,img.size)
new.putdata(newdata)

new.show()
new.save("LSB_BigText.png")

################################################################################
# Idem mais sur la couche 1 uniquement
################################################################################

# Texte aléatoire de taille w*h (largement sufisant)

text = "".join([random.choice(string.printable) for i in range(w*h)]) 
binary = ''.join('{:08b}'.format(ord(c)) for c in text)
newdata = []

x = 0
for i in range(h):
    for j in range(w):
        c = pxs[i*w+j] # Current
        r = c[0] - c[0]%2 + int(binary[x])
        g = c[1]
        b = c[2]
        newdata.append((r,g,b))
        x += 1

new = Image.new(img.mode,img.size)
new.putdata(newdata)

new.show()
new.save("LSB_BigText_RedOnly.png")

################################################################################
# Idem mais sur la couche 2 uniquement
################################################################################

# Texte aléatoire de taille w*h (largement sufisant)

text = "".join([random.choice(string.printable) for i in range(w*h)]) 
binary = ''.join('{:08b}'.format(ord(c)) for c in text)
newdata = []

x = 0
for i in range(h):
    for j in range(w):
        c = pxs[i*w+j] # Current
        r = c[0]
        g = c[1] - c[1]%2 + int(binary[x])
        b = c[2]
        newdata.append((r,g,b))
        x += 1

new = Image.new(img.mode,img.size)
new.putdata(newdata)

new.show()
new.save("LSB_BigText_GreenOnly.png")

################################################################################
# Idem mais sur la couche 3 uniquement
################################################################################

# Texte aléatoire de taille w*h (largement sufisant)

text = "".join([random.choice(string.printable) for i in range(w*h)]) 
binary = ''.join('{:08b}'.format(ord(c)) for c in text)
newdata = []

x = 0
for i in range(h):
    for j in range(w):
        c = pxs[i*w+j] # Current
        r = c[0]
        g = c[1]
        b = c[2] - c[2]%2 + int(binary[x])
        newdata.append((r,g,b))
        x += 1

new = Image.new(img.mode,img.size)
new.putdata(newdata)

new.show()
new.save("LSB_BigText_BlueOnly.png")

################################################################################
# On crééer l'image en codant un message déjà chiffré
################################################################################

# Texte aléatoire de taille w*h (largement sufisant)

text = "".join([random.choice(string.printable) for i in range(w*h)]) 


aes = AES.new("LSBISFUNNY012345", AES.MODE_CFB, 
'\xDE\xAD\xBE\xEF\xDE\xAD\xBE\xEF') # AES , mode CFB pour un padding + simple
cypher = aes.encrypt(text)

binary = ''.join('{:08b}'.format(c) for c in cypher)
newdata = []

x = 0
for i in range(h):
    for j in range(w):
        c = pxs[i*w+j] # Current
        r = c[0] - c[0]%2 + int(binary[x]) # On force MSB à 0 puis on ajoute
        g = c[1] - c[1]%2 + int(binary[x+1]) # le bon MSB en fonction de
        b = c[2] - c[2]%2 + int(binary[x+2]) # binary (lettre courrante)
        newdata.append((r,g,b))
        x += 3

new = Image.new(img.mode,img.size)
new.putdata(newdata)

new.show()
new.save("LSB_Cypher.png")