__author__ = 'Chema'

class Pixel:
    """Clase que define un pixel"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def suma(self, b):
        res = Pixel(0,0)
        res.x = self.x + b.x
        res.y = self.y + b.y
        return res

    def resta(self, b):
        res = Pixel(0,0)
        res.x = self.x - b.x
        res.y = self.y - b.y
        return res

    def printPixel(self):
        print('Coordenada x: '+ str(self.x) +' Coordenada x: ' + str(self.y))

