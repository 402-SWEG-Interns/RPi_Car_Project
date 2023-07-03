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
IR01 = 14
IR02 = 15
IR03 = 23
IR = [IR01, IR02, IR03]
pin.setup(IR, pin.IN)



# Functions
# main() --- Where the actual program occurs
def main():
    # v0.3
    print('Function: main()\nStatus:   active')
    
    try:
        print('\nplaceholder')
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

# Function Calls --- Comment out whichever functions you do not intend to use before running the code
main()
# test()