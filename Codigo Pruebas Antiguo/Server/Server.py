__author__ = 'Chema'

import socket
import RPi.GPIO as GPIO
import threading
import time
import sqlite3

class Server:
    """this is the class for a simple server"""
    list = []

    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.__order = False


    def create(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        #definir metodos de escucha de boton y lista de espera, nada mas que se crea deberia de empezar a comprobarlo a traves de hilos
        self.__initializeGPIO()
        button = threading.Thread(target=self.listenButton)
        button.start()#inicio lectura del boton
        order = threading.Thread(target=self.readList)
        order.start()#inicio lectura de la lista
        self.s.listen(1)

    def listen(self):
        print('waiting for connection...')
        conn, addr = self.s.accept()
        print('Conexion establecida')
        wireListening = threading.Thread(target=self.listen)
        wireListening.start()#inicio un nuevo proceso para que desde otro hilo "escuche mas clientes" POR ALGUN MOTIVO FUNCIONA!!!!
        while(True):
            data = conn.recv(1024).decode()
            self.list.append(data)
            conn.send('[ok]'.encode())


    def __initializeGPIO(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.IN)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)

    def listenButton(self):
        while(True):
            if(GPIO.input(11)):
                if(GPIO.input(7)):
                    time.sleep(0.5)
                    doing = threading.Thread(target=self.oidoCocina)
                    doing.start()
                    del self.list[0]
                    print(self.list)

    def readList(self):
        while (True):
            if(len(self.list)>0):
                GPIO.output(11,True)
            else:
                GPIO.output(11,False)

    def oidoCocina(self):
        self.db = sqlite3.connect('Database/contentDB/bebidas')
        cursor = self.db.cursor()
        cursor.execute('''
                   SELECT * FROM bebidas
        ''')
        rows = cursor.fetchall()
        for row in rows:
            secs = row[2]
        GPIO.output(13,True)
        time.sleep(secs)
        GPIO.output(13,False)