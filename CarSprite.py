from pyglet.gl import *
from pyglet.window import key
from pyglet.window import FPSDisplay
import math
from Line import *
import numpy as np
WINDOWWIDTH=1280
WINDOWHEIGHT=720
class CarSprite():
    def __init__(self):
        self.carSprite_image = pyglet.image.load('car_sprite5050.png')
        self.carSprite_image.anchor_x = 25
        self.carSprite_image.anchor_y = 25
        self.carSprite= pyglet.sprite.Sprite(self.carSprite_image, 40 +25, 60+25)
        self.x = self.carSprite.x
        self.y = self.carSprite.y
        self.theta = self.carSprite.rotation
        self.speed = 50.0
        self.rotation_speed = 90.0
        self.deltaX = 0.0
        self.deltaY = 0.0
        self.width = self.carSprite.width
        self.height = self.carSprite.height
        self.touchAlreadyP1=[False,False,False,False,False]
        self.touchAlreadyP2=[False,False,False,False,False]
        self.touchAlreadyP3=[False,False]
        self.touchAlreadyP4=[True,False]
        self.rewardCounter=0
    
    def draw(self):
        #draw the car
        self.carSprite.draw()
        Line(self.getX()-25,self.getY()-25,self.getX()+25,self.getY()-25,[0,0,1],1).draw()
        Line(self.getX()-25,self.getY()+25,self.getX()+25,self.getY()+25,[0,0,1],1).draw()

        Line(self.getX()-25,self.getY()-25,self.getX()-25,self.getY()+25,[0,0,1],1).draw()
        Line(self.getX()+25,self.getY()-25,self.getX()+25,self.getY()+25,[0,0,1],1).draw()
        

        #draw the check point
        #checkpointP1
        for x in range(0,4):
            Line(265 + x *200,135-25,265 +x *200,135+25,[0,0,0],1).draw()
        Line(965,185-25,965,185+25,[0,0,0],1).draw()
        
        #checkpointP2
        for x in range(0,4):
            Line(265 + x *200,460,265 +x *200,460+50,[0,0,0],1).draw()
        Line(965,460,965,460+50,[0,0,0],1).draw()

        #checkpointP3
        Line(1040,285,1040+50,285,[0,0,0],1).draw()
        #checkpointP32
        Line(1040,385,1040+50,385,[0,0,0],1).draw()

        #checkpointP4
        Line(40,285,240,285,[1,0,0],1).draw()
        #checkpointP4
        Line(40,385,240,385,[0,1,0],1).draw()


    #getter and setter
    def getX(self):
        self.x = self.carSprite.x
        return self.x
    def getY(self):
        self.y = self.carSprite.y
        return self.y
    def getTheta(self):
        self.theta = self.carSprite.rotation
        return self.theta
    def getDeltaX(self):
        return self.deltaX
    def getDeltaY(self):
        return self.deltaY
    def updateX(self,value):
        value += self.getX()
        self.carSprite.update(x=value)
    def updateY(self,value):
        value += self.getY()
        self.carSprite.update(y=value)
    def updateTheta(self,degree):  
        degree += self.getTheta()
        self.carSprite.update(rotation=degree)
    def setTheta(self,degree):
        self.carSprite.update(rotation=degree)
    def updateDeltaX(self, value):
        self.deltaX = value
    def updateDeltaY(self, value):
        self.deltaY = value

    #car movement
    def turnLeft(self):
        self.setTheta(180)
        value = self.goStraight(180)
        return value
    def turnRight(self):
        self.setTheta(0)
        value = self.goStraight(0)
        return value
    def goStraight(self,theta=-90):
        value = self.getX() + self.speed
        thetaRadian =  -math.radians(theta)
        deltaX = int(math.cos(thetaRadian) * self.speed) 
        deltaY = int(math.sin(thetaRadian) * self.speed) 
        
        #determine if we hit any wall
        #return the wall that hit
        #else return none
        if (((self.getX() + deltaX) <= 1240) and ((self.getX() + deltaX) >= 40)) and (((self.getY() + deltaY) <= 660) and ((self.getY() + deltaY) >= 60)):
            if ((self.getX() >=40 and self.getX() <= 240) and (self.getY() >=260) and self.getY()<=460) and (self.getX() + deltaX >240):
                return 240
            elif ((self.getX() >=1040 and self.getX() <= 1240) and (self.getY() >=260) and self.getY()<=460) and (self.getX() + deltaX <1040):
                return 1040
            elif ((self.getX() >=240 and self.getX() < 1040) and (self.getY() >=60) and self.getY()<=260) and (self.getY() + deltaY >260):
                return 260
            elif ((self.getX() >=240 and self.getX() < 1040) and (self.getY() >=460) and self.getY()<=660) and (self.getY() + deltaY <460):
                return 460
            elif (self.getY() + deltaY==(285)) and (self.getX()<240):
                return 285
            else:
                self.updateX(deltaX)
                self.updateY(deltaY)
                self.setTheta(theta)
                return None
        else: 
            if (self.getX() + deltaX) > 1240:
                return 1240
            elif (self.getX() + deltaX) < 40:
                return 40
            elif (self.getY() + deltaY) > 660 :
                return 660
            elif (self.getY() + deltaY) <60:
                return 60
    def goReverse(self,theta=-90):
        value = self.getX() - self.speed
        thetaRadian = -math.radians(theta)
        deltaX = int(math.cos(thetaRadian) * self.speed )
        deltaY = int(math.sin(thetaRadian) * self.speed)

        #determine if we hit any wall
        #return the wall that hit
        #else return none
        if (((self.getX() - deltaX) <= 1240) and ((self.getX() - deltaX) >= 40)) and (((self.getY() - deltaY) <= 660) and ((self.getY() - deltaY) >= 60)):
            if ((self.getX() >=40 and self.getX() <= 240) and (self.getY() >=260) and self.getY()<=460) and (self.getX() - deltaX >240):
                return 240
            elif ((self.getX() >=1040 and self.getX() <= 1240) and (self.getY() >=260) and self.getY()<=460) and (self.getX() - deltaX <1040):
                return 1040
            elif ((self.getX() >=240 and self.getX() < 1040) and (self.getY() >=60) and self.getY()<=260) and (self.getY() - deltaY >260):
                return 260
            elif ((self.getX() >=240 and self.getX() < 1040) and (self.getY() >=460) and self.getY()<=660) and (self.getY() - deltaY <460):
                return 460
            else:
                self.updateX(-deltaX)
                self.updateY(-deltaY)
                self.setTheta(-theta)
                return None
        else: 
            if (self.getX() - deltaX) > 1240:
                return 1240
            elif (self.getX() - deltaX) < 40:
                return 40
            elif (self.getY() - deltaY) > 660 :
                return 660
            elif (self.getY() - deltaY) <60:
                return 60
    
    #check for reward
    def checkPoint(self):
        #check P1
        for x in range(0,4):
            if (self.getX()==(265 + x*200)) and (self.getY()==135) and not(self.touchAlreadyP1[x]):
                print("touching "+str(self.getX())+" "+ str(self.getY()))
                self.touchAlreadyP1[x] = True
                return [self.getX(),self.getY()]
        if (self.getX()==(965)) and (self.getY()==185) and not(self.touchAlreadyP1[4]):
                print("touching "+str(self.getX())+" "+ str(self.getY()))
                self.touchAlreadyP1[4] = True
                return [self.getX(),self.getY()]
        #check P3
        if (self.getY()==(285)) and (self.getX()==1040+25) and not(self.touchAlreadyP3[0]):
                print("touching "+str(self.getX())+" "+ str(self.getY()))
                self.touchAlreadyP3[0] = True
                return [self.getX(),self.getY()]
        if (self.getY()==(385)) and (self.getX()==1040+25) and not(self.touchAlreadyP3[1]):
                print("touching "+str(self.getX())+" "+ str(self.getY()))
                self.touchAlreadyP3[1] = True
                return [self.getX(),self.getY()]
        
        
        #check P2
        for x in range(0,4):
            if (self.getX()==(265 + x*200)) and (self.getY()==460+25) and not(self.touchAlreadyP2[x]):
                print("touching "+str(self.getX())+" "+ str(self.getY()))
                self.touchAlreadyP2[x] = True
                return [self.getX(),self.getY()]
        if (self.getX()==(965)) and (self.getY()==460+25) and not(self.touchAlreadyP2[4]):
                print("touching "+str(self.getX())+" "+ str(self.getY()))
                self.touchAlreadyP2[4] = True
                return [self.getX(),self.getY()]
        
        

        #check P4
        if (self.getY()==(285)) and (self.getX()<240):
                print("touching "+str(self.getX())+" "+ str(self.getY()))
                return "BAD"
        if (self.getY()==(385)) and (self.getX()<240) and not(self.touchAlreadyP4[1]):
                print("touching "+str(self.getX())+" "+ str(self.getY()))
                self.touchAlreadyP4[1] = True
                return [self.getX(),self.getY()]

    #check to see if we reached goal state    
    def checkDone(self):
        if (self.getY()==(385)) and (self.getX()<240):
            print("touching "+str(self.getX())+" "+ str(self.getY()))
            self.touchAlreadyP1=[False,False,False,False,False]
            self.touchAlreadyP2=[False,False,False,False,False]
            self.touchAlreadyP3=[False,False]
            self.touchAlreadyP4=[True,False]
            return True
        else:
            return False

    #return current state
    def currentState(self):
        return self.stateToIndex([self.getX(), self.getY()])
    
    #return the new state
    def newState(self,action):
        result =0
        current = self.currentState()
        done = False
        
        #determine which action correlate with the value
        #then perform the action
        if action ==0:
            result = self.goStraight()
        elif action ==1:
            result = self.turnLeft()
        elif action ==2:
            result = self.turnRight() 
        elif action ==3:
            result = self.goReverse()
        
        #after the taking the action
        #update the state is current state
        new_state = [self.getX(), self.getY()]
        
        
        #determine from the action
        #what the reward
        point = self.checkPoint()
        if point is "BAD":
            reward = -100
        elif self.checkDone():
            reward = 1000
            done = True
        elif point is not None:
            #reward is higer each time it touch it
            reward = 100 + 100 * self.rewardCounter
            self.rewardCounter+=1
        elif result is None:
            reward = -1
        else:
            reward = -100
        return [self.stateToIndex(new_state), reward, done]

    #getting the center of the car points
    #which is the anchor that we used to draw
    #the sprite
    def stateToIndex(self, state):
        x = int(state[0])
        y = int(state[1])
        i = int(((x - 25) - 40)/50)
        j = int(((y - 25) - 40)/50)
        return [i,j]





            
            




        

    
