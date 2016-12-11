import socket
from BobGen import *
from QuantumConversion import *

def Main():
    hostAlice = raw_input("Alice IP: ")
    portAlice = 5000

    hostEva = raw_input("Eva IP: ")
    portEva=5000

    s = socket.socket()

    blocks = int(raw_input("Level of security: "))

    Eva = BobGen(blocks)

    print "Eva Bases"

    i=1
    for base in Bob:
        print "#"+ str(i) + ":" + str(base)
        i +=1

    while True:
        s.connect((hostAlice,portAlice))
        AliceStr= s.recv(5000)
        Alice = QuantumListToBasesAlice(QuantumStrToListAlice(AliceStr,blocks))
        Resultado = Medicion(Bob,Alice)
        strResultado = QuantumListToString(Resultado)
        s.close()
        
        s.connect((hostEva,portEva))
        s.send(strResultado)
        strcon = s.recv(5000)
        s.close()

        s.connect((hostAlice,portAlice))
        s.send(strcon)
        Alicestring=s.recv(5000)
        s.close()

        s.connect((hostEva,portEva))
        s.send(Alicestring)
        
        con = StringToBinaryList(strcon)
        llaveEva = QuantumKeyToBits(LlaveBob(Alice,Eva,con))
        Alicemessage = ForLoopDecrypt(XorDecrypt(Alicestring,int(llaveEva,2)))
        print Alicemessage
        
        
    s.close()
        
    
