import socket
import pickle
import AliceClass

def Main():
	host='192.168.0.14'
	port=5000
	s = socket.socket()
	s.bind((host,port))
	
	s.listen(1)
	c, addr = s.accept()
	quitting = False
	print "Bob address is:" + str(addr)
	while not quitting:
		blocks=int(raw_input('give me blocks'))
		AliceM = AliceClass.Alice(blocks)
		AliceMbits= pickle.dumps(AliceM)
		c.send(AliceMbits)
		consbits = c.recv(1024)	
		cons = pickle.loads(consbits)
		key = AliceM.KeyAlice(cons)
		print repr(AliceM)
		print cons
		print key


	c.close()

if __name__=='__main__':
	Main()

