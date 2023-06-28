import time
from PCA9685 import PCA9685
from Motor import Motor

PWM = Motor() 

def moveforward(secs):
    PWM.setMotorModel(1000,1000,1000,1000)       #Forward
    time.sleep(secs)

def movebackward(secs):    
    PWM.setMotorModel(-1000,-1000,-1000,-1000)   #Back
    time.sleep(secs)

def turnleft(secs):
    PWM.setMotorModel(-750,-750,2000,2000)       #Left 
    time.sleep(secs)

def turnright(secs):
    PWM.setMotorModel(2000,2000,-1000,-1000)       #Right    
    time.sleep(secs)

def stop(secs):
    PWM.setMotorModel(0,0,0,0)
    time.sleep(secs)                              #Stop

#Actual Code
def main():
    moveforward(2.45)
    stop(.5)
    turnright(.8)
    stop(.3)
    moveforward(.34)
    stop(.3)
    turnright(1)
    stop(.3)
    moveforward(1.9)
    stop(.3)
    turnleft(1.85)
    stop(.3)
    moveforward(2)
    stop(.3)
    turnleft(.4)
    stop(.3)
    moveforward(2)
    stop(.3)

    #turnright(2.22)
    #stop(1)


main()