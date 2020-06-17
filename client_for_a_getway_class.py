import socket
import struct
 
def main():
    # Creating a socket object
    s = socket.socket()
    # Connecting to the server
    s.connect(('127.0.0.1', 1337))
    print('Connected to server!')
    finished = False
    # Connection handling
    while not finished:
        to_send = input('> ').encode('utf-8')
        s.sendall(struct.pack('<I', len(to_send)) + to_send)
        reply_length = struct.unpack('<I', s.recv(struct.calcsize('<I')))[0]
        reply = s.recv(reply_length)
        print('Reply from server: "{0}"'.format(reply.decode('utf-8')))
        if to_send in (b'q', b'terminate'):
            finished = True
            s.close()
 
if __name__ == '__main__':
    main()
    
    
    
   #33#3333322222 elishevada
    
    
    
    
    
    