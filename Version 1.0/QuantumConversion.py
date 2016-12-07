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

def QuantumListToStr(Matrix):
    a=[]
    for base in Matrix:
	a.append(str(base))
    return str(a)

def QuantumStrToListAlice(string,bases):
    ##can be improved with regular expressions
    i=2
    d=[]
    for base in range(0,bases):
        a=float(string[i:i+4])
        i+=6
        b=float(string[i:i+4])
        i+=10
        c=[a,b]
        d.append(c)
    return d
        

import re

def QuantumStrToListAlice1(string):
    pass


def QuantumListToBasesAlice(lists):
    Alice = []
    for l in lists:
        if l == [0.7, 0.7]:
            Alice.append(ketsum)
            
        elif l == [0.7, -0.7]:
            Alice.append(ketmin)

        elif l == [1.0, 0.0]:
            Alice.append(ket0)

        elif l == [0.0, 1.0]:
            Alice.append(ket1)
    return Alice

def QuantumKeyToBits(llave):
    return "0b"+"".join(str(i) for i in llave)

def StringToBinaryList(string):
    con=[]
    for letter in string:
	if letter == '1' or letter == '0':
		con.append(int(letter))
    return con
    

