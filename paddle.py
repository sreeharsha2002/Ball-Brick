import random
from colorama import Fore
import numpy as np
import config
from gameobject import GameObject
from config import FRAMEHEIGHT,FRAMEWIDTH,PADDLEMOVE,EXPANDSIZE,POWERUPTIME,SHRINKSIZE,INCREASEBALLSPEED

class Paddle(GameObject):
    def __init__(self, x, y, xlength, ylength,xvel,yvel):
        super().__init__(x, y, xlength, ylength,xvel,yvel)
        self._type="PADDLE"
        self.score=0
        self.powerups={
            "E":[],
            "S":[],
            "M":[],
            "F":[],
            "T":[],
            "G":[],
        }


    def removePowerUp(self,ballobj):

        for i in self.powerups.keys():
            if (len(self.powerups[i])!=0):
                if self.powerups[i][0] ==0:
                    if(i=="E"):
                        self._ylength-=EXPANDSIZE
                    elif(i=="S"):
                        self._ylength+=SHRINKSIZE
                    elif(i=="F"):
                        for ball in ballobj:
                            ball._xvel-=INCREASEBALLSPEED
                            ball._yvel-=INCREASEBALLSPEED
                    if (len(self.powerups[i])==1):
                        if(i=="T"): 
                            for ball in ballobj:
                                ball.isThrough=False
                        elif(i=="G"):
                            for ball in ballobj:
                                ball.isCollidedWithPaddle=False
                    self.powerups[i].pop(0)
                else:
                    self.powerups[i][0]-=1

            
                    

    def _checkCollision(self,mul):
        if(mul==1 and self._y + self._ylength - 1 + PADDLEMOVE >= config.FRAMEWIDTH ):
            self._y=config.FRAMEWIDTH - PADDLEMOVE - self._ylength -1 
            
        elif( mul==-1 and self._y - PADDLEMOVE <= 0):
            self._y= 1 + PADDLEMOVE 
           
    def move(self,ch):
        if(ch=='d'):
            self._checkCollision(1)
            self._y+=PADDLEMOVE
        if(ch=='a'):
            self._checkCollision(-1)
            self._y-=PADDLEMOVE