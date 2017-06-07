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
from Matrix import Matrix
import AliceClass 
from XorEncrypt import *
ket0=Matrix.fromList([[1.0],[0.0]])
bra0=Matrix.fromList([[1.0,0.0]])
ket1=Matrix.fromList([[0.0],[1.0]])
bra1=Matrix.fromList([[0.0,1.0]])
ketsum=Matrix.fromList([[round(1/sqrt(2),1)],[round(1/sqrt(2),1)]])
brasum=Matrix.fromList([[round(1/sqrt(2),1),round(1/sqrt(2),1)]])
ketmin=Matrix.fromList([[round(1/sqrt(2),1)],[round(-1/sqrt(2),1)]])
bramin=Matrix.fromList([[round(1/sqrt(2),1),round(-1/sqrt(2),1)]])
P0=ket0*bra0
P1=ket1*bra1
Psum= Matrix.fromList([[0.5,0.5],[0.5,0.5]]) ##ketsum*brasum ##
Pmin= Matrix.fromList([[0.5,-0.5],[-0.5,0.5]]) ##ketmin*bramin ##

class Bob(Matrix):

    def __init__(self,blocks):
        self.blocks = blocks
        Bobs=[]
        for i in range(blocks):
            d= random.SystemRandom().choice([1,2]) 
            if d == 1:
                Bobs.append(P1)
            elif d == 2:
                Bobs.append(Pmin)
        self.bases = Bobs


    def __str__(self):
        a=[]
        for base in self.bases:
            a.append(str(base))
        return str(a)

    def __repr__(self):
        string=str(self)
        i=2
        s=[]
        for base in range(0,self.blocks):
            a=float(string[i:i+4])
            i+=5
            b=float(string[i:i+4])
            i+=6
            c=float(string[i:i+4])
            i+=5
            d=float(string[i:i+4])
            i+=10
            e=[a,b,c,d] #remove c for a simpler code
            if e == [1.0,0.0,0.0,0.0]:
                s.append(' P0 ')
            elif e == [0.0,0.0,0.0,1.0]:
                s.append(' P1 ')
            elif e == [0.5,0.5,0.5,0.5]:
                s.append(' Psum ')
            elif e == [0.5,-0.5,-0.5,0.5]:
                s.append(' Pmin ')
            else:
                s.append(' error ')

        return str(s)

    def Coincidences(Resultado):
        con=[]
        for i in range(Resultado.bases):
            mc=Resultado.bases[i]
            test = round(sqrt((mc[0][0])**2+(mc[1][0])**2),1)
            if test == 0.7:
                con.append(0)
            else:
                con.append(1)
        return con


    def KeyBob(self,AliceTarget,con):
    	key=[]
    	for i in range(len(con)):
            if con[i] == 1:
                ml = self.bases[i]*AliceTarget.bases[i]
                key.append(int(round(sqrt((ml[0][0])**2+(ml[1][0])**2),1)))
        return key

    def PrintBob(self):
        i=1
        for base in self.bases:
            print "#"+ str(i) + ":" + str(base)
            i +=1
    


    
