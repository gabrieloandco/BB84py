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
        
    
