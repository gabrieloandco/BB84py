import socket
import pickle
import AliceClass
import BobGen

def Main():
	host='192.168.0.10'
	port=5000
	s = socket.socket()
	s.bind((host,port))
	
	s.listen(1)
	c, addr = s.accept()
	print "Bob address is:" + str(addr)
	while True:
		data = c.recv(1024)
		if not data:
			break
		recvobject=pickle.loads(data)
		print 'Trash'
		print recvobject	
		Bo = BobGen.BobGen(recvobject.blocks)
		Result=recvobject.Measure(Bo)
		print Result
                print 'ID:' + str(id(recvobject))
		blocks=int(raw_input('give me side 1'))
        	objects = AliceClass.Alice(blocks)
	  	print 'Your ID: ' + str(id(objects))
		data= pickle.dumps(objects)
		c.send(data)
	c.close()
if __name__=='__main__':
	Main()

