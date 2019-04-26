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
from tempfile import TemporaryFile
WINDOWWIDTH=1280
WINDOWHEIGHT=720
class AI():
    def __init__(self):
        self.maxEpisode = 500000
        self.maxTestEpisode = 100
        self.maxSteps = 100
        self.learningRate = 0.7
        self.discountRate = 0.618
        self.exploreRate = 1.0
        self.maxExploreRate = 1.0
        self.minExploreRate = 0.1
        self.decayRate= 0.01
        self.actionNum = 4
        self.stateNum = 0
        self.twoToOneD = {}
        self.oneToTwoD = {}
        self.exp_tradeoff=0
        for j in range(12):
            for i in range(24):
                string = str(i)+","+str(j)
                self.twoToOneD[string] = self.stateNum
                self.oneToTwoD[self.stateNum]= string
                self.stateNum+=1
        self.qTable = np.zeros((self.stateNum,self.actionNum))
        self.currentState = self.twoT1([0,0])
        self.episodeCounter = 0
        self.stepCounter = 0
        self.done = False
        self.stopFlag = False
    
        #train
        self.rewards = []
        self.totalReward=0
    def oneT2(self, number):
        string = self.oneToTwoD[number]
        ijlist = string.split(',')
        i = ijlist[0]
        j = ijlist[1]
        return [i,j]
    def twoT1(self, twoD):
        string = str(twoD[0])+","+str(twoD[1])
        num = self.twoToOneD[string]
        return num
    def actionSample(self):
        return np.random.randint(0,4)
    def train(self,window,car):
        if self.episodeCounter <self.maxEpisode and not self.stopFlag:
            if self.stepCounter < self.maxSteps and not self.stopFlag:
                self.exp_tradeoff = random.uniform(0,1)
                if self.exp_tradeoff > self.exploreRate:
                    option="choose"
                    action = np.argmax(self.qTable[self.currentState,:])
                else:
                    option="random"
                    action = self.actionSample()
                
                newState, reward, self.done = car.newState(action)
                newState = self.twoT1(newState)
                
                #print[self.currentState]
                self.qTable[self.currentState, action] = self.qTable[self.currentState,action] + self.learningRate * (reward + self.discountRate * np.max(self.qTable[newState,:])- self.qTable[self.currentState,action])
                
                if self.done == True:
                    self.stopFlag = True
                    np.savetxt('test1.txt', self.qTable, fmt='%f')
                    print("saved")
                    return True
                #  print [self.qTable[self.currentState,action] + self.learningRate * (reward + self.discountRate * np.max(self.qTable[newState,:])- self.qTable[self.currentState,action])]
                self.exploreRate = self.minExploreRate + (self.maxExploreRate - self.minExploreRate)*np.exp(-self.decayRate *self.episodeCounter)
                print([self.currentState,newState,action,reward,self.done,option,self.exp_tradeoff,self.exploreRate])
                self.currentState = newState
                
                
                self.stepCounter +=1
            if self.stepCounter ==99:        
                window.resetCar()
                self.stepCounter=0
                self.episodeCounter +=1
                done = False
        #print(str(self.episodeCounter)+" "+str(self.stepCounter))
        window.updateES(self.episodeCounter,self.stepCounter)

    def play(self,window,car):
        if self.episodeCounter <self.maxTestEpisode:
            if self.stepCounter < self.maxSteps and not self.stopFlag:
                action = np.argmax(self.qTable[self.currentState,:])
                newState, reward, self.done = car.newState(action)
                self.totalReward +=reward
                if self.done == True:
                    self.stopFlag = True
                    print("Score =" + str(sum(self.rewards)/self.episodeCounter))
                    return True
                self.stepCounter +=1
                print([self.currentState,newState,action,reward,self.done,self.episodeCounter,self.stepCounter])
                self.currentState = newState
            if self.stepCounter ==199:
                self.rewards.append(self.totalReward)    
                window.resetCar()
                self.stepCounter=0
                self.episodeCounter +=1
                done = False
                self.totalReward = 0



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
        self.stop = True
        self.episodeCounter = 0
        self.stepCounter = 0
        self.play = False
            
    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.fps_display.draw()
        self.testGrid.draw()
        self.testTrack.draw()
        self.car.draw()
        self.centerLabel = pyglet.text.Label()
        self.centerLabel.draw()
        self.centerLabel = pyglet.text.Label(("Episode = " + str(self.episodeCounter)+ " , Step = " + str(self.stepCounter)),
                font_name='Times New Roman',                      
                font_size=15,
                x= 400, y=20,
                color=(0, 0, 255, 255))
        self.centerLabel.draw()
        
    def on_key_press(self, symbol,modifiers):
        if symbol == key.UP:
            #print(self.car.goStraight())
            #print(self.car.newState(0))
            #self.car.goStraight()
            self.car.newState(0)
        elif symbol == key.DOWN:
            #self.car.goReverse()
            #print(self.car.goReverse())
            self.car.newState(3)
        elif symbol == key.LEFT:
            #print(self.car.turnLeft())
            #self.car.turnLeft()
            self.car.newState(1)
        elif symbol == key.RIGHT:
            self.car.newState(2)
            #print(self.car.turnRight())
            #self.car.turnRight()
        elif symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == key.SPACE:
            #outfile = TemporaryFile()
            #np.save(outfile,self.ai.qTable)
            np.savetxt('test1.txt', self.ai.qTable, fmt='%f')
            print("saved")
        elif symbol == key.ENTER:
            self.stop = False
        elif symbol == key.BACKSPACE:
            tempA = np.loadtxt('test1.txt', dtype =float)
            self.ai.qTable = tempA
            print(self.ai.qTable)
            self.play = True
    
    #reset car env
    def resetCar(self):
        self.car = CarSprite()

    #check for points
    #check for complete
    #done when checkpoint is TRUE
    #then reset
    def update(self, dt):
        #print(self.ai.twoT1(self.car.currentState()))
        #print(self.ai.oneT2(self.ai.twoT1(self.car.currentState())))
        if self.stop is not True:
            self.stop=self.ai.train(self,self.car)
        if self.play:
            self.ai.play(self,self.car)
        
    def updateES(self,episode,step):
        self.episodeCounter = episode
        self.stepCounter = step
            
if __name__ == "__main__":
    window = MyWindow(WINDOWWIDTH,WINDOWHEIGHT, "DRIFT AI", resizable=True, vsync =True)
    window.push_handlers(window.key_handler)
    pyglet.clock.schedule_interval(window.update,1/200.0)
    pyglet.app.run()