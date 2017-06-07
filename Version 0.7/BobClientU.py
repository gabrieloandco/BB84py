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

def UpdateKey(blocks,socket,stop_receiving,stop_updating,start_updating,start_clock):
    global key
    def uk():
        global key
        try:
            start_updating.wait()
            stop_receiving.wait(3)
            socket.send("R3c1V3!")
            rLock.acquire()
            print "Updating"
            ready = select.select([socket],[],[],3)
            if ready[0]:
                AliceMbits = socket.recv(324*(1+blocks)/2)
                print "Received Alice's bases"
                AliceM=  pickle.loads(AliceMbits)
                BobM = Bob(blocks)
                ResultM= AliceM.Measure(BobM)
                cons = BobM.Coincidences(ResultM)
                consbits = pickle.dumps(cons)
                socket.send(consbits)
                print "Sent Coincidences"
                newkey = BobM.Key(ResultM,cons)
                if newkey == []:
                    newkey = [0]
                key= int("0b"+"".join(str(i) for i in newkey),2)
                done = socket.recv(1024)
                socket.send("Done")
                print done
                print "Key Updated; new key: " + bin(key)
                stop_receiving.clear()
                stop_updating.set()
                start_clock.set() 
                start_updating.clear() 
                rLock.release()
                return key
           
        except:
            print "Update Failed"
            stop_receiving.clear()
            stop_updating.set()   
            start_clock.set()   
            start_updating.clear()          
            return 1

    while not shutdown:
        uk()
    socket.close()



def UpdateKeyClock(delay, stop_updating,start_updating,start_clock):
    while not shutdown:
        start_clock.wait()
        print "clock started: "
        time.sleep(delay)
        print "clock finished:"
        stop_updating.clear()
        start_updating.set()
        start_clock.clear()


def ReceiveMessage(socket,stop_receiving,stop_updating):
    global key
    while not shutdown: 
        stop_updating.wait()
        stringAlice = socket.recv(5000)
        if stringAlice == "R3c1V3!":  
            stop_receiving.set()
 
        else:
            Alicemessage = Decrypt(stringAlice,key)
            rLock.acquire()
            print Alicemessage
            rLock.release()
    socket.close()

if True:
    blocks=int(raw_input('give me blocks: '))
    delay = 20
    keybackup = Calibrate(blocks)
    key = keybackup
    host='192.168.0.18'
    port = 5000
    s = socket.socket()
    quitting = False
    s.connect((host,port))
    stop_receiving = threading.Event()
    stop_updating=threading.Event()
    start_updating = threading.Event()
    start_clock = threading.Event()
    uTC= threading.Thread(target=UpdateKeyClock, args=(delay,stop_updating,start_updating,start_clock))
    uTC.start()
    uT = threading.Thread(target=UpdateKey, args=(blocks,s,stop_receiving,stop_updating,start_updating,start_clock))
    uT.start()
    rT = threading.Thread(target= ReceiveMessage, args=(s,stop_receiving,stop_updating))
    rT.start()
    stop_updating.set()
    start_clock.set()

    print "Connection Started with: " + host + ":" + str(port)
    message = ''
    while not quitting:     
        if message != '': 
            stringBob = "Bob: " + message
            stringBobEn = Encrypt(stringBob,key)
            s.send(stringBobEn)
        message = raw_input("Bob" + "-> ")
        if message == "quit":
            quitting = True  

        stop_updating.wait()

        time.sleep(0.2)  

    shutdown = True
    s.close()
    uTC.join()
    uT.join()
    rT.join()

