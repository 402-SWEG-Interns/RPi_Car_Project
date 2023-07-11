# 'border.py' is a line tracking file that utilizes the RPi Car's infrared sensors to keep it inside the boundaries of the ring.
from Led import *
from Motor import *
import RPi.GPIO as pin
import time

pin.setmode(pin.BCM)
M=Motor()

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

# Infrared Initialized
IRL = 14 # Left   (+4)
IRM = 15 # Middle (+2)
IRR = 23 # Right  (+1)
IR = [IRL, IRM, IRR] # If this doesn't work, just manually setup each
pin.setup(IR, pin.IN)

# Booleans
# Sensors
Ls = False
Ms = False
Rs = False
# Inside/Outside
io = False # Inside = False ; Outside = True





# boundary(): --- Detects if the car reaches a line (i.e. the edge of the ring), then returns the car to the ring
def boundary():   # currently a sync function; code is experimental and has yet to be tested
    M.setMotorModel(0,0,0,0)    # Stops the motor






    detection = True
    """
    Sensors | Truth | Sum | Action
    lmr     | 000   |  0  | nul
    lmR     | 001   |  1  | Turn Left - 45
    lMr     | 010   |  2  | U-Turn - 180
    lMR     | 011   |  3  | Turn Left - 90
    Lmr     | 100   |  4  | Turn Right - 45
    LmR     | 101   |  5  | U-Turn - 180
    LMr     | 110   |  6  | Turn Right - 90
    LMR     | 111   |  7  | U-Turn - 180
    """

    while detection:
        LMR=0x00 # Detects Black
        if pin.input(IRR)==io: # Right Sensor
            LMR=(LMR | 1)
            Rs = True
        else:
            Rs = False
        if pin.input(IRM)==io: # Middle Sensor
            LMR=(LMR | 2)
            Ms = True
        else:
            Ms = False
        if pin.input(IRL)==io: # Left Sensor
            LMR=(LMR | 4)
            Ls = True
        else:
            Ls = False
        




        # Boundary on Left
        # Boundary in Front
        # Boundary on Right





# stop(): --- Sets power output to 0 for each motor
def stop():   
    M.setMotorModel(0,0,0,0)   # Provides a value of 0 power to all motors