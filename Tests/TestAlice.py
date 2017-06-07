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
    


    

