import os
import random
import math
import time
import numpy as np
from colorama import init as coloramaInit, Fore, Style,Back
from terminalfns import clearScreen
from config import FRAMEHEIGHT,FRAMEWIDTH,POWERUPS
from ball import Ball
from paddle import Paddle
from brick import Brick
from powerup import PowerUp
from input import Get,input_to
class RenderGame():
    def __init__(self):
        coloramaInit()
        clearScreen()
        self.__gameobjects=[]
        self.__colorArray=np.full([FRAMEHEIGHT,FRAMEWIDTH],(Fore.WHITE + Back.BLACK))
        self.__arr=np.full([FRAMEHEIGHT, FRAMEWIDTH], (' '))
        self.__arr[::,0]='|'
        self.__arr[::,-1]='|'
        self.__arr[0,::]='-'
        self.__arr[-1,::]='-'
        self._starttime=time.time()
        self.lasttime=time.time()
        self.lives=3
        self._loopGame()

    def scores(self,paddleobj):
        padding = ' '*10
        str1=f"Score:{paddleobj[0].score}{padding}\n"
        str1+=f"Lives Remaining:{self.lives}{padding}\n"
        str1+=f"Time : {int((time.time()-self._starttime)*1000)} seconds{padding}\n"    
        os.write(1,str.encode(str1))
        
    def printToArray(self,coorlength,obj):
        from_x = int(coorlength["coor"][0])
        to_x = from_x + coorlength["length"][0] - 1

        from_y = int(coorlength["coor"][1])
        to_y = from_y + coorlength["length"][1] - 1

        self.__arr[from_x:to_x + 1,from_y: to_y + 1] = obj.draw()
        if(obj._type=='BRICK'):
            self.__colorArray[from_x:to_x + 1,from_y: to_y + 1]=obj.colorBrick()

    def _printGame(self):
        #self.scores(self.__gameobjects)
        for items in self.__gameobjects:
            for item in items:
                coorlength=item.retcoorlength()
                self.printToArray(coorlength,item)
        st=""
        for i in range(0,FRAMEHEIGHT):
            
            for j in range(0,FRAMEWIDTH):
                st+=self.__colorArray[i][j]+self.__arr[i][j]
            st+='\n'
        os.write(1,str.encode(st))


    def _resetArray(self):
        self.__arr=np.full([FRAMEHEIGHT, FRAMEWIDTH], (' '))
        self.__arr[::,0]='|'
        self.__arr[::,-1]='|'
        self.__arr[0,::]='-'
        self.__arr[-1,::]='-'
        self.__colorArray=np.full([FRAMEHEIGHT,FRAMEWIDTH],(Fore.WHITE + Back.BLACK))

    def _update(self,ballobj,paddleobj,ch,brickobj,powerupobj):
        self.__gameobjects=[]
        self.__gameobjects.append(brickobj)
        self.__gameobjects.append(ballobj)
        self.__gameobjects.append(paddleobj)
        self.__gameobjects.append(powerupobj)
        
        self._resetArray()
        pblength=[]
        for i in ballobj:
            pblength.append(i._y-paddleobj[0]._y)

        paddleobj[0].move(ch)
        for iti in range(len(ballobj)):
            # print(ballobj[iti].isCollidedWithPaddle)
            if(ballobj[iti].isCollidedWithPaddle):
                ballobj[iti].attach(paddleobj[0],pblength[iti])  
        if(1000*(time.time()-self.lasttime)>=100):
            for iti in range(len(ballobj)):   
                if not(ballobj[iti].isCollidedWithPaddle):
                    ballobj[iti].move(paddleobj[0],brickobj)
            for iti in powerupobj:
                if(iti._xvel==2):
                    iti.move(paddleobj[0],ballobj)   
            paddleobj[0].removePowerUp(ballobj)  
            self.lasttime=time.time()
        


    
    def checkPowerupIsCollided(self,powerupobj):
        rIndex=[]
        for i in powerupobj:
            if(i.isCollided==True):
                rIndex.append(i)
        for i in rIndex:
            powerupobj.remove(i)

    def fillBricks(self):
        array=[]
        array2=[]
        a=0
        for i in range(0,18,3):
            for j in range(0,144,8):
                stren=random.randint(1,5)
                hl=int(j/8)
                if(hl==a or hl== a+1 or hl==17-a or hl==17-a-1) and int(i/3)!=5:
                    stren=6
                array.append(Brick(9+i,30+j,3,8,0,0,stren))

                if (stren==3 or stren==4):
                    array2.append(PowerUp(9+i,30+j,1,1,0,0,random.choice(POWERUPS)))
            a+=2
        return array,array2


    def checkBricks(self,brickobj,powerupobj):
        rIndex=[]
        for i in brickobj:
            if(i.strength==0):
                for iti in powerupobj:
                    if(iti._x==i._x and iti._y==i._y):
                        iti.setVel()
                rIndex.append(i)
        for i in rIndex:
            brickobj.remove(i)
        
    def checkBall(self,ballobj,paddleobj):
        rIndex=[]
        for i in ballobj:
            if(i._xvel==0 and i._yvel==0):
                rIndex.append(i)
        for i in rIndex:
            ballobj.remove(i)
            if(len(ballobj)==0):
                self.lives-=1
               # print(paddleobj[0]._y)
                ballobj.append(Ball(FRAMEHEIGHT-3,paddleobj[0]._y+int(paddleobj[0]._ylength/2)
                ,1,1,-2,2))
    def status(self,brickobj,paddleobj):
        if(self.lives==0):
            return 0
        flag=0
        for i in brickobj:
            if(i.strength!=5):
                flag=1
            else:
                if(len(paddleobj[0].powerups["T"])!=0):
                    flag=1                
        return flag        
    def _loopGame(self):
        paddleobj= []
        paddleobj.append(Paddle(FRAMEHEIGHT-2,int(FRAMEWIDTH/2),1,7,0,0))
        ballobj=[]
        ballobj.append(Ball(FRAMEHEIGHT-3,paddleobj[0]._y+int(paddleobj[0]._ylength/2),1,1,-2,2))
        brickobj=[]
        powerupobj=[]
        brickobj,powerupobj=self.fillBricks()
        flag=0
        while (self.status(brickobj,paddleobj)):
            getch=Get()
            ch=input_to(getch,0.1)
            if ch=='e':
                flag=1
                break
            if(ch=='f'):
                for i in ballobj:
                    i.isCollidedWithPaddle=False
            print("\033[0;0H")
            
            self._update(ballobj,paddleobj,ch,brickobj,powerupobj)
            self.checkBricks(brickobj,powerupobj)
            self.checkBall(ballobj,paddleobj)
            self.checkPowerupIsCollided(powerupobj)
            self.scores(paddleobj)
            self._printGame()
        if flag:
            print("You Exited")
            print(f"With Score {paddleobj[0].score}")
        else:
            if(self.lives==0):
                print("You Lost")
                print(f"With Score {paddleobj[0].score}")
            else:
                print("You Won")
                print(f"With Score {paddleobj[0].score}")
            



