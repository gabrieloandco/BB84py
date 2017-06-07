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
import threading
import time
import select
import Queue 
from ForLoopEncrypt import *
from XorEncrypt import * 

rLock = threading.Lock()
breaking = False
key = 0

def EvaTunnel(blocks,connecttoeva, connecttoalice,start_updating,stop_updating,stop_receivingeva,stop_receivingbob,breakevent):
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
    RFET =  threading.Thread(target=ReceiveFrom, args = (blocks,ceva,receivedfromeva,start_updating,stop_receivingeva,stop_updating,qdataeva,"Eva",breakevent))
    RFBT =  threading.Thread(target=ReceiveFrom, args = (blocks,cbob,receivedfrombob,start_updating,stop_receivingbob,stop_updating,qdatabob,"Bob",breakevent))
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

def ReceiveFrom(blocks,socket,receivedfrom,start_updating,stop_receivingfrom,stop_updating,qdatafrom,person,breakevent,block=False):
    breaking = False
    while not breaking:
        datafrom = socket.recv(324*(1+blocks)/2)
        qdatafrom.put(datafrom)
        print "Received from: " + person + datafrom
        receivedfrom.set()

        if not datafrom:
            breaking = True
            breakevent.set()
        if datafrom == "R3c1V3!":
            stop_receivingfrom.set()
            stop_updating.clear()
            start_updating.set()

        if not stop_receivingfrom.is_set():        
            print DecryptMessage(datafrom,start_updating)

        if block:
            stop_updating.wait()

    
def DecryptMessage(data,start_updating):
    global key
    if not start_updating.is_set():
        try:
            print "key: " + str(key)
            print "message: " + ForLoopDecrypt(data,key)[0:20]
        except:
            print "Couldn't Decrypt"
    else:
        pass
    
    

def UpdateKey(blocks,socketalice,socketeva,stop_receivingbob,stop_receivingeva,stop_receivingfromtunnel,stop_receivingfromalice,stop_updating,start_updating,start_clock,breakingevent):
    global key
    breaking = False
    def uk():
        global key
        try:
            start_updating.wait()
            stop_receivingfromalice.wait()
            stop_receivingbob.wait()
            stop_receivingeva.wait()
            stop_receivingfromtunnel.wait()
            stop_updating.clear()
            rLock.acquire()
            print "Updating"
            ready = select.select([socketalice],[],[],3)
            if ready[0]:
                AliceMbits = socketalice.recv(324*(1+blocks)/2)
                print "Received Alice's bases"
                print "bases: " + AliceMbits
                AliceM=  pickle.loads(AliceMbits)
                BobM = BobClass.Bob(blocks)
                ResultM= AliceM.Measure(BobM)
                ResultMbits = pickle.dumps(ResultM)
                socketeva.send(ResultMbits)
                print "Sent State to Tunnel"
                consbits = socketeva.recv(47*(1+blocks)/2)
                print "Received Coincidences from Eva"
                socketalice.send(consbits)
                print "Sent Coincidences To Alice"
                cons = pickle.loads(consbits)
                newkey = BobM.KeyBob(ResultM,cons)
                key= int("0b"+"".join(str(i) for i in newkey),2)
                done = socketalice.recv(1024)
                socketeva.send(done)
                done = socketeva.recv(1024)
                socketalice.send(done)
                print done
                print "Key Updated; new key: " + bin(key)
                stop_receivingeva.clear()
                stop_receivingbob.clear()
                stop_updating.set()
                start_clock.set() 
                start_updating.clear() 
                rLock.release()
                return key
           
        except:
            print "Update Failed"
            stop_receivingbob.clear()
            stop_receivingeva.clear()
            stop_updating.set()   
            start_clock.set()   
            start_updating.clear()          
            return 1

    while not breaking:
        uk()
        if breakingevent.is_set():
            breaking = True
    socket.close()



if True:
    blocks=int(raw_input('give me blocks: '))
    delay = 10
    connecttoeva = threading.Event()
    connecttoalice = threading.Event()
    start_updating = threading.Event()
    stop_receivingeva = threading.Event()
    stop_receivingbob = threading.Event()
    stop_updating=threading.Event()
    start_clock = threading.Event()
    breakevent = threading.Event()
    Tunnel = threading.Thread(target=EvaTunnel, args=(blocks,connecttoeva, connecttoalice,start_updating,stop_updating,stop_receivingeva,stop_receivingbob,breakevent))
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
    stop_receivingfromtunnel = threading.Event()
    stop_receivingfromalice = threading.Event()
    qdatatunnel = Queue.Queue()
    qdataalice = Queue.Queue()
    RFTT =  threading.Thread(target=ReceiveFrom, args = (blocks,seva,receivedfromtunnel,start_updating,stop_receivingfromtunnel,stop_updating,qdatatunnel,"Tunnel",breakevent,True))
    RFAT =  threading.Thread(target=ReceiveFrom, args = (blocks,salice,receivedfromalice,start_updating,stop_receivingfromalice,stop_updating,qdataalice,"Alice",breakevent, True))
    RFTT.start()
    RFAT.start()

    uT = threading.Thread(target=UpdateKey, args=(blocks,salice,seva,stop_receivingbob,stop_receivingeva,stop_receivingfromtunnel,stop_receivingfromalice,stop_updating,start_updating,start_clock,breakevent))
    uT.start()
    stop_updating.set()
    start_clock.set()

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
    uT.join()
    RFTT.join()
    RFAT.join()   
    salice.close()
    seva.close()
    


