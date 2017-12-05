import socket

def Main():
    hostEva = raw_input("Eva IP")
    portEva = 5000

    s = socket.socket()

    blocks = int(raw_input("Level of security: "))

    s.bind((hostEva,portEva))

    while True:
        c, addr = s.accept()
        strcon = c.recv(5000)
        s.close()

        c, addr = s.accept()
        strResultado = s.recv(5000)
        c.send(con)
        s.close()

        c, addr = s.accept()
        Alicestring = c.recv(5000)
        s.close()

        c, addr = s.accept()
        c.send(Alicestring)
        s,close()
        
        
        
        

        

        
