import random
import binascii


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
        enmessage = XorEncrypt(ForLoopEncrypt(message,int(key,2)),int(key,2))
    else:
        raise Exception("Mode not available")
    return enmessage

def Decrypt(enmessage,key,mode='ForLoop'):
    if mode == 'ForLoop':
        message= ForLoopDecrypt(enmessage,key)
    elif mode == 'Xor':
        message= XorDecrypt(enmessage,key)
    elif mode == 'ForLoopXor':
        message = ForLoopDecrypt(XorDecrypt(enmessage,int(key,2)),int(key,2))
    else:
        raise Exception("Mode not available")
    return message
    
    

#
#
