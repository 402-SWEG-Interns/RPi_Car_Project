# This file contains the week1 code for the Freenove Car. It utilizes the Motor.py, Line_Tracking.py, and Led.py files. As for the obstacle avoidance code, that has yet to be completed within this file*.

# *update when this is false.

# Import Library
import time
import RPi.GPIO as GPIO
from Motor import *
# from Line_Tracking import *   --- DO NOT UNCOMMENT ---
# from Led import *

GPIO.setmode(GPIO.BCM)
PWM=Motor()

# Wheels
# PWM.setMotorModel(Motor1, Motor2, Motor4, Motor3)   --- DO NOT UNCOMMENT ---
# Motor1, Motor2, Motor4, Motor3   =   Front Left, Back Left, Front Right, Back Right

# Infrared Initialization
IR01 = 14
IR02 = 15
IR03 = 23
GPIO.setup(IR01, GPIO.IN)
GPIO.setup(IR02, GPIO.IN)
GPIO.setup(IR03, GPIO.IN)


def completeTrack():
    manualIncomplete = True
    while (manualIncomplete == True):

        infrared = False
        while (infrared == False):
            try:
                move("Forward")
                print("The car is moving forward")
            except KeyboardInterrupt:
                move("Stop")
                print("\nEnd of program")

def move(direction):
    try:
        if   direction == "Forward":
            PWM.setMotorModel(2000,2000,2000,2000)
            print("Moving forward")
        elif direction == "Backward":
            PWM.setMotorModel(-2000,-2000,-2000,-2000)
            print("Moving backward")
        elif direction == "Right":
            PWM.setMotorModel(1800,1800,-1500,-1500)
            print("Turning right")
            time.sleep(0.65)
            stop()
        elif direction == "Left":
            PWM.setMotorModel(-1500,-1500,2000,2000)
            print("Turning left")
            time.sleep(0.75)
            stop()
    except KeyboardInterrupt:
        stop()
        print("\nProgram has ended")

def stop():
    PWM.setMotorModel(0,0,0,0)

def CourseV02B():

    move("Forward")
    time.sleep(1.9)
    stop()
    time.sleep(0.2)

    PWM.setMotorModel(1800,1800,-1500,-1500)
    time.sleep(0.9)
    stop()
    time.sleep(0.2)

    move("Forward")
    time.sleep(.35)
    stop()
    time.sleep(0.25)

    PWM.setMotorModel(2000,2000,-1250,-1250)
    time.sleep(0.91)
    stop()
    time.sleep(0.2)

    move("Forward")
    time.sleep(1.35)
    stop()
    time.sleep(0.2)

    PWM.setMotorModel(-1250,-1250,2000,2000)
    time.sleep(0.75)
    stop()
    time.sleep(0.2)

    move("Forward")
    time.sleep(.325)
    stop()
    time.sleep(0.2)

    PWM.setMotorModel(-1250,-1250,2000,2000)
    time.sleep(0.5)
    stop()
    time.sleep(0.2)

    move("Forward")
    time.sleep(1.325)
    stop()
    time.sleep(0.2)

    PWM.setMotorModel(-1500,-1500,2000,2000)
    time.sleep(0.2)
    stop()
    time.sleep(0.2)

    move("Forward")
    time.sleep(1.8)
    stop()
    time.sleep(0.2)

CourseV02B()