__author__ = 'Chema'

import socket
import RPi.GPIO as GPIO

class Server:
    """this is the class for a simple server"""
    def __init__(self,host,port):
        self.host = host
        self.port = port

    def create(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.__initializeGPIO()
        self.s.listen(1)

    def listen(self):
        print("waiting for connection...")
        conn, addr = self.s.accept()
        while(True):
            data = conn.recv(1024).decode()
            print('Data: '+data)
            if(data == 'ledon'):
                self.__ledOn()
                self.response = "led encendido[OK]"
            elif(data == 'ledoff'):
                self.__ledOff()
                self.response = "led apagado[OK]"
            elif (data == 'quit'):
                self.response = "[QUIT]"
            elif (data == 'order'): #this start to take orders
                print(aux)
            else:
                self.response = "comando no reconocido[ER]"
            conn.send(self.response.encode())

    def __initializeGPIO(self):
       # GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)

    def __ledOn(self):
        GPIO.output(11,True)

    def __ledOff(self):
        GPIO.output(11,False)

