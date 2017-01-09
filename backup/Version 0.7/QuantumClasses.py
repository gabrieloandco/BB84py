from math import sqrt,fabs
import random
import quantumrandom
from Matrix import Matrix
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

def RandomGenerator(rang,option='Normal'):

    if option == "Normal":
        number = random.randint(0,rang-1)

    elif option == "System":
        number = random.SystemRandom().randint(0,rang-1)

    elif option == "Quantum":
        number = quantumrandom.randint(0,rang-1)

    else:
        raise Exception("Option not available")

    return number


class AliceError(Exception):
    """ An exception class for Alice """
    pass

class Alice(Matrix):

    def __init__(self,blocks,rand="Normal",null=0):
        self.blocks=blocks
        self.realid=id(self)
        self.null=null
        self.med = 1
        self.rand = rand
        Alices=[]
        if null==0:
            for i in range(0,blocks):
                c = RandomGenerator(4,rand)

                if c==0:
                    Alices.append(ket0)
                if c==1:
                    Alices.append(ket1)
                if c==2:
                    Alices.append(ketsum)
                if c==3:
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
        if self.realid ==id(self) and self.med==1: 
            a=[]
            for base in self.bases:
                a.append(str(base))
            return str(a)
        else:
            raise AliceError, "Collapsed State"
	
    def __repr__(self):
        if self.realid ==id(self) and self.med==1: 
            string=str(self)
            i=2
            d=[]
            for base in range(0,self.blocks):
                a=float(string[i:i+4])
                i+=6
                b=float(string[i:i+4])
                i+=10
                c=[a,b] 
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
        else:
            raise AliceError, "Collapsed State"
 	
    def PrintBases(self):
        print repr(self)

    def Measure(self,Bob):
        if self.med>0:
            Result=Alice(self.blocks,self.rand,1)
            self.med -= 1
            for i in range(self.blocks):
                Result.bases[i]= Bob.bases[i]*self.bases[i]
            return Result
        else:
            raise AliceError, "Collapsed State"


    def Key(self,con):
        llave=[]
        if self.realid == id(self):
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


class BobError(Exception):
    """ An exception class for Bob """
    pass

class Bob(Matrix):

    def __init__(self,blocks,rand="Normal"):
        self.blocks = blocks
        self.rand = rand
        Bobs=[]
        for i in range(blocks):
            d= RandomGenerator(2,rand)

            if d == 0:
                Bobs.append(P1)
            elif d == 1:
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
            e=[a,b,c,d] 
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

    def Coincidences(self,Result):
        con=[]
        if Result.realid == id(Result) and Result.med==1:
            for i in range(Result.blocks):
                mc=Result.bases[i]
                test = round(sqrt((mc[0][0])**2+(mc[1][0])**2),1)
                if test == 0.7:
                    con.append(0)
                else:
                    con.append(1)
            return con
        else:
                raise BobError, "Collapsed State"


    def Key(self,Result,con):
    	key=[]
        if Result.realid == id(Result): 
    	    for i in range(len(con)):
                if con[i] == 1:
                    ml = self.bases[i]*Result.bases[i]
                    key.append(int(round(sqrt((ml[0][0])**2+(ml[1][0])**2),1)))
            return key
        else:
                raise BobError, "Collapsed State"

    def PrintBases(self):
        print repr(self)

		
def Main():

    blocks = int(raw_input("Give me blocks: " ))

    randmode =  raw_input("Random Mode? 0:Normal , 1:System, 2:Quantum: " )
    if randmode == 1:
        rand='System'
    elif randmode == 2:
        rand = 'Quantum'
    else:
        rand = 'Normal'

    AliceM = Alice(blocks,rand)

    print "Alice Bases: "  
    AliceM.PrintBases()

    BobM = Bob(blocks,rand)

    print "Bob Bases: " 
    BobM.PrintBases()

    print "Protocol without intrusion: "

    ResultBM = AliceM.Measure(BobM)

    print "Coincidences: "

    con= BobM.Coincidences(ResultBM)

    print con

    keybob = BobM.Key(ResultBM,con)
    keyalice = AliceM.Key(con)

    print "Alice's Key: " + str(keyalice)
    print "Bob's Key: " + str(keybob)

    print "Protocol with intrusion: "

    AliceM = Alice(blocks,rand)

    print "Alice Bases: "  
    AliceM.PrintBases()

    BobM = Bob(blocks,rand)

    print "Bob Bases: " 
    BobM.PrintBases()

    EvaM = Bob(blocks,rand)

    print "Eva Bases: "
    EvaM.PrintBases()

    ResultEvM = AliceM.Measure(BobM)

    print "Result of Eva Measure: " 
    ResultEvM.PrintBases()

    ResultBM = ResultEvM.Measure(BobM)

    print "Coincidences: "

    con= BobM.Coincidences(ResultBM)

    print con 

    keybob = BobM.Key(ResultBM,con)
    keyalice = AliceM.Key(con)
    keyeva = BobM.Key(ResultEvM,con)

    print "Alice's Key: " + str(keyalice)
    print "Bob's Key: " + str(keybob)
    print "Eva's Key: " + str(keyeva)

    

    


if __name__=='__main__':
    Main()
