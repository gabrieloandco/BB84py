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
    
