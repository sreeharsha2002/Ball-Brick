import random
from colorama import init as coloramaInit, Fore, Style,Back
import time

def fn(arr,i):
    if(i==0):
        return
    arr.append(i)
    fn(arr,i-1)
arr=[]
fn(arr,4)
print(arr)