import socket
import pickle
import AliceClass
import BobGen
def Main():
	host='192.168.0.17'
	port = 5000
	s = socket.socket()
	s.connect((host,port))

	while True:
		blocks=int(raw_input('give me blocks'))
		objects = AliceClass.Alice(blocks)
		print 'Your ID' + str(id(objects))
		data = pickle.dumps(objects)
		s.send(data)
		data = s.recv(1024)
		recvobject=  pickle.loads(data)
		Bo = BobGen.BobGen(blocks)
		print 'Trash'
		print recvobject
		Result= recvobject.Measure(Bo)
		print Result
		print 'ID' + str(id(recvobject))

	s.close()

Main()
