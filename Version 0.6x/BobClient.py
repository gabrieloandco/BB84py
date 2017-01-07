import socket
import pickle
import BobClass
import threading
import time
import select
from ForLoopEncrypt import *
from XorEncrypt import * 

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
    BobM = BobClass.Bob(blocks)
    ResultM= AliceM.Measure(BobM)
    cons = ResultM.Coincidences()
    consbits = pickle.dumps(cons)
    s.send(consbits)
    s.close()
    print "Sent Coincidences"
    keybob = BobM.KeyBob(ResultM,cons)
    key= int("0b"+"".join(str(i) for i in keybob),2)
    print bin(key)
    print "Calibration Over"
    time.sleep(1)
    return key

def QuantumChannel(blocks,delay):
    time.sleep(2)
    host='192.168.0.18'
    qport=6001
    qsocket = socket.socket()
    qsocket.connect((host,qport))
    print "Quantum Connection Stablished with: " + host + ":" + str(qport)
    global key

    def uk():
        global key
        if True: #try:
            rLock.acquire()
            print "Updating"
            ready = select.select([qsocket],[],[],3)
            if ready[0]:
                AliceMbits = qsocket.recv(324*(1+blocks)/2)
                print "Received Alice's bases"
                AliceM=  pickle.loads(AliceMbits)
                BobM = BobClass.Bob(blocks)
                ResultM= AliceM.Measure(BobM)
                cons = ResultM.Coincidences()
                consbits = pickle.dumps(cons)
                qsocket.send(consbits)
                print "Sent Coincidences"
                newkey = BobM.KeyBob(ResultM,cons)
                key= int("0b"+"".join(str(i) for i in newkey),2)
                done = qsocket.recv(1024)
                qsocket.send("Done")
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
    qsocket.close()


def ReceiveMessage(socket):
    global key
    while not shutdown: 
        stringAlice = socket.recv(5000)
        Alicemessage = ForLoopDecrypt(stringAlice,key)
        rLock.acquire()
        print Alicemessage
        rLock.release()

    socket.close()


    
blocks=int(raw_input('give me blocks: '))
delay = 2
keybackup = Calibrate(blocks)
key = keybackup
host='192.168.0.18'
port = 5001
s = socket.socket()
quitting = False
s.connect((host,port))
QC= threading.Thread(target=QuantumChannel, args=(blocks,delay))
QC.start()
rT = threading.Thread(target= ReceiveMessage, args=(s,))
rT.start()

print "Connection Started with: " + host + ":" + str(port)
message = ''
while not quitting:     
    if message != '': 
        stringBob = "Bob: " + message
        stringBobEn = ForLoopEncrypt(stringBob,key)
        s.send(stringBobEn)
    message = raw_input("Bob" + "-> ")
    if message == "quit":
        quitting = True  

    time.sleep(0.2)  

shutdown = True
s.close()
QC.join()
rT.join()

    
