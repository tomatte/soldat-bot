import socket
import re
import time

HOST = '192.168.18.4'
PORT = 23074
PASS = 'admin'

sock = socket.socket()
sock.connect((HOST, PORT))
sock.send(b'admin\n')
#sock.send(str.encode("REFRESH\n"))
msg = ""
i = 10
while i > 0:
    msg = "/say " + str(i)
    sock.send(str.encode(msg))
    i += 1
    time.sleep(1)
    
#print(socket.recv(256))
