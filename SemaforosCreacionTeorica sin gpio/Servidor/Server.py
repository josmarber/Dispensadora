__author__ = 'Chema'

import threading
import socket
import sqlite3
from collections import deque

class Server:
    __debug = True
    #inicializa las variables host y port y crea un cerrojo
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__bloqCola = threading.RLock()
        self.cola = deque()
        threading.Thread(target=self.sniffer).start()
        self.dispensadora = {}
        self.connections = {}

    #crea el socket e inicia el metodo de escucha
    def create(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.bind((self.__host, self.__port))
        #en esta linea generar los hilos para los metodos de escucha
        self.__s.listen(1)
        self.listen()

    #espera que haya conexiones, cada conexion que entra crea un hilo nuevo para poder recibir otra conexion.
    def listen(self):
        self.printDebug('Esperando conexion...')
        conn, addr = self.__s.accept()
        self.printDebug('Conexion establecida')
        creadorHilos = threading.Thread(target=self.listen)
        creadorHilos.start()#inicio un nuevo proceso para que desde otro hilo "escuche mas clientes"
        while(True):
            data = conn.recv(1024).decode()
            if(data == 'cobrar'): #todo hay k destruir el proceso
                self.printDebug("destruccion hilo")

            elif(data == 'estado'):#se ha conectado una maquina, actualizo la tabla de makinas (id,estado)
                conn.send("status".encode())
                idEstado = conn.recv(1024).decode()
                status = idEstado.split(',')
                self.__bloqCola.acquire()
                self.dispensadora[status[0]] = status[1] #a la id de la maquina le asigno el estado de la maquina
                self.connections[status[0]] = conn #guardo la conexion para en el futuro mandar el pedido a la dispensadora
                self.__bloqCola.release()

            else:
                try:
                    pedido = data.split(',')
                    size = len(pedido)

                    idCliente = pedido[0]
                    idPedido = pedido[1]
                    horaPedido = pedido[2]
                    comanda = {}

                    for i in range(3,size,2): #creo diccionario con el pedido
                        if(pedido[i] == "fpedido"):
                            self.printDebug("fin pedido")
                        else:
                            print(pedido[i])
                            comanda[pedido[i]]= pedido[i+1]
                    self.dispatcher(idCliente,idPedido,horaPedido,comanda)
                    conn.send('[ok]'.encode())
                except IndexError:
                    print("Error organizando el pedido. Formato del pedido incorrecto")
                    conn.send('[error]'.encode())

                #todo crear base de datos para las bebidas con sus tiempos y precios, la tienen que tener presente todoas las dispensadoras
                #todo crear base de datos para almacenar los pedidos de una sesion, el guardado lo realizara el servidor
                #todo implementar el metodo cobrar, es calcularlo y mandarle el precio al cliente

    def dispatcher(self, idCliente,idPedido,horaPedido,comanda):
        pedido = [idCliente,idPedido,horaPedido,comanda]
        self.__bloqCola.acquire() #boqueamos para que nadie mas modifique en este tiempo la variable cola
        self.cola.append(pedido)
        self.__bloqCola.release()
        print("tamaño cola: "+str(len(self.cola)))

    def sniffer(self):# metodo de busqueda y asignacion de pedidos segun la cola
        while True:
            if(len(self.cola)>0):
                self.__bloqCola.acquire()
                pedido = self.cola.pop()
                self.__bloqCola.release()
                comanda = "pedido"
                for ped in pedido[3]: #convierto el array a string para mandar el pedido
                    comanda += ","+ped
                while True:
                    if(len(self.dispensadora == 0)):
                        self.printDebug("no hay dispensadoras conectadas")
                    else:
                        idDisp = self.dispensadora.keys()
                        for key in idDisp:
                            if(self.dispensadora[key]=="free"):
                                self.connections[key].send(pedido[3])
                                if(self.connections[key].recv(1024).decode() == "[ok]"):
                                    self.printDebug("pedido enviado a la dispensadora")
                                    break

    def printDebug(self,texto):
        if(self.__debug == True):
            print(texto)



