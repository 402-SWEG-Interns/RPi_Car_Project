import time
from Motor import *
import RPi.GPIO as GPIO
class Line_Tracking:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)
    def run(self):
        
        PWM.setMotorModel(1000,1000,800,800) #forward
        time.sleep(2.8)
        PWM.setMotorModel(0,0,0,0)
        time.sleep(.5)

        i = 0

        while i < 15:
            PWM.setMotorModel(3000,3000,-800,-600) #first turn
            time.sleep(.095)
            i = i+1
        
        PWM.setMotorModel(0,0,0,0)
        time.sleep(.025)

        PWM.setMotorModel(900,800,800,800) # second straight
        time.sleep(1.85)

        i = 0

        while i < 5:
            PWM.setMotorModel(300,300,3000,3000) #second
            time.sleep(.045)
            PWM.setMotorModel(-4000,-4000,3000,3000)
            time.sleep(.045)
            i = i + 1

        PWM.setMotorModel(0,0,0,0)
        time.sleep(.025)

        PWM.setMotorModel(800,800,800,800)
        time.sleep(.32)
        
        
        i = 0

        while i < 5:
            PWM.setMotorModel(300,300,3000,3000) #second
            time.sleep(.05)
            PWM.setMotorModel(-4000,-4000,3000,3000)
            time.sleep(.05)
            i = i + 1


        PWM.setMotorModel(800,800,800,800)
        time.sleep(2.85)

        
        PWM.setMotorModel(-4000,-4000,3000,3000)
        time.sleep(.1)
        PWM.setMotorModel(300,300,3000,3000)
        time.sleep(.1)
        
        

        PWM.setMotorModel(800,800,800,800)
        time.sleep(2.5)
        
        

        

        PWM.setMotorModel(0,0,0,0)
            
infrared=Line_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)