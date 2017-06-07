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
