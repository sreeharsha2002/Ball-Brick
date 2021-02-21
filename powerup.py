import random
from colorama import Fore
import numpy as np
import config
from gameobject import GameObject
from ball import Ball
from config import FRAMEHEIGHT,FRAMEWIDTH,PADDLEMOVE,EXPANDSIZE,SHRINKSIZE,INCREASEBALLSPEED,POWERUPTIME

class PowerUp(GameObject):
    def __init__(self, x, y, xlength, ylength,xvel,yvel,ptype):
        super().__init__(x, y, xlength, ylength,xvel,yvel)
        self._type=ptype
        self.isCollided=False

    def _checkCollision(self,paddleobj,ballobj):
        if(self._x+self._xvel>=paddleobj._x and 
        paddleobj._y<=self._y<paddleobj._y+paddleobj._ylength):
            self._x=paddleobj._x-1-self._xvel
            print(self._type,self._x,self._y)
            if(self._type=="E"):
                paddleobj.powerups[self._type].append(POWERUPTIME)
                paddleobj._ylength+=EXPANDSIZE
            elif(self._type=="S"):
                paddleobj.powerups[self._type].append(POWERUPTIME)
                if(paddleobj._ylength!=3):
                    paddleobj._ylength-=SHRINKSIZE
            elif(self._type=="M"):
                newballs=[]
                for ball in ballobj:
                    nball=Ball(ball._x,ball._y,ball._xlength,ball._ylength,
                    -1*ball._xvel,-1*ball._yvel)
                    nball.isCollidedWithPaddle=False
                    newballs.append(nball)
                for i in newballs:
                    ballobj.append(i)
                paddleobj.powerups[self._type].append(-1)
            elif(self._type=="F"):
                paddleobj.powerups[self._type].append(POWERUPTIME)
                for ball in ballobj:
                    ball._xvel+=INCREASEBALLSPEED
                    ball._yvel+=INCREASEBALLSPEED
            elif(self._type=="T"):
                paddleobj.powerups[self._type].append(POWERUPTIME)
                for ball in ballobj:
                    ball.isThrough=True
            elif(self._type=="G"):
                paddleobj.powerups[self._type].append(POWERUPTIME)

            self.isCollided=True 
        if(self._x + self._xvel >= config.FRAMEHEIGHT):
            self._x=0
            self.isCollided =True
    def setVel(self):
        self._xvel=2
           
    def move(self,paddleobj,ballobj):
        self._checkCollision(paddleobj,ballobj)
        self._x+=self._xvel