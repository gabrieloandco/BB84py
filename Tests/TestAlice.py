import socket
import threading

def AcceptEva(salice,eva_accepted):
    global cbob
    ceva, evaaddr = salice.accept()
    print "Eva accepted"
    eva_accepted.set()
    cbob.close()
    cbob = ceva
    return cbob

salice = socket.socket()
host = '192.168.0.18'
port = 5000
salice.bind((host,port))
salice.listen(2)
cbob, bobaddr= salice.accept()
eva_accepted = threading.Event()
AE = threading.Thread(target=AcceptEva, args = (salice,eva_accepted))
AE.start()

while True:
    message = raw_input("->")
    cbob.send(message)
    received = cbob.recv(1024)
    print received
    


    

