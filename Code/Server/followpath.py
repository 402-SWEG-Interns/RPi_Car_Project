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
    time.sleep(2.67)

    stop()
    halfturn()

    stop()
    forward()
    time.sleep(2)
    

    stop()
    left()
    time.sleep(.6985)

    stop()
    forward()
    time.sleep(.575)

    stop()
    left()
    time.sleep(.5525)

    stop()
    forward()
    time.sleep(2.17)

    stop()
    left()
    time.sleep(.225)

    stop()
    forward()
    time.sleep(3)
    
    stop()

def halfturn():
    for i in range(5):
        right()
        time.sleep(.32)
        forward()
        time.sleep(.04)
  
    pass

def forward():
    PWM.setMotorModel(900,900,850,850)  #Forward

def right():
     PWM.setMotorModel(2000,2000,-1000,-1000)

def backwards():
    PWM.setMotorModel(-900,-900,-850,-850)   #Back

def left():
     PWM.setMotorModel(-1500,-1500, 2000, 2000)

def stop():
    PWM.setMotorModel(0,0,0,0) 
    time.sleep(.25)





    
def destroy():
    PWM.setMotorModel(0,0,0,0)                   
if __name__=='__main__':
    try:
        path_loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
    