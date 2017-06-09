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
from QuantumClasses import Alice
import threading
import time
import select
from Encrypt import Encrypt,Decrypt

def AliceQC(): 
    rLock = threading.Lock()
    shutdown = False

    def Calibrate(blocks):
        host='192.168.0.18'
        port=5000
        s = socket.socket()
        s.bind((host,port))
        s.listen(1)
        print "Server started"
        c, addr = s.accept()
        print "Bob address is:" + str(addr)
        AliceM = Alice(blocks)
        AliceMbits= pickle.dumps(AliceM)
        c.send(AliceMbits)
        print 'Sent Bases '
        consbits = c.recv(47*(1+blocks)/2)
        print 'Received Coincidences '
        cons = pickle.loads(consbits)
        keyalice = AliceM.Key(cons)
        key = int("0b"+"".join(str(i) for i in keyalice),2)
        print bin(key)
        print "Calibration Over"
        c.close()
        s.close()	
        return key


    def QuantumChannel(blocks,delay):
        host='192.168.0.18'
        qport=6000
        qsocket = socket.socket()
        qsocket.bind((host,qport))
        qsocket.listen(1)
        qclient, addr = qsocket.accept()
        print "Quantum Connection Stablished with" + str(addr)
        global key
        def uk():
            global key
            if True: #try:
                rLock.acquire()
