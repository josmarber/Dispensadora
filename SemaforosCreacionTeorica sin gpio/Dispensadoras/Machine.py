__author__ = 'Chema'

import socket
import time

class Machine:

    __debug = True

    def __init__(self,host,port,id):
        self.__host = host
        self.__port = port
        self.__id = id
        self.__status = "free"


    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.__host, self.__port))
        self.sendStatus()
        self.sniffer()

    def sendStatus(self):
        self.client.send(str(self.__id)+","+self.__status)

    def sniffer(self):
        while True:
            command = self.client.recv(1024).decode()
            if (command == "status"):
                self.sendStatus()
            elif(command.find("pedido")>0):
                pedido = command.split(',')
                self.__status = "busy"
                self.sendStatus()
                self.ejecutaPedido(pedido)
                self.__status = "free"
                self.sendStatus()
            if (command == "quit"):
                break

    def ejecutaPedido(self,command):
        for i in range (1,len(command),2):
            self.sirveProducto(command[i],command[i+1])

    def sirveProducto(self, prod, cantidad): #movimiento arduino, de momento todos los productos tardan 5 segundos
        self.printDebug("Sirviendo: " + prod)
        time.sleep(5)
        self.printDebug("Finalizado: " + prod)

    def printDebug(self,text):
        if(self.__debug):
            print(text)

    #todo definir funciones para apagar la maquina correctamente con un boton y mande mensaje de desconexion
    #todo definir y crear bd con bebidas y tiempos




