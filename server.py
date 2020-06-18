import socket

s = socket.socket()
port = 65521
s.bind(('127.0.0.1', port))
s.listen(5)
print('Waiting for connection...')
c, addr = s.accept()
print ("Socket Up and running with a connection from",addr)
while True:
    rcvdData = c.recv(1024).decode()
    print ("Accepted: ",rcvdData)
c.close()