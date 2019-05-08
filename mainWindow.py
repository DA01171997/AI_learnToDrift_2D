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
import pickle
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
        self.train = 0
        self.play = 0
        self.manualSaveCounter=0

        #printing variable
        self.episodeCounter = self.ai.episodeCounter
        self.stepCounter = self.ai.stepCounter
        self.completeC=0
        self.minStep = self.ai.maxSteps
        self.toggleGrid=0
    
    def draw_label(self):
        #print bottom message on screen
        self.bottomLabel = pyglet.text.Label()
        self.topLabel = pyglet.text.Label()
        thisIterationNameIs="First Working Version"
        self.minStep = self.ai.minStep
        self.bottomLabel = pyglet.text.Label((thisIterationNameIs+":  Episode = " + str(self.episodeCounter)+ " , minStep = " + str(self.minStep)+ " , Step = " + str(self.stepCounter)+ " , Complete = " + str(self.completeC)),
                font_name='Times New Roman',                      
                font_size=15,
                x= 400, y=20,
                color=(0, 0, 255, 255))
        

        self.topLabel = pyglet.text.Label((str(self.ai.getEnvironment())),
                font_name='Times New Roman',                      
                font_size=9,
                x= 1, y=690,
                color=(0, 0, 255, 255))
        self.bottomLabel.draw() 
        self.topLabel.draw()

    
    #get called by update()
    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.fps_display.draw()
        if self.toggleGrid%2!=0:
            self.testGrid.draw()
        self.testTrack.draw()
        self.car.draw()
        self.draw_label()
    

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

        #toggle grid on or off
        #self.toggleGrid%2==0 == OFF
        elif symbol == key.G:
            self.toggleGrid +=1

        #for user to manually save current Q table
        elif symbol == key.SPACE:

            #save the Q table
            name ='manualSaveQTable' + str(self.manualSaveCounter) +'.txt'
            self.saveFile(name,whatToSave=self.ai.qTable,option="Q")

            #save the environment
            name = 'manualSaveEnvironment'
            name= name + str(self.manualSaveCounter) +".npy"
            environment = self.ai.getEnvironment()
            self.saveFile(name,whatToSave=environment,option="E")

            #increment file counter
            self.manualSaveCounter+=1
            
        #enter to train
        elif symbol == key.ENTER:
            self.train +=1
            self.play = 0
        #backspace to play
        elif symbol == key.BACKSPACE:
            self.play +=1
            self.train = 0
        
        #load Qtable manually on fresh environment
        elif symbol == key._1:
            name = "fileNameHere"
            loadedQtable = self.loadFile(name,option="Q")
            if loadedQtable != None:
                self.ai.qTable =loadedQtable
                print(self.ai.qTable)
                self.ai.play(self,self.car)
            else:
                print("Error loading: "+name)

        #load Qtable manually on saved environment
        elif symbol == key._2:

            #load QTable
            #name = "QfileName"
            name = "./saveData/manualSaveQTable1.txt"
            if os.path.isfile(name):
                loadedQtable = self.loadFile(name,option="Q")
                self.ai.qTable =loadedQtable
                print(self.ai.qTable)
                print("Loaded: "+name)
            else:
                print("Error Loading: "+ name)

            #load Environment
            #name = "EnvironmentfileName"
            name = "./saveData/manualSaveEnvironment1.npy"
            print(name)
            if os.path.isfile(name):
                tempA = np.load(name).item()
                #loadedEnvironmentDictionary = self.loadFile(name,option="E")
                #self.ai.setEnvironment(loadedEnvironmentDictionary)
                #print(loadedEnvironmentDictionary)
                print("here")
            else:
                print("Error loading: "+name)

        #reset everything
        elif symbol == key.R:
            self.resetCar()
            self.resetAI()
            self.episodeCounter = self.ai.episodeCounter
            self.stepCounter = self.ai.stepCounter
            self.completeC=0
            self.minStep = self.ai.maxSteps

            
    
    #reset car
    def resetCar(self):
        self.car = CarSprite()
        self.ai.currentState = self.ai.twoT1([0,0])
    #resest Environment
    def resetAI(self):
        self.ai = AI()

    #get called every frame
    #check if we enter to train
    # or play
    def update(self, dt):

        #train if enter pressed
        if self.train%2!=0:
            self.ai.train(self,self.car)

        #play if backspace is pressed
        #or the qtable text file is given as parameters
        if self.play or len(sys.argv)>1:
            name = str(sys.argv[1])
            loadedQtable = self.loadFile(name,option="Q")
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
    #option Q for Qtable
    #option E for Environment
    def createDirectory(self,directoryName):
        if not os.path.exists(directoryName):
            os.makedirs(directoryName)
    def loadFile(self,fileName,option):
        if option=="Q":
            tempA = np.loadtxt(fileName, dtype =float)
            return tempA
        elif option=="E":
            #tempA = np.load(fileName).item()
            #with open (fileName, 'rb') as file:
            #    tempA = pickle.load(file)
            #    print(tempA)
            return tempA

    def saveFile(self,name, whatToSave, option, directory = "./saveData/"):
        if option == "Q":
            self.createDirectory(directory)
            name = directory+name
            np.savetxt(name, whatToSave, fmt='%f')
            print("Save: " + name)
        elif option == "E":
            self.createDirectory(directory)
            name = directory+name
            print(whatToSave)
            np.save(name, whatToSave)
            print("Save: " + name)


#start window
if __name__ == "__main__":
    window = MyWindow(WINDOWWIDTH,WINDOWHEIGHT, "DRIFT AI", resizable=True, vsync =True)
    window.push_handlers(window.key_handler)
    music = pyglet.resource.media('deja-vu.mp3')    
    pyglet.clock.schedule_interval(window.update,1/100.0)
    music.play()
    pyglet.app.run()
