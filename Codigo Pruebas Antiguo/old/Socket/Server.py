__author__ = 'Chema'
import RPi.GPIO as GPIO ## Import GPIO library

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(11, GPIO.OUT) ## Setup GPIO Pin 11 to OUT

# Accept the connection once (for starter)
HOST = ''   # Symbolic name meaning the local host
PORT = 24069    # Arbitrary non-privileged port
s = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
print ('Socket created')
s.bind((HOST, PORT))
print ('Socket bind complete')
s.listen(1)
print ('Socket now listening')
(conn, addr) = s.accept()
print ('Connected with ' + addr[0] + ':' + str(addr[1]))
stored_data = ''
while True:
    # RECEIVE DATA
    data = conn.recv(1024).decode()
    # PROCESS DATA
    tokens = data.split('\n')            # Split by space at most once
    print(tokens)
    command = tokens[0]                   # The first token is the command
    print("comando recibido: "+ command)
    if command=='GET':                    # The client requests the data
        reply = stored_data               # Return the stored data
    elif command=='STORE':                # The client want to store data
        stored_data = tokens[1]           # Get the data as second token, save it
        reply = 'OK'                      # Acknowledge that we have stored the data
    elif command=='TRANSLATE':            # Client wants to translate
        stored_data = stored_data.upper() # Convert to upper case
        reply = stored_data               # Reply with the converted data
    elif command == 'ledon':
        GPIO.output(11,True)
        reply = 'OK'
    elif command == 'ledoff':
        GPIO.output(11,False)
        reply = 'OK'
    elif command=='QUIT':                 # Client is done
        conn.send('Quit'.encode())           # Acknowledge
        conn.close()
        break                                # Quit the loop
    else:
        reply = 'Unknown command'
    # SEND REPLY
    conn.send(reply.encode())
conn.close() # When we are out of the loop, we're done, close