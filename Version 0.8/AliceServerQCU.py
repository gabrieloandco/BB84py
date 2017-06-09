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

def AliceQCU():
 
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
                print "Updating"
                AliceM = Alice(blocks)
                AliceMbits= pickle.dumps(AliceM)
                qclient.send(AliceMbits)
                print 'Sent Bases '
                ready = select.select([qclient],[],[],3)
                if ready[0]:
                    consbits = qclient.recv(47*(1+blocks)/2)
                    cons = pickle.loads(consbits)
                    print 'Received Coincidences '
                    newkey = AliceM.Key(cons)
                    if newkey == []:
                        newkey = [0]
                    key = int("0b"+"".join(str(i) for i in newkey),2)
                    qclient.send("Done") 
                    done= qclient.recv(1024)
                    print done           
                    print "Key Updated; new key: " + bin(key)
                    rLock.release()
                    return key

            else: #except:
                print "Update Failed"         
                return 1
                

        while not shutdown:
            uk()
            time.sleep(delay)

        qclient.close()
        qsocket.close()



    def ReceiveMessage(client):
        global key
        while not shutdown:
            stringBob = client.recv(5000)
            Bobmessage = Decrypt(stringBob,key)
            rLock.acquire()
            print Bobmessage
            rLock.release()
        client.close()


    blocks= int(raw_input('give me blocks: '))
    delay = 10
    keybackup = Calibrate(blocks)
    key = keybackup
    host='192.168.0.18'
    port=5000
    s = socket.socket()
    s.bind((host,port))
    s.listen(1)
    quitting = False
    QC = threading.Thread(target=QuantumChannel, args=(blocks,delay))
    QC.start()
    c, addr = s.accept()
    rT = threading.Thread(target= ReceiveMessage, args=(c,))
    rT.start()
    print "Accepted connection from:" + str(addr)
    message = ''
    while not quitting: 
        if message != '': 
            stringAlice = "Alice: " + message
            stringAliceEn = Encrypt(stringAlice,key)
            c.send(stringAliceEn)
        message = raw_input("Alice" + "-> ")
        if message == "quit":
            quitting= True   
  
        time.sleep(0.2)  

    shutdown = True
    c.close()
    s.close()
    QC.join()
    rT.join()



