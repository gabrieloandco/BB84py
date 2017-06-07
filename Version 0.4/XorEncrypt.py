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

import binascii
##in development
def XorEncrypt(string,key):
    bitlist=[]
    for letter in string:
        bitlist.append(bin(int(binascii.hexlify(letter),16) ^ key))
        
    return  str(bitlist)

def XorDecrypt(bitlist,key):
    lis = eval(bitlist)
    string=''
    for bit in lis:
        try:
            number = int(bit,2)^key
            string += binascii.unhexlify('%x' % number)
        except:
            print 'Wrong Key :('
            break
    return string
    

def Main():
    string = raw_input('Give me a string: ')
    key = int(raw_input('Give me a key: '))
    enstring= XorEncrypt(string,key)
    key = int(raw_input('Give me the key: '))
    stri= XorDecrypt(enstring,key)
    print stri


if __name__ == '__main__':
    Main()
    
