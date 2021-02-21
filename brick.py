import random
from colorama import Fore,Back
import numpy as np
import config
from gameobject import GameObject
class Brick(GameObject):
    def __init__(self, x, y, xlength, ylength,xvel,yvel,strength):
        super().__init__(x, y, xlength, ylength,xvel,yvel)
        self.strength=strength
        self._type="BRICK"
        self.isDestroyed=False
        self.togglecolor=False
        self.isVisited=False
    def strengthColor(self):
        if(self.strength==1):
            return Back.GREEN
        elif(self.strength==2):
            return Back.YELLOW
        elif(self.strength==3):
            return Back.BLUE
        elif(self.strength==4):
            return Back.MAGENTA
        elif(self.strength==5):
            return Back.RED
        elif(self.strength==6):
            if(self.togglecolor):
                self.togglecolor=not(self.togglecolor)
                return Back.CYAN
            else:
                self.togglecolor=not(self.togglecolor)
                return Back.WHITE
        elif(self.strength==0):
            return Back.WHITE
    def colorBrick(self):
        obj=np.full([self._xlength,self._ylength],(self.strengthColor() + Fore.BLACK))
        return obj