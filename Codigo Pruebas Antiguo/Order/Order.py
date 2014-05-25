__author__ = 'Chema'

class Order:
    """Class for the orders"""
    def __init__(self):
        self.orders = []

    def add(self, order):
        self.orders.append(order)

    def remove(self,order):
        self.orders.remove(order)

    def showOrders(self):
        print(self.orders)