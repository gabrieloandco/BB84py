import socket
from BobGen import *
from QuantumConversion import QuantumStrToListAlice,QuantumListToBasesAlice,QuantumKeyToBits
from XorEncrypt import *
from ForLoopEncrypt import *

def Main():

    host =raw_input("Host IP: ")

    port = 5000

    s = socket.socket()

    blocks = int(raw_input("Level of security: "))

    s.connect((host, port))

    Bob = BobGen(blocks)

    print "Bob Bases: "

    i=1
    for base in Bob:
        print "#"+ str(i) + ":" + str(base)
        i +=1

    AliceStr = s.recv(5000)

    AliceList= QuantumStrToListAlice(AliceStr,blocks)

    Alice = QuantumListToBasesAlice(AliceList)

    Resultado = Medicion(Bob,Alice)

    con = Con(Resultado)

    print "Coincidences: "

    print con

    s.send(str(con))

    llaveq = LlaveBob(Alice,Bob,con)

    print "Llave: "

    print llaveq

    llave = QuantumKeyToBits(llaveq)

    backupllave = llave ##Sera usado con Eva

    print  "Calibracion terminada, iniciando comunicacion"

    message=''
    while message != 'q':
        AliceStr = s.recv(5000)
        Alice = QuantumListToBasesAlice(QuantumStrToListAlice(AliceStr,blocks))
        Resultado = Medicion(Bob,Alice)
	con = Con(Resultado)
        s.send(str(con))
        llave = QuantumKeyToBits(LlaveBob(Alice,Bob,con))
        stringAlice = s.recv(5000)
        Alicemessage= ForLoopDecrypt(XorDecrypt(stringAlice,int(llave,2)),int(llave,2)*blocks)
        print "Alice: " + Alicemessage

        if llave != backupllave:
            print "Something is Wrong"
            choice = raw_input("End communication? (Y/N): ")
            if choice == Y or choice == y:
                s.close()

        message = raw_input('-->')
        stringBob= XorEncrypt(ForLoopEncrypt(message,int(llave,2)*blocks),int(llave,2))
        s.send(stringBob)
        print 'sending: '+ stringBob

    

    s.close()

if __name__ == '__main__':
    Main()
