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

def AliceGen(limit):
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
    return Alice

def LlaveAlice(Alice,con):
    llave=[]
    for i in range(len(Alice)):
        if con[i] == 1:
            if str(Alice[i]) == '+0.0\n+1.0\n':
                llave.append(1)

            elif str(Alice[i]) == '+1.0\n+0.0\n':
                llave.append(0)

            elif str(Alice[i]) == '+0.7\n-0.7\n':
                llave.append(1)

            elif str(Alice[i]) == '+0.7\n+0.7\n':
                llave.append(0)
                
    return llave

def PrintAlice(Alice):
    i=1
    for base in Alice:
        print "#"+ str(i) + ":" + str(base)
        i +=1
    
    
    
