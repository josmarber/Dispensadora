__author__ = 'Chema'
import socket

HOST = '192.168.1.10'   # Symbolic name meaning the local host
PORT = 24069    # Arbitrary non-privileged port
s = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
s.connect((HOST,PORT))
while True:
    command = input('Enter your command: ')
    if command.split(' ',1)[0]=='STORE':
        while True:
            additional_text = input()
            command = command+'\n'+additional_text
            if additional_text=='.':
                break
    s.send(command.encode())
    reply = s.recv(1024).decode()
    if reply=='Quit':
        break
    print (reply)