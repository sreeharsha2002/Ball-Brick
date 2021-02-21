import random
from colorama import Fore
import numpy as np
import config

class GameObject:
    def __init__(self,x,y,xlength,ylength,xvel,yvel):
        self._x=x
        self._y=y
        self._xlength=xlength
        self._ylength=ylength
        self._xvel=xvel
        self._yvel=yvel
        self._type='NONE'
    def draw(self):
        if(self._type=='BALL'):
            obj=np.full([self._xlength,self._ylength],('O'))
            return obj
        elif(self._type=='PADDLE'):
            obj=np.full([self._xlength,self._ylength],(' '))
            for i in range(0,self._xlength):
                for j in range(0,self._ylength):
                    obj[i][j]='/'
                    if(j==0):
                        obj[i][j]='('
                    elif(j==self._ylength-1):
                        obj[i][j]=')'
            return obj
        elif(self._type=='BRICK'):
            obj=np.full([self._xlength,self._ylength],('X'))
            for i in range(0,self._xlength):
                for j in range(0,self._ylength):
                    if(i==0 or i== self._xlength-1):
                        obj[i][j]='-'
                    elif(j==0 or j== self._ylength-1):
                        obj[i][j]='|'

            return obj
        else:
            obj=np.full([self._xlength,self._ylength],(self._type))
            return obj
            
    def retcoorlength(self):
        return{
            "coor": [self._x, self._y],
            "length": [self._xlength, self._ylength]
        }

    
    def move(self):
        self._y+=self._yvel
        self._x+=self._xvel