# This file contains the pathfinding code that utilizes both the Motor.py and the Line_Tracking.py files
import time
import RPi.GPIO as GPIO
from Motor import *
from Line_Tracking import *
from Led import *

PWM=Motor()
infrared=Line_Tracking()

# Wheels
try:
    PWM.setMotorModel(1000,0,0,0)
    time.sleep(1)
    PWM.setMotorModel(0,1000,0,0)
    time.sleep(1)
    PWM.setMotorModel(0,0,1000,0)
    time.sleep(1)
    PWM.setMotorModel(0,0,0,1000)
    time.sleep(1)
    PWM.setMotorModel(0,0,0,0)
except KeyboardInterrupt:
    PWM.setMotorModel(0,0,0,0)
    Print("Program ended")

# def completeTrack():
#     incomplete = True
#     while (incomplete):
#         """URGENT
#         Insert Async Coding? Or create three while loops: the outermost for the track completion, the middlemost for checking Infrared status, and the innermost for determining car action based on Infrared status."""
#         while infra == False:
#             try:
#                 move("Forward")
#                 print("The car is moving forward")
#             except KeyboardInterrupt:
#                 move("Stop")
#                 print("\nEnd of program")

# def move(direction):
#     if direction == "Forward":
#         PWM.setMotorModel(1000,1000,1000,1000)
#     elif direction == "Backward":
#         PWM.setMotorModel(-1000,-1000,-1000,-1000)
#     elif direction == "Left":
#         PWM.setMotorModel(-1500,-1500,2000,2000)
#         time.sleep(1)
#         PWM.setMotorModel(0,0,0,0)
#     elif direction == "Right":
#         PWM.setMotorModel(2000,2000,-1500,-1500)
#         time.sleep(1)
#         PWM.setMotorModel(0,0,0,0)
#     elif direction == "Stop":
#         PWM.setMotorModel(0,0,0,0)
