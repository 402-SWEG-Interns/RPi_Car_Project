# Imports
import time
import RPi.GPIO as pin
from Motor import *
# from Line_Tracking import *   --- DO NOT UNCOMMENT ---
from Led import *

pin.setmode(pin.BCM)
PWM=Motor()

"""
Wheels
Legend:
  M - Motor
  F - Front
  B - Back
  L - Left
  R - Right
PWM.setMotorModel(M1, M2, M4, M3)
M1, M2, M4, M3   =   FL, BL, FR, BR
"""

# Infrared Initialized
IR01 = 14 # Left
IR02 = 15 # Middle
IR03 = 23 # Right
IR = [IR01, IR02, IR03] # If this doesn't work, just manually setup each
pin.setup(IR, pin.IN)



# Functions
# main() --- Where the actual program occurs
def main():
    # v0.3
    print('Function: main()\nStatus:   active')
    
    try:
        print('\nplaceholder')
        PWM.setMotorModel(500,500,500,500)
        while True:
            LMR=0x00 # Detects Black
            if pin.input(IR01)==False: # Left Sensor
                LMR=(LMR | 4)
            if pin.input(IR02)==False: # Middle Sensor
                LMR=(LMR | 2)
            if pin.input(IR03)==False: # Right Sensor
                LMR=(LMR | 1)
            








            
            # Booleans
            Ls   = False
            Ms   = False
            Rs   = False
            LMs  = False
            MRs  = False
            LRs  = False # If somehow Left and Right are triggered, but no Middle
            LMRs = False
            NULs = False # No Sensors
            sensors = [Ls, Ms, Rs, LMs, MRs, LRs, LMRs, NULs]









            
            # Action
            # Start
            if   LMR==0: # No Sensors
                if NULs == False:
                    print('No Sensors Detected\nDriving Forward: Fast')
                    for s in sensors:
                        s = False
                    NULs = True
            elif LMR==5: # Left + Right Sensors
                if LRs == False:
                    print('Left + Right Sensors Detected\nDriving Forward: Slow')
                    for s in sensors:
                        s = False
                    LRs = True



            # Turn Right
            elif LMR==4: # Left Sensor
                if Ls == False:
                    print('Left Sensor Detected\nTurning Right: Soft')
                    for s in sensors:
                        s = False
                    Ls = True
            elif LMR==6: # Left + Middle Sensors
                if LMs == False:
                    print('Left + Middle Sensor Detected\nTurning Right: Hard')
                    for s in sensors:
                        s = False
                    LMs = True



            # Stop
            elif LMR==7: # All Sensors
                if LMRs == False:
                    print('All Sensors Detected\nStopping Car')
                    for s in sensors:
                        s = False
                    LMRs = True
                    # PWM.setMotorModel(0,0,0,0)
            elif LMR==2: # Middle Sensor
                if Ms == False:
                    print('Middle Sensor Detected\nStopping Car')
                    for s in sensors:
                        s = False
                    Ms = True
                    # PWM.setMotorModel(0,0,0,0)



            # Turn Left
            elif LMR==3: # Middle + Right Sensors
                if MRs == False:
                    print('Middle + Right Sensor Detected\nTurning Left: Hard')
                    for s in sensors:
                        s = False
                    MRs = True
            elif LMR==1: # Right Sensor
                if Rs == False:
                    print('Right Sensor Detected\nTurning Left: Soft')
                    for s in sensors:
                        s = False
                    Rs = True


    except KeyboardInterrupt:   # Ctrl+C
        print('Function: main()\nStatus:   inactive')
        PWM.setMotorModel(0,0,0,0)

# test() --- Where test code occurs before it is decided whether it is used in main() or not
def test():
    # v0.3 Test
    print('Function: test()\nStatus:   active')

    try:
        print('\nplaceholder')
    except KeyboardInterrupt:   # Ctrl+C
        print('Function: test()\nStatus:   inactive')
        PWM.setMotorModel(0,0,0,0)



# 



# Function Calls --- Comment out whichever functions you do not intend to use before running the code
main()
# test()