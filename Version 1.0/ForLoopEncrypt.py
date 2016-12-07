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

        
        
            
        
