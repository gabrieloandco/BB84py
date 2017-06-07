
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
from Encrypt import Decrypt
import Queue 

rLock = threading.Lock()
breaking = False

def EvaQTunnel(blocks,delay,breakevent):
    connecttoqeva = threading.Event()
    connecttoqalice = threading.Event()
    QChannel = threading.Thread(target=QuantumChannel, args=(blocks,delay,connecttoqeva,connecttoqalice,breakevent))
    QChannel.start()
    host = '192.168.0.18'
    port = 6001
    s = socket.socket()
    s.bind((host,port))
    connecttoqeva.set()
    s.listen(2)
    print "Tunneling Started."
    ceva, addreva = s.accept()
    print "Eva address is:" + str(addreva)
    cbob, addrbob = s.accept()
    connecttoqalice.set()
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
    
    QChannel.join()
    ceva.close()
    cbob.close
    s.close()

def QuantumChannel(blocks,delay,connecttoqeva,connecttoqalice,breakevent):
    time.sleep(2)
    tunnelqhost='192.168.0.18'
    tunnelqport=6001
    tunnelqsocket = socket.socket()
    connecttoqeva.wait()
    tunnelqsocket.connect((tunnelqhost,tunnelqport))
    aliceqhost = '192.168.0.18'
    aliceqport = 6000
    aliceqsocket = socket.socket()
    connecttoqalice.wait()
    aliceqsocket.connect((aliceqhost,aliceqport))
    breaking = False
    print "Quantum Connection Stablished with Alice: " + aliceqhost + ":" + str(aliceqport)
    print "Quantum Connection Stablished with Tunnel: " + tunnelqhost + ":" + str(tunnelqport)
    global key

    def uk():
        global key
        if True: #try:
            rLock.acquire()
            print "Updating"
            ready = select.select([aliceqsocket],[],[],3)
            if ready[0]:
                AliceMbits = aliceqsocket.recv(324*(1+blocks)/2)
                print "Received Alice's bases"
                AliceM=  pickle.loads(AliceMbits)
                EvaM = Bob(blocks)
                ResultM= AliceM.Measure(EvaM)
                ResultMbits = pickle.dumps(ResultM)
                tunnelqsocket.send(ResultMbits)
                print "Sent the Result of the Measure to Tunnel"
                consbits = tunnelqsocket.recv(47*(1+blocks)/2)
                print "Received coincidences of Bob from Tunnel"
                aliceqsocket.send(consbits)
                print "Sent to Alice Bob's Coincidences"
                cons = pickle.loads(consbits)
                newkey = EvaM.Key(ResultM,cons)
                if newkey == []:
                    newkey = [0]
                key= int("0b"+"".join(str(i) for i in newkey),2)
                done = aliceqsocket.recv(1024)
                tunnelqsocket.send(done)
                print done
                done = tunnelqsocket.recv(1024)
                aliceqsocket.send(done)
                print done
                print "Key Updated; new key: " + bin(key)
                rLock.release()
                return key
           
        else: #except:
            print "Update Failed"        
            return 1

    while not breaking:
        uk()
        time.sleep(delay)

    aliceqsocket.close()
    tunnelqsocket.close()


def EvaTunnel(blocks,connecttoeva, connecttoalice,breakevent):
    breaking = False
    host = '192.168.0.18'
    port = 5001
    s = socket.socket()
    s.bind((host,port))
    s.listen(2)
    print "Tunneling Started."
    connecttoeva.set()
    ceva, addreva = s.accept()
    print "Eva address is:" + str(addreva)
    cbob, addrbob = s.accept()
    connecttoalice.set()
    print "Bob address is:" + str(addrbob)
    receivedfromeva = threading.Event()
    receivedfrombob = threading.Event()
    qdatabob = Queue.Queue()
    qdataeva = Queue.Queue()
    RFET =  threading.Thread(target=ReceiveFrom, args = (blocks,ceva,receivedfromeva,qdataeva,"Eva",breakevent))
    RFBT =  threading.Thread(target=ReceiveFrom, args = (blocks,cbob,receivedfrombob,qdatabob,"Bob",breakevent))
    RFET.start()
    RFBT.start()
    while not breaking:

        if receivedfromeva.is_set():
            dataeva = qdataeva.get()
            cbob.send(dataeva)
            print "Sent to Bob" + dataeva
            receivedfromeva.clear()

        if receivedfrombob.is_set():
            databob = qdatabob.get()
            ceva.send(databob)
            print "Sent to Eva" + databob
            receivedfrombob.clear()  
        
        if breakevent.is_set():
            breaking = True  

    RFET.join()
    RFBT.join()
    ceva.close()
    cbob.close()
    s.close()

def ReceiveFrom(blocks,socket,receivedfrom,qdatafrom,person,breakevent):
    breaking = False
    while not breaking:
        datafrom = socket.recv(324*(1+blocks)/2)
        qdatafrom.put(datafrom)
        print "Received from: " + person + datafrom
        receivedfrom.set()

        if not datafrom:
            breaking = True
            breakevent.set()
     
        print DecryptMessage(datafrom,start_updating)


    
def DecryptMessage(data):
    global key
    
    try:
        print "key: " + str(key)
        print "message: " + Decrypt(data,key)[0:20]
    except:
        print "Couldn't Decrypt"
    else:
        pass


if True:
    blocks=int(raw_input('give me blocks: '))
    delay = 10
    connecttoeva = threading.Event()
    connecttoalice = threading.Event()
    breakevent = threading.Event()
    EvaQT = threading.Thread(target=EvaQTunnel, args=(blocks,delay,breakevent))
    EvaQT.start()
    Tunnel = threading.Thread(target=EvaTunnel, args=(blocks,connecttoeva, connecttoalice,breakevent))
    Tunnel.start()
    connecttoeva.wait()
    hostEva='192.168.0.18'
    portEva = 5001
    seva = socket.socket()
    seva.connect((hostEva,portEva))
    connecttoalice.wait()
    hostAlice='192.168.0.18'
    portAlice = 5000
    salice = socket.socket()
    salice.connect((hostAlice,portAlice))
    receivedfromtunnel = threading.Event()
    receivedfromalice = threading.Event()
    qdatatunnel = Queue.Queue()
    qdataalice = Queue.Queue()
    RFTT =  threading.Thread(target=ReceiveFrom, args = (blocks,seva,receivedfromtunnel,qdatatunnel,"Tunnel",breakevent))
    RFAT =  threading.Thread(target=ReceiveFrom, args = (blocks,salice,receivedfromalice,qdataalice,"Alice",breakevent))
    RFTT.start()
    RFAT.start()
    while not breaking:
        if receivedfromalice.is_set():
            datatunnel = qdatatunnel.get()
            seva.send(datatunnel)
            print "Sent to Tunnel"
            receivedfromalice.clear()

        if receivedfromtunnel.is_set():
            dataalice = qdataalice.get()
            salice.send(dataalice)
            print "Sent to Alice"
            receivedfromtunnel.clear()  
        
        if breakevent.is_set():
            breaking = True  

    Tunnel.join()
    EvaQT.join()
    RFTT.join()
    RFAT.join()   
    salice.close()
    seva.close()
