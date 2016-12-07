from math import sqrt,fabs
import random
import Matrix
ket0=Matrix.Matrix.fromList([[1.0],[0.0]])
bra0=Matrix.Matrix.fromList([[1.0,0.0]])
ket1=Matrix.Matrix.fromList([[0.0],[1.0]])
bra1=Matrix.Matrix.fromList([[0.0,1.0]])
P0=ket0*bra0
P1=ket1*bra1
ketsum=Matrix.Matrix.fromList([[round(1/sqrt(2),1)],[round(1/sqrt(2),1)]])
brasum=Matrix.Matrix.fromList([[round(1/sqrt(2),1),round(1/sqrt(2),1)]])
ketmin=Matrix.Matrix.fromList([[round(1/sqrt(2),1)],[round(-1/sqrt(2),1)]])
bramin=Matrix.Matrix.fromList([[round(1/sqrt(2),1),round(-1/sqrt(2),1)]])
Psum= Matrix.Matrix.fromList([[0.5,0.5],[0.5,0.5]]) ##ketsum*brasum ##
Pmin= Matrix.Matrix.fromList([[0.5,-0.5],[-0.5,0.5]]) ##ketmin*bramin ##
from QuantumConversion import *

limit=int(raw_input("Security lvl: ")) ##Can be chosen by user
##Generador Alice
Alice=[]
for i in range(0,limit):
    c= random.SystemRandom().choice([1,2,3,4]) ##random.randrange(1,5)
    if c ==1:
        Alice.append(ket0)
    if c==2:
        Alice.append(ket1)
    if c==3:
        Alice.append(ketsum)
    if c==4:
        Alice.append(ketmin)
print "Bases de Alice"

i=1
for base in Alice:
    print "#"+ str(i) + ":" + str(base)
    i +=1

AStr= QuantumListToStr(Alice)

Alist = QuantumStrToListAlice(AStr,limit)

Alice=QuantumListToBasesAlice(Alist)


##Generador de Bob
Bob=[]
for i in range(0,limit):
    d= random.SystemRandom().choice([1,2]) ##random.randrange(1,3)
    if d == 1:
        Bob.append(P1)
    if d == 2:
        Bob.append(Pmin)

print "Bases de Bob"

i=1
for base in Bob:
    print "#"+ str(i) + ":" + str(base)
    i +=1

##Coincidencias
con=[]
for i in range(0,limit):
    mc = Bob[i]*Alice[i]
    test = round(sqrt((mc[0][0])**2+(mc[1][0])**2),1)
    if test == 0.7:
        con.append(0)
    else:
        con.append(1)

print "coincidencias"
print con

##llave
llave=[]
for i in range(0,limit):
    if con[i] == 1:
        ml = Bob[i]*Alice[i]
        llave.append(int(round(sqrt((ml[0][0])**2+(ml[1][0])**2),1)))

print "llave"
print llave

##Eva

##Generador de Eva
Eva=[]
for i in range(0,limit):
    d= random.SystemRandom().choice([1,2]) ##random.randrange(1,3)
    if d == 1:
        Eva.append(P1)
    if d == 2:
        Eva.append(Pmin)

print "Bases de Eva"
i=1
for base in Eva:
    print "#"+ str(i) + ":" + str(base)
    i +=1

##Llave de eva si conoce las coincidencias
llaveeva=[]
for i in range(0,limit):
    if con[i]==1:
        me = Eva[i]*Alice[i]
        llaveeva.append(int(round(sqrt((ml[0][0])**2+(ml[1][0])**2),1)))

print "Llave de eva"
print llaveeva
print "Son iguales?"
print llaveeva == llave

print "llave final:"       
llavebits = "0b"+"".join(str(i) for i in llave)
print llavebits

        
    
    
