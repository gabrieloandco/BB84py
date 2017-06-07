# Copyright (c) 2016 Gabriel Oliveri (<gabrieloandco@gmail.com>)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
		print AliceM
		print cons
		print key


	c.close()

if __name__=='__main__':
	Main()

