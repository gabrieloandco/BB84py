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
    
