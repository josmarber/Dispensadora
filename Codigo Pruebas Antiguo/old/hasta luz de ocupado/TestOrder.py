__author__ = 'Chema'

from Order.Order import *

x = Order()
x.add([10,2])
x.add([5,1])
x.showOrders()
x.remove([10,2])
x.showOrders()