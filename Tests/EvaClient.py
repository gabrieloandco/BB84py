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
		objects = AliceClass.Alice(blocks))
		data = pickle.dumps(objects)
		s.send(data)
		data = s.recv(1024)
		recvobject=  pickle.loads(data)
		Result= recvobject.Measure(Bo)
		print Result
	s.close()

Main()
