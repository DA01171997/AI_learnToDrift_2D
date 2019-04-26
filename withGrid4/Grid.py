from pyglet.gl import *
from pyglet.window import key
from pyglet.window import FPSDisplay
import math
from Line import *

class Grid():
    def __init__(self,x1,y1,width, height, gridSize):
        self.x1=x1
        self.y1=y1
        self.width=width
        self.height=height
        self.gridSize=gridSize
    def draw(self):
        for x in range(self.gridSize,self.width,self.gridSize):
            Line(self.x1+x, self.y1, self.x1+x, self.y1 + self.height,[0,1,0],0.0).draw()
        for y in range(self.gridSize,self.height,self.gridSize):
            Line(self.x1, self.y1+y, self.x1+self.width, self.y1 + y,[0,1,0],0.0).draw()

