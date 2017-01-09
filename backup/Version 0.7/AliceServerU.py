import socket
import pickle
from QuantumClasses import Alice
import threading
import time
import select
from Encrypt import Encrypt,Decrypt

 
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


def UpdateKey(blocks,client,stop_receiving,stop_updating,start_updating,start_clock):
    global key

    def uk():
        global key
        try:
            start_updating.wait()
            client.send("R3c1V3!")
            stop_receiving.wait(3)
            rLock.acquire()
            print "Updating"
            AliceM = Alice(blocks)
            AliceMbits= pickle.dumps(AliceM)
            client.send(AliceMbits)
            print 'Sent Bases '
            ready = select.select([client],[],[],3)
            if ready[0]:
                consbits = client.recv(47*(1+blocks)/2)
                cons = pickle.loads(consbits)
                print 'Received Coincidences '
                newkey = AliceM.Key(cons)
                if newkey == []:
                    newkey = [0]
                key = int("0b"+"".join(str(i) for i in newkey),2)
                client.send("Done") 
                done= client.recv(1024)
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
    client.close()



def UpdateKeyClock(delay, stop_updating,start_updating,start_clock):
    while not shutdown:
        start_clock.wait()
        print "clock started: "
        time.sleep(delay)
        print "clock finished:"
        stop_updating.clear()
        start_updating.set()
        start_clock.clear()



def ReceiveMessage(client,stop_receiving,stop_updating):
    global key
    while not shutdown:
        stop_updating.wait()
        stringBob = client.recv(5000)
        if stringBob == "R3c1V3!": 
            stop_receiving.set()

        else:
            Bobmessage = Decrypt(stringBob,key)
            rLock.acquire()
            print Bobmessage
            rLock.release()
    client.close()

if True:
    blocks=int(raw_input('give me blocks: '))
    delay = 20
    keybackup = Calibrate(blocks)
    key = keybackup
    host='192.168.0.18'
    port=5000
    s = socket.socket()
    s.bind((host,port))
    s.listen(1)
    quitting = False
    c, addr = s.accept()
    stop_receiving = threading.Event()
    stop_updating=threading.Event()
    start_updating = threading.Event()
    start_clock = threading.Event()
    uTC= threading.Thread(target=UpdateKeyClock, args=(delay,stop_updating,start_updating,start_clock))
    uTC.start()
    uT = threading.Thread(target=UpdateKey, args=(blocks,c,stop_receiving,stop_updating,start_updating,start_clock))
    uT.start()
    rT = threading.Thread(target= ReceiveMessage, args=(c,stop_receiving,stop_updating))
    rT.start()
    print "Accepted connection from:" + str(addr)
    message = ''
    stop_updating.set()
    start_clock.set()
    while not quitting: 
        if message != '': 
            stringAlice = "Alice: " + message
            stringAliceEn = Encrypt(stringAlice,key)
            c.send(stringAliceEn)
        message = raw_input("Alice" + "-> ")
        if message == "quit":
            quitting= True   

        stop_updating.wait()
  
        time.sleep(0.2)  

    shutdown = True
    c.close()
    s.close()
    uTC.join()
    uT.join()
    rT.join()





