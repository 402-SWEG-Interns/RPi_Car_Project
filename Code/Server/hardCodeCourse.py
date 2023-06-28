from Motor import *
import sys
import time

PWM=Motor()

# IR01 = Left
# IR02 = Middle
# IR03 = Right


def moveForward(t=int):
    PWM.setMotorModel(1500, 1500, 750, 750)
    time.sleep(t)
    PWM.setMotorModel(0, 0, 0, 0)

def turnRight(t=int):
    PWM.setMotorModel(2000,2000,-1500,-1500)
    time.sleep(t)
    PWM.setMotorModel(0, 0, 0, 0)

def turnLeft(t=int):
    PWM.setMotorModel(-1500,-1500,2000,2000)
    time.sleep(t)
    PWM.setMotorModel(0, 0, 0, 0)

def moveBackward(t=int): 
    PWM.setMotorModel(-1000, -1000, -1000, -1000)
    time.sleep(t)
    PWM.setMotorModel(0, 0, 0, 0)

def courseRuner():
    try:
        moveForward(2.1)
        turnRight(0.92)
        moveForward(0.4)
        turnRight(0.875)
        moveForward(2)
        turnLeft(0.6)
        moveForward(3)
        turnLeft(0.1)
        moveForward(3)
    except KeyboardInterrupt:
        print(" Ended")
    except(Exception) as e:
        print(e)
    finally:
        PWM.setMotorModel(0, 0, 0, 0)

courseRuner()