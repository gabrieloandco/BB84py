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
from AliceGen import AliceGen,LlaveAlice
from QuantumConversion import QuantumListToStr, QuantumKeyToBits, StringToBinaryList
from XorEncrypt import *
from ForLoopEncrypt import *


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

