import socket
import pickle
import AliceClass

def Main():
    blocks=int(raw_input('give me blocks: '))
    host='192.168.0.14'
    port=5000
    s = socket.socket()
    s.bind((host,port))
    s.listen(1)
    quitting = False
    print "Server started"
    c, addr = s.accept()
    print "Bob address is:" + str(addr)
    if not quitting:

        AliceM = AliceClass.Alice(blocks)
        AliceMbits= pickle.dumps(AliceM)
        c.send(AliceMbits)
        print 'Sent Bases '
        consbits = c.recv(47*(1+blocks)/2)
        print 'Received Coincidences '	
        cons = pickle.loads(consbits)
        key = AliceM.KeyAlice(cons)
        print 'Alice Matrix'
        print AliceM
        print 'Coincidences'
        print cons
        print 'Key'
        print key


    c.close()
    s.close()

if __name__=='__main__':
    Main()

