#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import random
import string
from Crypto.Cipher import AES

w,h = 300,300

################################################################################
# Creating random image 
################################################################################

randimg = Image.new('RGB', (w, h))

randomData = []
for i in range(h):
    for j in range(w):
        t = (
        random.randint(0,255), # r
        random.randint(0,255), # g
        random.randint(0,255)  # b
        ) # Random Tuple
        randomData.append(t)
randimg.putdata(randomData)


randimg.show()
randimg.save("Random.png")

################################################################################
# Creating Image with Ascii as layout value
################################################################################

ascii = Image.new('RGB', (w, h))

asciiData = []
cleartext = ""

for i in range(h):
    for j in range(w): # Ord = ascii value
        r = ord(random.choice(string.printable)) # Random printable letter
        g = ord(random.choice(string.printable))
        b = ord(random.choice(string.printable))
        asciiData.append((r,g,b)) # Ascii Tuple
        cleartext += chr(r)+chr(g)+chr(b) # On recup ce qui a été écrit pour
        # la partie AES
ascii.putdata(asciiData)

ascii.show()
ascii.save("Ascii.png")

################################################################################
# Creating Image with Ascii as layout value
################################################################################

cypherImg = Image.new('RGB', (w, h))

aes = AES.new("LSBISFUNNY012345", AES.MODE_CFB, 
'\xDE\xAD\xBE\xEF\xDE\xAD\xBE\xEF') # AES , mode CFB pour un padding + simple
cypher = aes.encrypt(cleartext)
cypherdata = []
x = 0
for i in range(h):
    for j in range(w): # Ord = ascii value
        r = cypher[x] # Random printable letter
        g = cypher[x+1]
        b = cypher[x+2]
        cypherdata.append((r,g,b)) # Ascii Tuple
        x += 3
cypherImg.putdata(cypherdata)

cypherImg.show()
cypherImg.save("Cypher.png")