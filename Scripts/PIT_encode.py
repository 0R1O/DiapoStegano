# -*- coding:utf-8 -*-

""" 
Ce Script permet de lire les messages cachés avec la technique 
"Pixel Indicator Technique"
"""

from PIL import Image
import binascii
import sys
import random

VERBOSE = True
PYTHON3 = sys.version_info > (3, 0)


def is_prime(n):
    """ Advanced Prime Number Fn """
    if n == 2 or n == 3: return True
    if n < 2 or n%2 == 0: return False
    if n < 9: return True
    if n%3 == 0: return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        if n%f == 0: return False
        if n%(f+2) == 0: return False
        f +=6
    return True

def get2lsb(n):
    """ Return 2 last LSB as String """
    n = n%4
    if(n == 0):
        return "00"
    if(n == 1):
        return "01"
    if(n == 2):
        return "10"
    if(n == 3):
        return "11"

def int2bytes(i):
    """ Convert int to bytes """
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def text_to_bits(str):
    """  string to bits """
    out = ""
    if PYTHON3:
        r = bytes(str, "utf-8")
        for x in r:
            out += "0"*(8-len("{0:b}".format(x)))+"{0:b}".format(x)
    else:
        for x in str:
            out += "0"*(8-len(format(ord(x), 'b')))+format(ord(x), 'b')
    return out

###############################################################################

img = Image.open("Lenna.png")

MSG = "Nouveau message à cacher !"

pxs = img.load() # 2D Array pxs[x,y] ; pxs[0,0] = top left
w,h = img.size

if(VERBOSE):
    print("Load Image with size: "+str(w)+"*"+str(h))

N = len(MSG)*8

Nstr = "{0:b}".format(N)
Nstr = "0"*(64-len(Nstr))+Nstr # Padding avec des 0



if(VERBOSE):
    print("Taille du message : "+str(N))

"""

Si N pair : indicateur = R
Si N premier : indicateur = B
Sinon : indicateur = V

"""

# IC = Indicator Channel, R = 0 , V = 1 , B = 2


if(N%2 == 0): # Pair --> IC = R
    IC = 0
    if(VERBOSE):
        print("'N' est pair ==> IC = R (0)")
elif(is_prime(N)): # Premier -->  IC = B
    IC = 2
    if(VERBOSE):
        print("'N' est premier ==> IC = B (2)")
else: # Sinon IC = V
    IC = 1 
    if(VERBOSE):
        print("'N' est ni pair ni premier ==> IC = V (1)")

"""
On calcul la "parité binaire":
nombre de bit à 1 pair ==> 0
nombre de bit à 1 impaire ==> 1
"""

parite = format(N,'b').count("1")%2 # Nb de bit % 2

if(VERBOSE):
    print("Parité binaire : "+("paire" if parite == 0 else "impaire"))

c = ["R","G","B"]

if(parite == 1): # Impair (Odd)
    if(IC == 0): # R
        c1 = 1
        c2 = 2
    elif(IC == 2): # B
        c1 = 0
        c2 = 1
    else: # G
        c1 = 0
        c2 = 2
else: # Pair (Even)
    if(IC == 0): # R
        c1 = 2 # B
        c2 = 1 # G
    elif(IC == 2): # B
        c1 = 1
        c2 = 0
    else: # G
        c1 = 2
        c2 = 0


if(VERBOSE):
    print("\n-----------------\n")
    print("Indicator Chanel: "+c[IC])
    print("Data Chanel 1: "+c[c1])
    print("Data Chanel 2: "+c[c2])


""" On commence la création de l'image """

pxsl = list(img.getdata()) # Copie de l'ancienne image

# On set la taille du message
pxsl[0] = (int(Nstr[:8],2),int(Nstr[8:16],2),int(Nstr[16:24],2))
pxsl[1] = (int(Nstr[24:32],2),int(Nstr[32:40],2),int(Nstr[40:48],2))
pxsl[2] = (int(Nstr[48:56],2),int(Nstr[56:],2),pxsl[2][2])


secretBin = text_to_bits(MSG)

secretBin += "0"*(4-(len(secretBin)%4))

RMS = len(secretBin)


i = 0 # pixel courrant
while(RMS > 0): # Tant qu'il nous reste des choses à lire
    c = pxsl[w+i] # On commence à la 2eme ligne (d'où le w)
    newpx = [0,0,0]
    randTamper = random.randint(0,3) # On génère un nouveau nombre d'IC random
    newpx[IC] = c[IC]-(c[IC]%4)+randTamper # On le fusione avec l'existant
    newpx[c2] = c[c2] # On fait une copie du reste dans une liste
    newpx[c1] = c[c1]
    
    # On check en fonction du random IV, où stocker le message
    
    if(randTamper == 1): # 01
        newpx[c2] = c[c2]-(c[c2]%4)+int(secretBin[:2],2)
        secretBin = secretBin[2:] # on retire 2 char au secret
        RMS -= 2
    elif(randTamper == 2): # 10
        newpx[c1] = c[c1]-(c[c1]%4)+int(secretBin[:2],2)
        secretBin = secretBin[2:] # on retire 2 char au secret
        RMS -= 2
    elif(randTamper == 3): # 11
        if len(secretBin) < 4:
            secretBin += "0"*(4-(len(secretBin)%4))
        newpx[c1] = c[c1]-(c[c1]%4)+int(secretBin[:2],2)
        secretBin = secretBin[2:] # on retire 2 char au secret
        newpx[c2] = c[c2]-(c[c2]%4)+int(secretBin[:2],2)
        secretBin = secretBin[2:] # on retire 2 char au secret
        RMS -= 4
        
    pxsl[w+i] = tuple(newpx)
    i += 1

# On enregistre
new = Image.new(img.mode,img.size)
new.putdata(pxsl)

new.show()
new.save("PixelIndicatorTechnique.png")
