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
