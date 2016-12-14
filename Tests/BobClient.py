import socket
import pickle
import BobClass

def Main():
    host='192.168.0.14'
    port = 5000
    s = socket.socket()
    s.connect((host,port))

    while True:
        blocks=int(raw_input('give me blocks'))
        AliceMbits = s.recv(1024)
        AliceM=  pickle.loads(AliceMbits)
        BobM = BobClass.Bob(blocks)
        ResultM= BobM.Measure(AliceM)
        cons = ResultM.Coincidences()
        consbits = pickle.dumps(cons)
        s.send(consbits)
        key = BobM.KeyBob(AliceM,cons)
        print repr(BobM)
        print ResultM
        print key
        print '---'
        print AliceM

	s.close()

if __name__ == "__main__":
	Main()
