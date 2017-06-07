# Copyright (c) 2016 Gabriel Oliveri (<gabrieloandco@gmail.com>)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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

def BobGen(limit):
    Bob=[]
    for i in range(0,limit):
        d= random.SystemRandom().choice([1,2]) ##random.randrange(1,3)
        if d == 1:
            Bob.append(P1)
        if d == 2:
            Bob.append(Pmin)
    return Bob

def Medicion(Bob,Alice):
    Resultado=[]
    for i in range(len(Alice)):
        Resultado.append(Bob[i]*Alice[i])
    return Resultado

def Con(Resultado):
    con=[]
    for i in range(len(Resultado)):
        mc = Resultado[i]
        test = round(sqrt((mc[0][0])**2+(mc[1][0])**2),1)
        if test == 0.7:
            con.append(0)
        else:
            con.append(1)
    return con

def LlaveBob(Alice,Bob,con):
    llave=[]
    for i in range(len(Alice)):
        if con[i] == 1:
            ml = Bob[i]*Alice[i]
            llave.append(int(round(sqrt((ml[0][0])**2+(ml[1][0])**2),1)))
    return llave

def PrintBob(Bob):
    i=1
    for base in Bob:
        print "#"+ str(i) + ":" + str(base)
        i +=1
    


    
