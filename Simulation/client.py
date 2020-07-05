import socket

s = socket.socket()
s.connect(('127.0.0.1',65531))

while True:
    str = input("\nMessage: ")
    s.send(str.encode());
s.close()