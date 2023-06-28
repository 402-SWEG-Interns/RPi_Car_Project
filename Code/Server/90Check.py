import time
from Motor import *

PWM = Motor()

def checkNinety(t=int, Left=False):
    if Left:
        PWM.setMotorModel(-1500,-1500,1500,1500)
    else:
        PWM.setMotorModel(1500,1500,-1600,-1500)
    time.sleep(t)
    print("done")
    PWM.setMotorModel(0, 0, 0, 0)

checkNinety(1.1, True)
time.sleep(0.5)
checkNinety(1.8, False)
