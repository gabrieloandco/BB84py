import socket
from AliceGen import AliceGen,LlaveAlice
from QuantumConversion import QuantumListToStr, QuantumKeyToBits, StringToBinaryList
from XorEncrypt import *
from ForLoopEncrypt import *
##agregar encryptacion por python y por generadores (blocks*llave)
##Eva sera servidor y cliente
##agregar cambio de bases en caso de intrusion
##agregar GUI
#agregar chat en tiempo real
#Fix non collapsing of Alice bases with subclasses and generators and fix alice matrix
#Fix Alice key
#Improve loops with generators and iterators
#System check?? with id at first
#sizeof in buffers bytes
#choose between random and quantum random and between pycrypto and generic crypto (#FINAL)

def Main():

    host = raw_input("Host IP: ")

    port = 5000

    s = socket.socket()

    blocks = int(raw_input("Level of security: "))

    s.bind((host,port))

    s.listen(1)

    c, addr = s.accept()

    print "Connection from: " + str(addr)
    
    Alice = AliceGen(blocks)

    print "Alice bases: " 

    i=1
    for base in Alice:
        print "#"+ str(i) + ":" + str(base)
        i +=1

    bases = QuantumListToStr(Alice)    
    
    c.send(bases)

    strcon = c.recv(5000)

    con = StringToBinaryList(strcon)

    print "Coincidences: "
    print con

    llaveq = LlaveAlice(Alice,con)

    print llaveq

    llave = QuantumKeyToBits(llaveq)

    backupllave = llave ##Sera usado con Eva

    print  "Calibracion terminada, iniciando comunicacion"

    message=''

    while message != 'q':
        c.send(bases)
        strcon = c.recv(5000)
        con = StringToBinaryList(strcon)
        llave = QuantumKeyToBits(LlaveAlice(Alice,con))
        message = raw_input('-->')
        stringAlice = XorEncrypt(ForLoopEncrypt(message,int(llave,2)))
        c.send(stringAlice)
        stringBob = c.recv(5000)
        Bobmessage = ForLoopDecrypt(XorDecrypt(stringBob,int(llave,2)))

        print "Bob: " + Bobmessage    

    c.close()



if __name__ == '__main__':

    Main()

