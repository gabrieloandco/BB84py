import socket
import pickle
import AliceClass
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
    port=5000
    s = socket.socket()
    s.bind((host,port))
    s.listen(1)
    print "Server started"
    c, addr = s.accept()
    print "Bob address is:" + str(addr)
    AliceM = AliceClass.Alice(blocks)
    AliceMbits= pickle.dumps(AliceM)
    c.send(AliceMbits)
    print 'Sent Bases '
    consbits = c.recv(47*(1+blocks)/2)
    print 'Received Coincidences '
    cons = pickle.loads(consbits)
    keyalice = AliceM.KeyAlice(cons)
    key = int("0b"+"".join(str(i) for i in keyalice),2)
    print bin(key)
    print "Calibration Over"
    c.close()
    s.close()	
    return key


def UpdateKey(blocks,client,stop_receiving,stop_updating):
    global ku
    global key
    def uk():
        global ku
        global key

        if ku:
            try:
                client.send("R3c1V3!")
                stop_receiving.wait(3)
                rLock.acquire()
                print "Updating"
                AliceM = AliceClass.Alice(blocks)
                AliceMbits= pickle.dumps(AliceM)
                client.send(AliceMbits)
                print 'Sent Bases '
                ready = select.select([client],[],[],3)
                if ready[0]:
                    consbits = client.recv(47*(1+blocks)/2)
                    cons = pickle.loads(consbits)
                    print 'Received Coincidences '
                    newkey = AliceM.KeyAlice(cons)
                    key = int("0b"+"".join(str(i) for i in newkey),2)
                    client.send("Done") 
                    done= client.recv(1024)
                    print done           
                    print "Key Updated; new key: " + bin(key)
                    ku = False
                    stop_receiving.clear()
                    stop_updating.set()
                    rLock.release()
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
    client.close()



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



def ReceiveMessage(client,stop_receiving,stop_updating):
    global ku
    global key
    while not shutdown:
        stop_updating.wait()
        stringBob = client.recv(5000)
        if stringBob == "R3c1V3!": 
            stop_receiving.set()

        else:
            Bobmessage = ForLoopDecrypt(stringBob,key)
            rLock.acquire()
            print Bobmessage
            rLock.release()
    client.close()


blocks=int(raw_input('give me blocks: '))
delay = 10
keybackup = Calibrate(blocks)
key = keybackup
host='192.168.0.20'
port=5000
s = socket.socket()
s.settimeout(5)
s.bind((host,port))
s.listen(1)
quitting = False
c, addr = s.accept()
stop_receiving = threading.Event()
stop_updating=threading.Event()
stop_updating.set()
uTC= threading.Thread(target=UpdateKeyClock, args=(delay,stop_updating))
uTC.start()
uT = threading.Thread(target=UpdateKey, args=(blocks,c,stop_receiving,stop_updating))
uT.start()
rT = threading.Thread(target= ReceiveMessage, args=(c,stop_receiving,stop_updating))
rT.start()
print "Accepted connection from:" + str(addr)
message = ''
while not quitting: 
    if message != '': 
        stringAlice = "Alice: " + message
        stringAliceEn = ForLoopEncrypt(stringAlice,key)
        c.send(stringAliceEn)
    message = raw_input("Alice" + "-> ")
    if message == "quit":
        quitting= True   
    try:
        stop_updating.wait(5)
    except:
        print "Clock failed"
        ku = False
        stop_receiving.clear()
        stop_updating.set()    
    time.sleep(0.2)  

shutdown = True
c.close()
s.close()
uTC.join()
uT.join()
rT.join()
#XorEncrypt(ForLoopEncrypt(message,int(key,2)),int(key,2))
#ForLoopDecrypt(XorDecrypt(stringBob,int(key,2)),int(key,2))


