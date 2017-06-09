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
from QuantumClasses import Bob
import threading
import time
import select
from Encrypt import Encrypt,Decrypt

rLock = threading.Lock()
shutdown = False

def Calibrate(blocks):
    host='192.168.0.18'
    port = 5000
    s = socket.socket()
    s.connect((host,port))
    print "Connection Started"
    AliceMbits = s.recv(324*(1+blocks)/2)
    print "Received Alice's bases"
    AliceM=  pickle.loads(AliceMbits)
    BobM = Bob(blocks)
    ResultM= AliceM.Measure(BobM)
    cons = BobM.Coincidences(ResultM)
    consbits = pickle.dumps(cons)
    s.send(consbits)
    s.close()
    print "Sent Coincidences"
    keybob = BobM.Key(ResultM,cons)
    if keybob == []:
        keybob = [0]
    key= int("0b"+"".join(str(i) for i in keybob),2)
    print bin(key)
    print "Calibration Over"
    time.sleep(1)
    return key

def QuantumChannel(blocks,delay):
    time.sleep(2)
    host='192.168.0.18'
    qport=6000
    qsocket = socket.socket()
    qsocket.connect((host,qport))
    print "Quantum Connection Stablished with: " + host + ":" + str(qport)
    global key

    def uk():
        global key
        if True: #try:
            rLock.acquire()
            print "Updating"
