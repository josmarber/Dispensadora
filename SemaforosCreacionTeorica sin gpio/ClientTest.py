__author__ = 'Chema'
from Cliente.Client import *

y = Client('localhost',2525)

y.connect()
y.command()