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

try:
    from Crypto.Cipher import AES
    from Crypto import Random
except:
    raise Warning('Pycrypto not installed')
    pycryptoimported = False
else:
    pycryptoimported = True


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
            string = 'Wrong Key :('
            break
    return string


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

def Encrypt(message,key,mode='ForLoop'):
    if mode == 'ForLoop':
        enmessage= ForLoopEncrypt(message,key)
    elif mode == 'Xor':
        enmessage= XorEncrypt(message,key)
    elif mode == 'ForLoopXor':
        enmessage = XorEncrypt(ForLoopEncrypt(message,key),key)
    elif mode == 'PyCryptAES':
        if pycryptoimported:
            key = ''.join([str(0) for i in range(16-len(hex(key)[2:]))]) + hex(key)[2:]
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(key, AES.MODE_CFB,iv)
            enmessage = iv+cipher.encrypt(message)

        else:
            raise Exception('Pycrypto not imported')

    else:
        raise Exception("Mode not available")
    return enmessage

def Decrypt(enmessage,key,mode='ForLoop'):
    if mode == 'ForLoop':
        message= ForLoopDecrypt(enmessage,key)
    elif mode == 'Xor':
        message= XorDecrypt(enmessage,key)
    elif mode == 'ForLoopXor':
        message = ForLoopDecrypt(XorDecrypt(enmessage,key),key)
    elif mode=='PyCryptAES':
        if pycryptoimported:
            key = ''.join([str(0) for i in range(16-len(hex(key)[2:]))]) + hex(key)[2:]
            iv = enmessage[0:16]
            cipher = AES.new(key, AES.MODE_CFB,iv)
            message =cipher.decrypt(enmessage[AES.block_size:])
        else:
            raise Exception('Pycrypto not imported')

    else:
        raise Exception("Mode not available")
    
    return message

if  __name__ == '__main__':
    
    modes = ['ForLoop','Xor','ForLoopXor','PyCryptAES']
    keys = [102,1232,10202,103232,1949234]
    message = 'Hello there'

    for mode in modes:
        for key in keys:
            print('Testing '+ mode)
            enmessage= Encrypt(message,key,mode)
            demessage = Decrypt(enmessage,key,mode)
            print('Decryption with correct key:' + demessage)


