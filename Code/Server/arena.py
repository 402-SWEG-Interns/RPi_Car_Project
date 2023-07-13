# from ADC import *
# from Buzzer import *
# from Command import COMMAND as cmd
# import fcntl
# import io
# from Led import *
# from Light import *
# from Line_Tracking import *
from Motor import *
from PCA9685 import * # Is this one needed?
# import picamera
import RPi.GPIO as GPIO
from servo import *
# import socket
# import struct
# import sys
# from Thread import *
# import threading
# from threading import Condition
# from threading import Timer
# from threading import Thread
import time





class Arena:
    def __init__(self):
        # self.buzzer=Buzzer()
        # self.infrared=Line_Tracking()
        # self.led=Led()
        self.motor=Motor()
        """
        Motor Legend:
            M - Motor
            F - Front
            B - Back
            L - Left
            R - Right
        PWM.setMotorModel(M1, M2, M4, M3)
        M1, M2, M4, M3   =   FL, BL, FR, BR
        """

        self.servo=Servo()

        self.io = False # Inside = False ; Outside = True
        self.Ls = False
        self.Ms = False
        self.Rs = False
        self.red    = False
        self.green  = False
        self.blue   = False
        self.yellow = False

        self.IRL = 14 # Left   (+4)
        self.IRM = 15 # Middle (+2)
        self.IRR = 23 # Right  (+1)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IRL, GPIO.IN)
        GPIO.setup(self.IRM, GPIO.IN)
        GPIO.setup(self.IRR, GPIO.IN)
    def run(self):
        self.motor.setMotorModel(0,0,0,0)
        
        moving = True # 'tracking' can be renamed to 'patrol'; either way, this is supposed to prevent the car from leaving the arena; this boolean is 'moving' for when the patrolling occurs
        while moving:
            """
            Sensors | Truth | Sum | Action
            lmr     | 000   |  0  | nul
            lmR     | 001   |  1  | Turn Left - Soft
            lMr     | 010   |  2  | U-Turn
            lMR     | 011   |  3  | Turn Left - Hard
            Lmr     | 100   |  4  | Turn Right - Soft
            LmR     | 101   |  5  | U-Turn
            LMr     | 110   |  6  | Turn Right - Hard
            LMR     | 111   |  7  | U-Turn
            """
            LMR=0x00 # Detects Black
            if GPIO.input(self.IRR)==self.io: # Right Sensor
                LMR=(LMR | 1)
            #     Rs = True
            # else:
            #     Rs = False
            if GPIO.input(self.IRM)==self.io: # Middle Sensor
                LMR=(LMR | 2)
            #     Ms = True
            # else:
            #     Ms = False
            if GPIO.input(self.IRL)==self.io: # Left Sensor
                LMR=(LMR | 4)
            #     Ls = True
            # else:
            #     Ls = False

            if   LMR==0: # nul
                pass
            elif LMR==4: # Turn Right - Soft
                self.motor.setMotorModel(0,0,0,0)
                time.sleep(1)
                self.motor.setMotorModel(1500,1500,-1500,-1500)
                time.sleep(0.5)
                self.motor.setMotorModel(0,0,0,0)

                moving = False
            elif LMR==6: # Turn Right - Hard
                self.motor.setMotorModel(0,0,0,0)
                time.sleep(1)
                self.motor.setMotorModel(1500,1500,-1500,-1500)
                time.sleep(1)
                self.motor.setMotorModel(0,0,0,0)

                moving = False
            elif LMR==2 or LMR==5 or LMR==7: # U-Turn
                self.motor.setMotorModel(0,0,0,0)
                time.sleep(1)
                self.motor.setMotorModel(-1500,-1500,-1500,-1500)
                time.sleep(1)
                self.motor.setMotorModel(0,0,0,0)
                time.sleep(1)
                self.motor.setMotorModel(1500,1500,-1500,-1500)
                time.sleep(2)
                self.motor.setMotorModel(0,0,0,0)

                moving = False
            elif LMR==3: # Turn Left - Hard
                self.motor.setMotorModel(0,0,0,0)
                time.sleep(1)
                self.motor.setMotorModel(-1500,-1500,1500,1500)
                time.sleep(1)
                self.motor.setMotorModel(0,0,0,0)

                moving = False
            elif LMR==1: # Turn Left - Soft
                self.motor.setMotorModel(0,0,0,0)
                time.sleep(1)
                self.motor.setMotorModel(-1500,-1500,1500,1500)
                time.sleep(0.5)
                self.motor.setMotorModel(0,0,0,0)

                moving = False
            
            print('placeholder')

arena=Arena()
# Main program logic follows
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        arena.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)