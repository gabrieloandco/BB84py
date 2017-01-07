import socket
import pickle
import BobClass

def Main():
    blocks=int(raw_input('give me blocks: '))
    host='192.168.0.18'
    port = 5001
    s = socket.socket()
    s.connect((host,port))
    print "Connection Started"
    if True:
        AliceMbits = s.recv(324*(1+blocks)/2)
        print "Received Alice's bases"
        AliceM=  pickle.loads(AliceMbits)
        BobM = BobClass.Bob(blocks)
        ResultM= AliceM.Measure(BobM)
        cons = ResultM.Coincidences()
        consbits = pickle.dumps(cons)
        s.send(consbits)
        print "Sent Coincidences"
        key = BobM.KeyBob(ResultM,cons)
        print 'Bob Matrix'
        print BobM
        print 'Result Matrix'
        print ResultM
        print 'Coincidences'
        print cons
        print 'Key'
        print key
        print AliceM.bases


	s.close()

if __name__ == "__main__":
	Main()
