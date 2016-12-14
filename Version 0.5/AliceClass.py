from Matrix import Matrix
import random
from XorEncrypt import *
from math import sqrt

ket0=Matrix.fromList([[1.0],[0.0]])
ket1=Matrix.fromList([[0.0],[1.0]])
ketsum=Matrix.fromList([[round(1/sqrt(2),1)],[round(1/sqrt(2),1)]])
ketmin=Matrix.fromList([[round(1/sqrt(2),1)],[round(-1/sqrt(2),1)]])

class AliceError(Exception):
    """ An exception class for Alice """
    pass

class Alice(Matrix):

    def __init__(self,blocks,null=0,med=1):
        self.blocks=blocks
        self.realid=id(self)
        self.null=null
        self.med = med
        Alices=[]
        if null==0:
            for i in range(0,blocks):
                c = random.SystemRandom().choice([1,2,3,4])
                if c==1:
                    Alices.append(ket0)
                if c==2:
                    Alices.append(ket1)
                if c==3:
                    Alices.append(ketsum)
                if c==4:
                    Alices.append(ketmin)
            self.bases=Alices
        else:
            for i in range(0,blocks):
                Alices.append(0)
            self.bases=Alices

    def __getitem__(self,idx):
        if self.realid ==id(self) and self.med==1: 
            return self.bases[idx]
        else:
            raise AliceError, "Collapsed State"

    def __str__(self):
        a=[]
        for base in self.bases:
            a.append(str(base))
        stren = XorEncrypt(str(a),self.realid)
        strde = XorDecrypt(stren,id(self))
        return strde
	
    def __repr__(self):
        string=str(self)
        i=2
        d=[]
        for base in range(0,self.blocks):
            a=float(string[i:i+4])
            i+=6
            b=float(string[i:i+4])
            i+=10
            c=[a,b] #remove c for a simpler code
            if c == [1.0,0.0]:
                d.append(' ket0 ')
            elif c == [0.0,1.0]:
                d.append(' ket1 ')
            elif c == [round(1/sqrt(2),1), round(1/sqrt(2),1)]:
                d.append(' ketsum ')
            elif c == [round(1/sqrt(2),1), round(-1/sqrt(2),1)]:
                d.append(' ketmin ')
            else:
                d.append(' error ')

        return str(d)
 	
    def PrintBases(self):
        print repr(self)

    def Measure(self,Bob):
        if self.med>0:
            Result=Alice(self.blocks,1)
            self.med -= 1
            for i in range(self.blocks):
                Result.bases[i]= Bob.bases[i]*self.bases[i]
            return Result
        else:
            raise AliceError, "Collapsed State"
	
    def Coincidences(self):
        con=[]
        if self.realid == id(self) and self.med==1:
            for i in range(self.blocks):
                mc=self.bases[i]
                test = round(sqrt((mc[0][0])**2+(mc[1][0])**2),1)
                if test == 0.7:
                    con.append(0)
                else:
                    con.append(1)
            return con

        else:
            raise AliceError, "Collapsed State"


    def KeyAlice(self,con):
        llave=[]
        if self.realid == id(self) and self.med==1:
            for i in range(len(con)):
                if con[i] == 1:
            	    if str(self.bases[i]) == '+0.0\n+1.0\n':
                        llave.append(1)

                    elif str(self.bases[i]) == '+1.0\n+0.0\n':
                        llave.append(0)

                    elif str(self.bases[i]) == '+0.7\n-0.7\n':
                        llave.append(1)

                    elif str(self.bases[i]) == '+0.7\n+0.7\n':
                        llave.append(0)

        else:
            raise AliceError, "Collapsed State" 	
        return llave		

		
def Main():
    Alices = Alice(10)

    print Alices

    Alices.PrintBases()
if __name__=='__main__':
    Main()
