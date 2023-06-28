import Motor
from Motor import *
import time
            
            
PWM=Motor()          
def test_loop(): 
    PWM.setMotorModel(2000,2000,2000,2000)       #Forward
    time.sleep(3)
    PWM.setMotorModel(-2000,-2000,-2000,-2000)   #Back
    time.sleep(3)
    PWM.setMotorModel(-500,-500,2000,2000)       #Left 
    time.sleep(3)
    PWM.setMotorModel(2000,2000,-500,-500)       #Right    
    time.sleep(3)
    PWM.setMotorModel(0,0,0,0)                   #Stop

def path_loop():
    
    forward()
    time.sleep(2.1)
    halfturn()
    time.sleep(1.35)
    """
    #right()
    time.sleep(1.35)
    left()

    time.sleep(1.25)
    forward()
    time.sleep(.5)
    left()
    time.sleep(.5)
    """


    left()
    time.sleep(.925)
    forward()
    time.sleep(.5)
    left()
    time.sleep(.3)
    forward()
    time.sleep(1.9)
    left()
    time.sleep(.3)
    forward()
    time.sleep(1.5)
    PWM.setMotorModel(0,0,0,0) 

def halfturn():
    for i in range(5):
        right()
        time.sleep(.25)
        forward()
        time.sleep(.07)
  
    pass

def forward():
    PWM.setMotorModel(1500,1500,1250,1250)  #Forward

def right():
     PWM.setMotorModel(2000,2000,-1500,-1500)

def backwards():
    PWM.setMotorModel(-2000,-2000,-950,-950)   #Back

def left():
     PWM.setMotorModel(-1500,-1500, 2000, 2000)




    
def destroy():
    PWM.setMotorModel(0,0,0,0)                   
if __name__=='__main__':
    try:
        path_loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
    