# Imports
import time
import RPi.GPIO as pin
from Motor import *
# from Line_Tracking import *   --- DO NOT UNCOMMENT ---
# from Led import *

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
        # Hard Reset On The Motors
        PWM.setMotorModel(0,0,0,0)



        # Variables
        # Booleans
        Ls   = False
        Ms   = False
        Rs   = False
        LMs  = False
        MRs  = False
        LRs  = False # If somehow Left and Right are triggered, but no Middle
        LMRs = False
        NULs = False # No Sensors
        # Speeds
        fS = 600
        fF = 800
        tS = -700
        tF = -900
        # Inside/Outside
        io = True # Inside = False ; Outside = True
        # Counter
        tick = 0





        while True:
            LMR=0x00 # Detects Black
            if pin.input(IR01)==io: # Left Sensor
                LMR=(LMR | 4)
            if pin.input(IR02)==io: # Middle Sensor
                LMR=(LMR | 2)
            if pin.input(IR03)==io: # Right Sensor
                LMR=(LMR | 1)




            
            # Action
            # Start
            if   LMR==0: # No Sensors
                if NULs == False:
                    print('\nNo Sensors Detected\nDriving Forward: Fast')
                    Ls   = False
                    Ms   = False
                    Rs   = False
                    LMs  = False
                    MRs  = False
                    LRs  = False
                    LMRs = False
                    NULs = True
                    PWM.setMotorModel(fF,fF,fF,fF)
            elif LMR==5: # Left + Right Sensors
                if LRs == False:
                    print('\nLeft + Right Sensors Detected\nDriving Forward: Slow')
                    Ls   = False
                    Ms   = False
                    Rs   = False
                    LMs  = False
                    MRs  = False
                    LRs  = True
                    LMRs = False
                    NULs = False
                    PWM.setMotorModel(fS,fS,fS,fS)



            # Turn Right
            elif LMR==4: # Left Sensor
                if Ls == False:
                    print('\nLeft Sensor Detected\nTurning Right: Soft')
                    Ls   = True
                    Ms   = False
                    Rs   = False
                    LMs  = False
                    MRs  = False
                    LRs  = False
                    LMRs = False
                    NULs = False
                    PWM.setMotorModel(fF,fF,tS,tS)
            elif LMR==6: # Left + Middle Sensors
                if LMs == False:
                    print('\nLeft + Middle Sensor Detected\nTurning Right: Hard')
                    Ls   = False
                    Ms   = False
                    Rs   = False
                    LMs  = True
                    MRs  = False
                    LRs  = False
                    LMRs = False
                    NULs = False
                    PWM.setMotorModel(fF,fF,tF,tF)



            # Stop
            elif LMR==7: # All Sensors
                if LMRs == False:
                    print('\nAll Sensors Detected\nStopping Car')
                    Ls   = False
                    Ms   = False
                    Rs   = False
                    LMs  = False
                    MRs  = False
                    LRs  = False
                    LMRs = True
                    NULs = False
                    PWM.setMotorModel(0,0,0,0)
                    hardcode(tick)
            elif LMR==2: # Middle Sensor
                if Ms == False:
                    print('\nMiddle Sensor Detected\nStopping Car')
                    Ls   = False
                    Ms   = True
                    Rs   = False
                    LMs  = False
                    MRs  = False
                    LRs  = False
                    LMRs = False
                    NULs = False
                    PWM.setMotorModel(0,0,0,0)
                    hardcode(tick)



            # Turn Left
            elif LMR==3: # Middle + Right Sensors
                if MRs == False:
                    print('\nMiddle + Right Sensor Detected\nTurning Left: Hard')
                    Ls   = False
                    Ms   = False
                    Rs   = False
                    LMs  = False
                    MRs  = True
                    LRs  = False
                    LMRs = False
                    NULs = False
                    PWM.setMotorModel(tF,tF,fF,fF)
            elif LMR==1: # Right Sensor
                if Rs == False:
                    print('\nRight Sensor Detected\nTurning Left: Soft')
                    Ls   = False
                    Ms   = False
                    Rs   = True
                    LMs  = False
                    MRs  = False
                    LRs  = False
                    LMRs = False
                    NULs = False
                    PWM.setMotorModel(tS,tS,fF,fF)


    except KeyboardInterrupt:   # Ctrl+C
        print('\nFunction: main()\nStatus:   inactive')
        PWM.setMotorModel(0,0,0,0)

# test() --- Where test code occurs before it is decided whether it is used in main() or not
# def test():
#     # v0.3 Test
#     print('Function: test()\nStatus:   active')

#     try:
#         print('\nplaceholder')
#     except KeyboardInterrupt:   # Ctrl+C
#         print('Function: test()\nStatus:   inactive')
#         PWM.setMotorModel(0,0,0,0)

# harcode() --- This is called when all sensors are triggered, or the middle sensor alone is triggered
def hardcode(tick):
    try:
        time.sleep(1)



        PWM.setMotorModel(-600,-600,-600,-600)
        time.sleep(0.25)



        PWM.setMotorModel(0,0,0,0)
        time.sleep(1)



        if   tick == 0 or tick == 1: # Turn Right - 90 Degrees Approx.
            PWM.setMotorModel(2000,2000,-2000,-2000)
            time.sleep(0.9)

            PWM.setMotorModel(0,0,0,0)
            time.sleep(1)
        


        elif tick == 2: # Turn Left - 90 Degrees Approx.
            PWM.setMotorModel(-2000,-2000,2000,2000)
            time.sleep(0.9)

            PWM.setMotorModel(0,0,0,0)
            time.sleep(1)
        


        else: # Idk, break program for now
            PWM.setMotorModel(0,0,0,0)
            print('An unexpected error occurred')
            KeyboardInterrupt
    except KeyboardInterrupt:
        PWM.setMotorModel(0,0,0,0)
        print('An unexpected error has occurred')



# Function Calls --- Comment out whichever functions you do not intend to use before running the code
main()
# test()