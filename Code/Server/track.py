import time
from PCA9685 import PCA9685
from Motor import Motor
from line_avoidance import Line_Tracking
import RPi.GPIO as GPIO


PWM = Motor()




def movef(secs):
    seconds = time.time()


    while True:
            LMR=0x00
            if GPIO.input(14)==False:
                LMR=(LMR | 4)
            if GPIO.input(15)==False:
                LMR=(LMR | 2)
            if GPIO.input(23)==False:
                LMR=(LMR | 1)
            if LMR==7:
                PWM.setMotorModel(800,800,800,800)              
            if LMR==2:
                PWM.setMotorModel(800,800,800,800)
            elif LMR==4:
                PWM.setMotorModel(-1500,-1500,2500,2500)
            elif LMR==6:
                PWM.setMotorModel(-2000,-2000,4000,4000)
            elif LMR==1:
                PWM.setMotorModel(2500,2500,-1500,-1500)
            elif LMR==3:
                PWM.setMotorModel(4000,4000,-2000,-2000)
            elif LMR==0 or time.time()>= seconds+secs:
                PWM.setMotorModel(0,0,0,0)
                break              
    time.sleep(1)




def moveforward(secs):
    PWM.setMotorModel(1000,1000,1000,1000)       #Forward
    time.sleep(secs)
    PWM.setMotorModel(0,0,0,0)
    time.sleep(.3)


def movebackward(secs):    
    PWM.setMotorModel(-1000,-1000,-1000,-1000)   #Back
    time.sleep(secs)
    PWM.setMotorModel(0,0,0,0)
    time.sleep(.3)


def turnleft(secs):
    PWM.setMotorModel(-2000,-900,1390,1390)       #Left
    time.sleep(secs)
    PWM.setMotorModel(0,0,0,0)
    time.sleep(.3)


def turnright(secs):
    PWM.setMotorModel(1300,1300,-2000,-900)       #Right    
    time.sleep(secs)
    PWM.setMotorModel(0,0,0,0)
    time.sleep(.3)


def stop(secs):
    PWM.setMotorModel(0,0,0,0)
    time.sleep(secs)                              #Stop




#hard coded course
def course():
    moveforward(2.65)
    turnright(1)
    moveforward(.55)
    turnright(1.1)
    moveforward(2.1)
    turnleft(1)
    moveforward(.7)
    turnleft(1)
    moveforward(2.2)
    turnleft(.5)
    moveforward(2)


  #line avoidance course  
def course2():
    movef(3)
    turnright(1)
    movef(1)
    turnright(1)
    movef(3)
    turnleft(1)
    movef(1)
    turnleft(.7)
    movef(7)
   
   
#course()
course2()

