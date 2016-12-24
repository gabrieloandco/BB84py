import socket
import pickle
import BobClass
import threading
import time
import select
from ForLoopEncrypt import *
from XorEncrypt import * 

uLock = threading.RLock(True)
rLock = threading.Lock()
sLock = threading.Lock()
shutdown = False
ku = False

def Calibrate(blocks):
    host='192.168.0.20'
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

def UpdateKey(blocks,socket,stop_receiving,stop_updating):
    global ku
    global key
    def uk():
        global ku
        global key
        if ku: 
            try:
                stop_receiving.wait(3)
                socket.send("R3c1V3!")
                rLock.acquire()
                print "Updating"
                ready = select.select([socket],[],[],3)
                if ready[0]:
                    AliceMbits = socket.recv(324*(1+blocks)/2)
                    print "Received Alice's bases"
                    AliceM=  pickle.loads(AliceMbits)
                    BobM = BobClass.Bob(blocks)
                    ResultM= AliceM.Measure(BobM)
                    cons = ResultM.Coincidences()
                    consbits = pickle.dumps(cons)
                    socket.send(consbits)
                    print "Sent Coincidences"
                    newkey = BobM.KeyBob(ResultM,cons)
                    key= int("0b"+"".join(str(i) for i in newkey),2)
                    done = socket.recv(1024)
                    socket.send("Done")
                    print done
                    print "Key Updated; new key: " + bin(key)
                    ku = False
                    rLock.release()
                    stop_receiving.clear()
                    stop_updating.set()
                    return key, ku
           
            except:
                print "Update Failed"
                ku = False
                stop_receiving.clear()
                stop_updating.set()                
                return ku
            


        else:
            pass

    while not shutdown:
        uk()
    socket.close()


def UpdateKeyClock(delay, stop_updating):
    global ku

    def ukc():
        global ku
        if not ku:
            print "clock started: ku ="+ str(ku) 
            time.sleep(delay)
            ku = not ku
            print "clock finished: ku ="+ str(ku)
            stop_updating.clear()
            return ku
        if ku:
             pass

    while not shutdown:
        ukc()

def ReceiveMessage(socket,stop_receiving,stop_updating):
    global ku
    global key
    while not shutdown: 
        stop_updating.wait()
        stringAlice = socket.recv(5000)
        if stringAlice == "R3c1V3!":  
            stop_receiving.set()
 
        else:
            Alicemessage = ForLoopDecrypt(stringAlice,key)
            rLock.acquire()
            print Alicemessage
            rLock.release()
    socket.close()


    
blocks=int(raw_input('give me blocks: '))
delay = 10
keybackup = Calibrate(blocks)
key = keybackup
host='192.168.0.20'
port = 5000
s = socket.socket()
quitting = False
s.connect((host,port))
stop_receiving = threading.Event()
stop_updating = threading.Event()
stop_updating.set()
uTC= threading.Thread(target=UpdateKeyClock, args=(delay,stop_updating))
uTC.start()
uT = threading.Thread(target=UpdateKey, args=(blocks,s,stop_receiving,stop_updating))
uT.start()
rT = threading.Thread(target= ReceiveMessage, args=(s,stop_receiving,stop_updating))
rT.start()

print "Connection Started with: " + str(host)
message = ''
while not quitting:     
    if message != '': 
        stringBob = "Bob: " + message
        stringBobEn = ForLoopEncrypt(stringBob,key)
        s.send(stringBobEn)
    message = raw_input("Bob" + "-> ")
    if message == "quit":
        quitting = True  
    try:
        stop_updating.wait(5)
    except:
        print "Clock failed"
        ku = False
        stop_receiving.clear()
        stop_updating.set()   
    time.sleep(0.2)  

shutdown = True
s.close()
uTC.join()
uT.join()
rT.join()

    
