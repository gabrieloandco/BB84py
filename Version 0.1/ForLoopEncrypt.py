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

import random
import binascii
##repeat with iterators and generators
def ForLoopEncrypt(string,key):
    enstring=''
    for letter in string:
        for i in range(key):
            enstring+=binascii.unhexlify('%x' % random.SystemRandom().choice(range(16,256)))
        enstring+=letter
    return enstring

def ForLoopDecrypt(enstring,key):
    destring=''
    iterator=key
    while iterator < len(enstring):
        destring += enstring[iterator]
        iterator +=key+1

    return destring

def Main():
    string = raw_input("Message: ")
    key1 = int(raw_input("Key: "))
    enstring = ForLoopEncrypt(string,key1)
    print "encrypted: " +  enstring
    key2 = int(raw_input("Key: "))
    destring = ForLoopDecrypt(enstring,key2)
    print destring

if __name__ == "__main__":
    Main()

        
        
            
        
