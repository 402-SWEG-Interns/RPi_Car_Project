import time
import RPi.GPIO as pin
from Motor import *

pin.setmode(pin.BCM)
PWM=Motor()

# Infrared Initialized
IR01 = 14 # Left
IR02 = 15 # Middle
IR03 = 23 # Right
IR = [IR01, IR02, IR03] # If this doesn't work, just manually setup each
pin.setup(IR, pin.IN)

def main():
    
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
                    PWM.setMotorModel(-tF,-tF,tS,tS)
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
                    PWM.setMotorModel(-tF,-tF,tF,tF)

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
                    time.sleep(1)


                    PWM.setMotorModel(-600,-600,-600,-600)
                    time.sleep(0.75)



                    PWM.setMotorModel(0,0,0,0)
                    time.sleep(1)



                    if   tick == 0 or tick == 1: # Turn Right - 90 Degrees Approx.
                        tick = tick + 1
                        PWM.setMotorModel(2000,2000,-2000,-2000)
                        time.sleep(0.9)

                        PWM.setMotorModel(0,0,0,0)
                        time.sleep(1)
                    
                    elif tick == 2 or tick == 3: # Turn Left - 90 Degrees Approx.
                        tick = tick + 1
                        PWM.setMotorModel(-2000,-2000,2000,2000)
                        time.sleep(0.9)

                        PWM.setMotorModel(0,0,0,0)
                        time.sleep(1)

                        if tick == 3:
                           tick = 0
                    
                    else: # Idk, break program for now
                        PWM.setMotorModel(0,0,0,0)
                        print('An unexpected error occurred')
                        KeyboardInterrupt
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
                    time.sleep(1)


                    PWM.setMotorModel(-600,-600,-600,-600)
                    time.sleep(0.75)



                    PWM.setMotorModel(0,0,0,0)
                    time.sleep(1)



                    if   tick == 0 or tick == 1: # Turn Right - 90 Degrees Approx.
                        tick = tick + 1
                        PWM.setMotorModel(2000,2000,-2000,-2000)
                        time.sleep(0.9)

                        PWM.setMotorModel(0,0,0,0)
                        time.sleep(1)
                    
                    elif tick == 2 or tick == 3: # Turn Left - 90 Degrees Approx.
                        tick = tick + 1
                        PWM.setMotorModel(-2000,-2000,2000,2000)
                        time.sleep(0.9)

                        PWM.setMotorModel(0,0,0,0)
                        time.sleep(1)

                        if tick == 3:
                           tick = 0

                    else: # Idk, break program for now
                        PWM.setMotorModel(0,0,0,0)
                        print('An unexpected error occurred')
                        KeyboardInterrupt

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
                    PWM.setMotorModel(tF,tF,-tF,-tF)
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
                    PWM.setMotorModel(tS,tS,-tF,-tF)

    except KeyboardInterrupt:   # Ctrl+C
        print('\nFunction: main()\nStatus:   inactive')
        PWM.setMotorModel(0,0,0,0)


main()
