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
ket0=Matrix.Matrix.fromList([[1],[0]])
bra0=Matrix.Matrix.fromList([[1,0]])
ket1=Matrix.Matrix.fromList([[0],[1]])
bra1=Matrix.Matrix.fromList([[0,1]])
P0=ket0*bra0
P1=ket1*bra1
ketsum=Matrix.Matrix.fromList([[1/sqrt(2)],[1/sqrt(2)]])
brasum=Matrix.Matrix.fromList([[1/sqrt(2),1/sqrt(2)]])
ketmin=Matrix.Matrix.fromList([[1/sqrt(2)],[-1/sqrt(2)]])
bramin=Matrix.Matrix.fromList([[1/sqrt(2),-1/sqrt(2)]])
Psum=Matrix.Matrix.fromList([[0.5,0.5],[0.5,0.5]]) ##ketsum*brasum
Pmin=Matrix.Matrix.fromList([[0.5,-0.5],[-0.5,0.5]]) ##ketmin*bramin

def EvaGen(limit):
    Eva=[]
    for i in range(0,limit):
        d= random.randrange(1,3)
        if d == 1:
            Eva.append(P1)
        if d == 2:
            Eva.append(Pmin)
    return Eva

def LlaveEva(limit):
    llaveeva=[]
    for i in range(0,limit):
        if con[i]==1:
            me = Eva[i]*Alice[i]
            llaveeva.append(int(sqrt((ml[0][0])**2+(ml[1][0])**2)))
    return llaveeva
    
