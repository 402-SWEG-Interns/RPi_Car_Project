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


    def lineavoid(self):
        while True:
            self.LMR=0x00
            if GPIO.input(self.IR01)==False:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==False:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==False:
                self.LMR=(self.LMR | 1)
            if self.LMR==0:
                PWM.setMotorModel(0,0,0,0)
            if self.LMR==2:
                PWM.setMotorModel(800,800,800,800)
            elif self.LMR==4:
                PWM.setMotorModel(-1500,-1500,2500,2500)
            elif self.LMR==6:
                PWM.setMotorModel(-2000,-2000,4000,4000)
            elif self.LMR==1:
                PWM.setMotorModel(2500,2500,-1500,-1500)
            elif self.LMR==3:
                PWM.setMotorModel(4000,4000,-2000,-2000)
            elif self.LMR==7:
                PWM.setMotorModel(0,0,0,0)


infrared = Line_Tracking()


if __name__ == '__main__':
    print ('Program is starting ... ')
    try:


        infrared.lineavoid()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)



