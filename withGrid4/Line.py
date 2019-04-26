from pyglet.gl import *
from pyglet.window import key
from pyglet.window import FPSDisplay
import math

class Line():
    def __init__(self,x1,y1,x2,y2,color=None,z=None):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.z=z
        self.color = color
    def draw(self):
        if self.z is None:
            self.z=1
        glBegin(GL_LINES)
        if self.color:
            glColor3f(self.color[0],self.color[1],self.color[2])
        else:
            glColor3f(1,0,0)
        glVertex3f(float(self.x1),float(self.y1),float(self.z))
        glVertex3f(float(self.x2),float(self.y2),float(self.z))
        glEnd()