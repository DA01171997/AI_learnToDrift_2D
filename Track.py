from pyglet.gl import *
from pyglet.window import key
from pyglet.window import FPSDisplay
import math
from Line import *

#Draw car tracks
class Track():
    def __init__(self, outTrack, inTrack, color=None):
        self.outX=outTrack[0]
        self.outY=outTrack[1]
        self.outWidth=outTrack[2]
        self.outHeight=outTrack[3]

        self.inX=inTrack[0]
        self.inY=inTrack[1]
        self.inWidth=inTrack[2]
        self.inHeight=inTrack[3]
        self.color = color

        #outer track
        #horizonal lines
        self.outH1Line = Line(self.outX,self.outY,self.outX+self.outWidth,self.outY)
        self.outH2Line = Line(self.outX,self.outY + self.outHeight,self.outX+self.outWidth,self.outY+self.outHeight)
        #vertical lines
        self.outV1Line = Line(self.outX,self.outY,self.outX,self.outY+self.outHeight)
        self.outV2Line = Line(self.outX+self.outWidth,self.outY,self.outX+self.outWidth,self.outY+self.outHeight)
        
        #inner track
        #horizonal lines 
        self.inH1Line = Line(self.inX,self.inY,self.inX+self.inWidth,self.inY)
        self.inH2Line = Line(self.inX,self.inY + self.inHeight,self.inX+self.inWidth,self.inY+self.inHeight)

        #vertical lines
        self.inV1Line = Line(self.inX,self.inY,self.inX,self.inY+self.inHeight)
        self.inV2Line = Line(self.inX+self.inWidth,self.inY,self.inX+self.inWidth,self.inY+self.inHeight)
    def draw(self):
        #outer track
        #horizonal lines
        self.outH1Line.draw()
        self.outH2Line.draw()

        #vertical lines
        self.outV1Line.draw()
        self.outV2Line.draw()

        #inner track
        #horizonal lines
        self.inH1Line.draw()
        self.inH2Line.draw()

        #vertical lines
        self.inV1Line.draw()
        self.inV2Line.draw()
        