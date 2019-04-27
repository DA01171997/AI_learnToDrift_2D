import numpy as np
import random
import os
class AI():
    def __init__(self):
        #hyperparameters
        self.maxEpisode = 500000
        self.maxSteps = 2000
        self.learningRate = 0.9
        self.discountRate = 0.5
        self.exploreRate = 1.0
        self.maxExploreRate = 1.0
        self.minExploreRate = 0.1
        self.decayRate= 0.01
        self.exp_tradeoff=0.0
        #initialize Qtable
        #and create 2D to 1D mapping (and vice versa) dictionaries
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
        self.completeCounter=0
        self.option=""
        self.done=False

        
        self.environmentVariable={
        "learningRate":self.learningRate,
        "discountRate":self.discountRate,
        "exploreRate":self.exploreRate,
        "decayRate":self.decayRate,
        "currentState":self.currentState,
        "episodeCounter":self.episodeCounter,
        "exp_tradeoff":self.exp_tradeoff,
        "option":self.option,
        "done":self.done, 
        "maxExploreRate":self.maxExploreRate, 
        "minExploreRate":self.minExploreRate,
        "maxEpisode":self.maxEpisode,
        "maxSteps":self.maxSteps}

        #play variables
        self.playEpisodeCounter =0
        self.maxPlayEpisode = 100
        self.playStepCounter = 0
        self.maxPlayStep = 300
        self.playCurrentState = self.twoT1([0,0])
        self.stopPlayFlag=False
        self.playDone = False
        self.rewardSum = 0
        self.playCompleteCounter =0
        self.rewards= []

        #used to keep track of last 4 actions and states 
        self.actionCounter = 0
        self.actionArray=[None,None,None,None]
        self.stateRepeatCounter = 0
        self.stateRepeatArray=[None,None,None,None]

        #printing variable
        self.minStep = self.maxSteps

    #convert 1D value to 2D array
    def oneT2(self, number):
        string = self.oneToTwoD[number]
        ijlist = string.split(',')
        i = ijlist[0]
        j = ijlist[1]
        return [i,j]
    
    #convert 2D array to 1D array value
    def twoT1(self, twoD):
        string = str(twoD[0])+","+str(twoD[1])
        num = self.twoToOneD[string]
        return num
    
    # return a random movement index
    def actionSample(self):
        return np.random.randint(0,self.actionNum)
    def getEnvironment(self):
        self.environmentVariable={
        "learningRate":self.learningRate,
        "discountRate":self.discountRate,
        "exploreRate":self.exploreRate,
        "decayRate":self.decayRate,
        "currentState":self.currentState,
        "episodeCounter":self.episodeCounter,
        "exp_tradeoff":self.exp_tradeoff,
        "option":self.option,
        "done":self.done, 
        "maxExploreRate":self.maxExploreRate, 
        "minExploreRate":self.minExploreRate,
        "maxEpisode":self.maxEpisode,
        "maxSteps":self.maxSteps}
        return self.environmentVariable 
    def setEnvironment(self,environment):
        self.environmentVariable=environment
        self.learningRate = self.environmentVariable["learningRate"]
        self.discountRate = self.environmentVariable["discountRate"]
        self.exploreRate = self.environmentVariable["exploreRate"]
        self.decayRate = self.environmentVariable["decayRate"]
        self.currentState = self.environmentVariable["currentState"]
        self.episodeCounter = self.environmentVariable["episodeCounter"]
        self.exp_tradeoff = self.environmentVariable["exp_tradeoff"]
        self.option = self.environmentVariable["option"]
        self.done = self.environmentVariable["done"]
        self.maxExploreRate = self.environmentVariable["maxExploreRate"]
        self.minExploreRate = self.environmentVariable["minExploreRate"]
        self.maxEpisode = self.environmentVariable["maxEpisode"]
        self.maxSteps = self.environmentVariable["maxSteps"]


    #Training function
    #think of it as the loop that get run
    #ever frame.
    def train(self,window,car):

        #think of this as a outer for loop
        if self.episodeCounter <self.maxEpisode:
            
            #inner loop
            if self.stepCounter < self.maxSteps and self.stopFlag==False:

                #trade off to explore or exploit
                self.exp_tradeoff = random.uniform(0,1)
                if self.exp_tradeoff > self.exploreRate:
                    self.option="choose"
                    action = np.argmax(self.qTable[self.currentState,:])
                else:
                    self.option="random"
                    action = self.actionSample()

                #keep track the last 4 state and actions
                repeating = ""
                self.stateRepeatArray[self.stateRepeatCounter%4] = self.currentState
                self.actionArray[self.actionCounter%4] = action

                #start after step >4
                #make sure the chosen action doesn't lead it
                #to go in circle by randomly select action that's won't be the repeating action
                if self.stepCounter >=4:
                    if self.actionArray[0] ==self.actionArray[2] and self.actionArray[1] ==self.actionArray[3]:
                        if self.stateRepeatArray[0] ==self.stateRepeatArray[2] and self.stateRepeatArray[1] ==self.stateRepeatArray[3]:
                            repeating = "Repeated"
                            while True:
                                action = self.actionSample()
                                if action!=self.actionArray[0] and action!=self.actionArray[1]:
                                    break
                

                #get the next state
                newState, reward, self.done = car.newState(action)
                newState = self.twoT1(newState)
                
                #back propagating the Qvalue of the previous state
                #now set newstate to current state
                self.qTable[self.currentState, action] = self.qTable[self.currentState,action] + self.learningRate * (reward + self.discountRate * np.max(self.qTable[newState,:])- self.qTable[self.currentState,action])
                self.currentState = newState


                #check to see the current state is a goal state
                #save and the Qdata
                if self.done == True:
                    self.stopFlag = True
                    
                    #save the Q table
                    name ='auto-saveQtable' + str(self.completeCounter) +'.txt'
                    window.saveFile(name,whatToSave=self.qTable,option="Q")

                    #save the environment
                    name = 'auto-saveEnvironment'
                    name= name + str(self.completeCounter) +".npy"
                    environment = self.getEnvironment()
                    window.saveFile(name,whatToSave=environment,option="E")

                    self.completeCounter+=1
                    if self.stepCounter < self.minStep:
                        self.minStep = self.stepCounter
    
                print([self.currentState,newState,action,reward,self.done,self.option,self.exp_tradeoff,self.exploreRate, repeating])
                
                #increment counter for the  inner loop
                #reseting the index for that used
                #to keep track of the last 4 actions and state 
                self.stepCounter +=1
                self.actionCounter +=1
                self.stateRepeatCounter +=1
                if self.actionCounter >=4:
                    self.actionCounter = 0
                if self.stateRepeatCounter >=4:
                    self.stateRepeatCounter = 0
            
            #increment counter for the  outer loop
            #reducing the exploring rate
            #reseting the environment for next episode
            if self.stepCounter ==self.maxSteps-1 or self.stopFlag:
                self.exploreRate = self.minExploreRate + (self.maxExploreRate - self.minExploreRate)*np.exp(-self.decayRate *self.episodeCounter)        
                self.stepCounter=0
                self.episodeCounter +=1
                window.resetCar()
                self.stopFlag = False
                self.currentState = self.twoT1([0,0])
        
        #updates the variables that get print on screen
        window.updateES(self.episodeCounter,self.stepCounter,self.completeCounter)

    
    #Playing function
    #think of it as the loop that get run
    #ever frame.
    def play(self,window,car):
        if self.playEpisodeCounter < 1:
            if self.playStepCounter < self.maxPlayStep and self.stopPlayFlag ==False:
                action = np.argmax(self.qTable[self.playCurrentState,:])
                playNewState, reward, self.playDone = car.newState(action)
                print([action,playNewState, self.twoT1(playNewState), reward, self.playDone])
                playNewState = self.twoT1(playNewState)
                
                self.rewardSum += reward

                self.playCurrentState = playNewState
                
                if self.playDone == True:
                    self.stopPlayFlag = True
                    self.playCompleteCounter+=1
                    self.rewards.append(self.rewardSum)

                self.playStepCounter +=1
            
            if self.playStepCounter == self.maxPlayStep -1 or self.stopPlayFlag:
                self.playStepCounter = 0
                self.playEpisodeCounter +=1
                window.resetCar()
                self.stopPlayFlag = False
                self.rewardSum = 0
        window.updateES(self.playEpisodeCounter,self.playStepCounter,self.playCompleteCounter)
