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
        self.servo=Servo()

        self.IRL = 14 # Left   (+4)
        self.IRM = 15 # Middle (+2)
        self.IRR = 23 # Right  (+1)
        # IR = [IRL, IRM, IRR] # If this doesn't work, just manually setup each
        GPIO.setmode(GPIO.BCM)
        # GPIO.setup(IR, GPIO.IN)
        GPIO.setup(self.IRL, GPIO.IN)
        GPIO.setup(self.IRM, GPIO.IN)
        GPIO.setup(self.IRR, GPIO.IN)
    def run(self):
        PWM.setMotorModel(0,0,0,0)