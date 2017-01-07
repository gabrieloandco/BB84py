import socket
import threading

salice = socket.socket()
host = '192.168.0.18'
port = 5000
salice.connect((host,port))

while True:
    message = raw_input("->")
    salice.send(message)
    received = salice.recv(1024)
    print received
