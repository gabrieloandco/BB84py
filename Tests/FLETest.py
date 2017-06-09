import binascii
import random
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

if __name__ == '__main__':

    for i in range(1,1000):
        try:
            en = ForLoopEncrypt('hello',i)
            de = ForLoopDecrypt(en,i)
        except:
            print(i)

