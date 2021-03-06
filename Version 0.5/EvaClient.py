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
import pickle
import BobClass
from threading import Thread
import time

def EvaServer(blocks):

    #Eva must connect First 
    host = '192.168.0.18'
    port = 5001
    s = socket.socket()
    s.bind((host,port))
    s.listen(2)
    print "Tunneling Started."
    ceva, addreva = s.accept()
    print "Eva address is:" + str(addreva)
    cbob, addrbob = s.accept()
    print "Bob address is:" + str(addrbob)
    breaking = False
    while not breaking:
        dataeva = ceva.recv(324*(1+blocks)/2)
        if not dataeva:
            breaking = True
        print "Received from Eva"
        cbob.send(dataeva)
        print "Sent to Bob"
        databob = cbob.recv(47*(1+blocks)/2)
        if not databob:
            breaking = True
        print "Received from Bob" 
        ceva.send(databob)
        print "Sent to Eva"
    
    ceva.close()
    cbob.close
    s.close()

def Main():
    blocks=int(raw_input('give me blocks: '))
    Tunnel = Thread(target=EvaServer, args=(blocks,))
    Tunnel.start()
    hostAlice='192.168.0.18'
    portAlice = 5000
    hostEva='192.168.0.18'
    portEva = 5001
    salice = socket.socket()
    seva = socket.socket()
    salice.connect((hostAlice,portAlice))
    time.sleep(2)
    seva.connect((hostEva,portEva))
    print "Hacking Started"
    if True:
        AliceMbits = salice.recv(324*(1+blocks)/2)
        print "Received Alice's bases"
        AliceM=  pickle.loads(AliceMbits)
        EvaM = BobClass.Bob(blocks)
        ResultM= AliceM.Measure(EvaM)
        ResultMbits = pickle.dumps(ResultM)
        seva.send(ResultMbits)
        print "Sent the Result of the Measure to Tunnel"
        consbits = seva.recv(47*(1+blocks)/2)
        print "Received coincidences of Bob from Tunnel"
        salice.send(consbits)
        print "Sent to Alice Bob's Coincidences"
        cons = pickle.loads(consbits)
        key = EvaM.KeyBob(ResultM,cons)
        print 'Eva Matrix'
        print EvaM
        print 'Result Matrix'
        print ResultM
        print 'Coincidences'
        print cons
        print 'Key'
        print key


    salice.close()
    seva.close()
    

if __name__ == "__main__":
	Main()
