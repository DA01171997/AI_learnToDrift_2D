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
    def draw(self):
        self.carSprite.draw()
        Line(self.getX()-25,self.getY()-25,self.getX()+25,self.getY()-25,[0,0,0],1).draw()
        Line(self.getX()-25,self.getY()+25,self.getX()+25,self.getY()+25,[0,0,0],1).draw()

        Line(self.getX()-25,self.getY()-25,self.getX()-25,self.getY()+25,[0,0,0],1).draw()
        Line(self.getX()+25,self.getY()-25,self.getX()+25,self.getY()+25,[0,0,0],1).draw()
        
        #checkpointP1
        for x in range(0,4):
            Line(265 + x *200,60,265 +x *200,260,[0,0,0],1).draw()
        Line(965,60,965,260,[0,0,0],1).draw()
        
        #checkpointP2
        for x in range(0,4):
            Line(265 + x *200,460,265 +x *200,660,[0,0,0],1).draw()
        Line(965,460,965,660,[0,0,0],1).draw()

        #checkpointP3
        Line(1040,285,1240,285,[0,0,0],1).draw()
        #checkpointP32
        Line(1040,385,1240,385,[0,0,0],1).draw()

        #checkpointP4
        Line(40,285,240,285,[1,0,0],1).draw()
        #checkpointP4
        Line(40,385,240,385,[0,1,0],1).draw()


    
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
    def updateDeltaX(self, value):
        self.deltaX = value
    def updateDeltaY(self, value):
        self.deltaY = value

    def turnLeft(self):
        self.updateTheta(-self.rotation_speed)
        value = self.goStraight()
        if  value != None:
            self.updateTheta(self.rotation_speed)
        return value
    def turnRight(self):
        self.updateTheta(self.rotation_speed)
        value = self.goStraight()
        if  value != None:
            self.updateTheta(-self.rotation_speed)
        return value
    def goStraight(self):
        value = self.getX() + self.speed
        thetaRadian = -math.radians(self.getTheta())
        deltaX = int(math.cos(thetaRadian) * self.speed) 
        deltaY = int(math.sin(thetaRadian) * self.speed) 
        if (((self.getX() + deltaX) <= 1240) and ((self.getX() + deltaX) >= 40)) and (((self.getY() + deltaY) <= 660) and ((self.getY() + deltaY) >= 60)):
            if ((self.getX() >=40 and self.getX() <= 240) and (self.getY() >=260) and self.getY()<=460) and (self.getX() + deltaX >240):
                return 240
            elif ((self.getX() >=1040 and self.getX() <= 1240) and (self.getY() >=260) and self.getY()<=460) and (self.getX() + deltaX <1040):
                return 1040
            elif ((self.getX() >=240 and self.getX() < 1040) and (self.getY() >=60) and self.getY()<=260) and (self.getY() + deltaY >260):
                return 260
            elif ((self.getX() >=240 and self.getX() < 1040) and (self.getY() >=460) and self.getY()<=660) and (self.getY() + deltaY <460):
                return 460
            else:
                self.updateX(deltaX)
                self.updateY(deltaY)
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
    
    
    def goReverse(self):
        value = self.getX() - self.speed
        thetaRadian = -math.radians(self.getTheta())
        deltaX = int(math.cos(thetaRadian) * self.speed )
        deltaY = int(math.sin(thetaRadian) * self.speed)
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
    
    def checkPoint(self):
        #check P1
        for x in range(0,4):
            if (self.getX()==(265 + x*200)) and (self.getY()<260) and not(self.touchAlreadyP1[x]):
                print("touching "+str(self.getX())+" "+ str(self.getY()))
                self.touchAlreadyP1[x] = True
                return [self.getX(),self.getY()]
        if (self.getX()==(965)) and (self.getY()<260) and not(self.touchAlreadyP1[4]):
                print("touching "+str(self.getX())+" "+ str(self.getY()))
                self.touchAlreadyP1[4] = True
                return [self.getX(),self.getY()]
        #check P3
        if self.touchAlreadyP1[4] == True:
            if (self.getY()==(285)) and (self.getX()>=1040) and not(self.touchAlreadyP3[0]):
                    print("touching "+str(self.getX())+" "+ str(self.getY()))
                    self.touchAlreadyP3[0] = True
                    return [self.getX(),self.getY()]
            if (self.getY()==(385)) and (self.getX()>=1040) and not(self.touchAlreadyP3[1]):
                    print("touching "+str(self.getX())+" "+ str(self.getY()))
                    self.touchAlreadyP3[1] = True
                    return [self.getX(),self.getY()]
        
        
        
        #check P2
        if self.touchAlreadyP3[1] == True:
            for x in range(0,4):
                if (self.getX()==(265 + x*200)) and (self.getY()>=260) and not(self.touchAlreadyP2[x]):
                    print("touching "+str(self.getX())+" "+ str(self.getY()))
                    self.touchAlreadyP2[x] = True
                    return [self.getX(),self.getY()]
            if (self.getX()==(965)) and (self.getY()>=260) and not(self.touchAlreadyP2[4]):
                    print("touching "+str(self.getX())+" "+ str(self.getY()))
                    self.touchAlreadyP2[4] = True
                    return [self.getX(),self.getY()]
        
        
        if self.touchAlreadyP2[4] == True:
            #check P4
            if (self.getY()==(285)) and (self.getX()<240):
                    print("touching "+str(self.getX())+" "+ str(self.getY()))

                    return "BAD"
            if (self.getY()==(385)) and (self.getX()<240) and not(self.touchAlreadyP4[1]):
                    print("touching "+str(self.getX())+" "+ str(self.getY()))
                    self.touchAlreadyP4[1] = True
                    return [self.getX(),self.getY()]
        
    def checkDone(self):
        for x in range(0,4):
            if not(self.touchAlreadyP1[x]) or not(self.touchAlreadyP2[x]):
                return False
        for x in range(0,2):
            if not(self.touchAlreadyP3[x]) or not(self.touchAlreadyP4[x]):
                return False
        return True
    def currentState(self):
        return self.stateToIndex([self.getX(), self.getY()])
    def newState(self,action):
        current = self.currentState()
        done = False
        if action ==0:
            result = self.goStraight()
        elif action ==1:
            result = self.turnLeft()
        elif action ==2:
            result = self.turnRight() 
        new_state = [self.getX(), self.getY()]
        point = self.checkPoint()
        if point is "BAD":
            reward = -1000
        elif point is not None:
            reward = 100
        elif self.checkDone():
            reward = 1000
            done = True
        elif result is None:
            reward = -1
        else:
            reward = -100
        return [self.stateToIndex(new_state), reward, done]


    def stateToIndex(self, state):
        x = int(state[0])
        y = int(state[1])
        i = int(((x - 25) - 40)/50)
        j = int(((y - 25) - 40)/50)
        return [i,j]





            
            




        

    
