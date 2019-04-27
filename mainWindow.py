from pyglet.gl import *
from pyglet.window import key
from pyglet.window import FPSDisplay
import math
from CarSprite import *
from Line import *
from Track import *
from Grid import *
import numpy as np
import random
from AI import *
import sys
import os
WINDOWWIDTH=1280
WINDOWHEIGHT=720

class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(MyWindow,self).__init__(*args, **kwargs)
        #this clear thing affect the background color
        #comment it out to get a black background
        glClearColor(1,1.0,1.0,1)
        self.fps_display = FPSDisplay(self)
        self.car = CarSprite()
        self.key_handler = key.KeyStateHandler()
        self.testTrack= Track([40,60,1200,600],[240,260,800,200])
        self.testGrid = Grid(40,60,1200,600,50)
        self.ai = AI()
        self.train = False
        self.play = False
        self.manualSaveCounter=0
        #printing variable
        self.episodeCounter = 0
        self.stepCounter = 0
        self.completeC=0
        self.minStep = self.ai.maxSteps

    
    #get called by update()
    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.fps_display.draw()
        self.testGrid.draw()
        self.testTrack.draw()
        self.car.draw()
        self.bottomLabel = pyglet.text.Label()
        self.topLabel = pyglet.text.Label()


        #print bottom message on screen
        thisIterationNameIs="First Working Version"
        self.minStep = self.ai.minStep
        self.bottomLabel = pyglet.text.Label((thisIterationNameIs+":  Episode = " + str(self.episodeCounter)+ " , minStep = " + str(self.minStep)+ " , Step = " + str(self.stepCounter)+ " , Complete = " + str(self.completeC)),
                font_name='Times New Roman',                      
                font_size=15,
                x= 400, y=20,
                color=(0, 0, 255, 255))
        self.bottomLabel.draw()

        self.topLabel = pyglet.text.Label((str(self.ai.getCurrentVariable())),
                font_name='Times New Roman',                      
                font_size=9,
                x= 1, y=690,
                color=(0, 0, 255, 255))
        self.topLabel.draw()
        
    #get called by update()
    #perform action based on user input
    def on_key_press(self, symbol,modifiers):
        if symbol == key.UP:
            self.car.newState(0)
        elif symbol == key.DOWN:
            self.car.newState(3)
        elif symbol == key.LEFT:
            self.car.newState(1)
        elif symbol == key.RIGHT:
            self.car.newState(2)
        elif symbol == key.ESCAPE:
            pyglet.app.exit()

        #for user to manually save current Q table
        elif symbol == key.SPACE:
            name ='manualSaveQTable' + str(self.manualSaveCounter) +'.txt'
            self.saveFile(name)
            self.manualSaveCounter+=1
            
        #enter to train
        elif symbol == key.ENTER:
            self.train = True
            self.play = False
        #backspace to play
        elif symbol == key.BACKSPACE:
            self.play = True
            self.train = False
        
        #load and then train manually
        elif symbol == key._1:
            name = "fileNameHere"
            loadedQtable = self.loadFile(name)
            if loadedQtable != None:
                self.ai.qTable =loadedQtable
                print(self.ai.qTable)
                self.ai.play(self,self.car)
            else:
                print("Error loading: "+name)
    
    #reset car environment
    def resetCar(self):
        self.car = CarSprite()

    #get called every frame
    #check if we enter to train
    # or play
    def update(self, dt):

        #train if enter pressed
        if self.train:
            self.ai.train(self,self.car)

        #play if backspace is pressed
        #or the qtable text file is given as parameters
        if self.play or len(sys.argv)>1:
            name = str(sys.argv[1])
            loadedQtable = self.loadFile(name)
            if loadedQtable != None:
                self.ai.qTable =loadedQtable
                print(self.ai.qTable)
                self.ai.play(self,self.car)
            else:
                print("Error loading: "+name)
        
    #update called to update value we print on screen
    def updateES(self,episode,step,complete):
        self.episodeCounter = episode
        self.stepCounter = step
        self.completeC = complete

    #supporting function
    def createDirectory(self,directoryName):
        if not os.path.exists(directoryName):
            os.makedirs(directoryName)
    def loadFile(self,fileName):
        if os.path.isfile(fileName):
            tempA = np.loadtxt(fileName, dtype =float)
            return tempA
        else:
            return None
    def saveFile(self,name, directory = "./saveData/"):
        self.createDirectory(directory)
        name = directory+name
        np.savetxt(name, self.ai.qTable, fmt='%f')
        print("Save: " + name)

#start window
if __name__ == "__main__":
    window = MyWindow(WINDOWWIDTH,WINDOWHEIGHT, "DRIFT AI", resizable=True, vsync =True)
    window.push_handlers(window.key_handler)
    pyglet.clock.schedule_interval(window.update,1/100.0)
    pyglet.app.run()