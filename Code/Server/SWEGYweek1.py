# This file contains the week1 code for the Freenove Car. It utilizes the Motor.py, Line_Tracking.py, and Led.py files. As for the obstacle avoidance code, that has yet to be completed within this file*.

# *update when this is false.

# Import Library
import time
import RPi.GPIO as GPIO
from Motor import *
from Line_Tracking import *
# from Led import *

PWM=Motor()
IR=Line_Tracking()

# Wheels
# PWM.setMotorModel(Motor1, Motor2, Motor4, Motor3)   --- DO NOT UNCOMMENT ---
# Motor1, Motor2, Motor4, Motor3   =   Front Left, Back Left, Front Right, Back Right

def completeTrack():
    manualIncomplete = True
    while (manualIncomplete == True):
        """URGENT
        Insert Async Coding? Or create three while loops: the outermost for the track completion, the middlemost for checking Infrared status, and the innermost for determining car action based on Infrared status.
        VERDICT
        Three While Loops"""

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
            time.sleep(5)
            stop()
        elif direction == "Backward":
            PWM.setMotorModel(-2000,-2000,-2000,-2000)
            print("Moving backward")
            time.sleep(5)
            stop()
        elif direction == "Right":
            PWM.setMotorModel(2000,2000,-2000,-2000)
            print("Turning right")
            time.sleep(0.75)
            stop()
        elif direction == "Left":
            PWM.setMotorModel(-2000,-2000,2000,2000)
            print("Turning left")
            time.sleep(0.75)
            stop()
    except KeyboardInterrupt:
        stop()
        print("\nProgram has ended")

def stop():
    PWM.setMotorModel(0,0,0,0)