__author__ = 'Chema'
from Client.Client import *

y = Client("192.168.1.10",2525)
y.connect()
y.command()