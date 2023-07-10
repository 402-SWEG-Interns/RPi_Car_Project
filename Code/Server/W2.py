import time
from Motor import *
import RPi.GPIO as GPIO
from Line_Tracking import *
# line=Line_Trackingself

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
        while True:
            
            self.LMR=0x00
            if GPIO.input(self.IR01)==True and GPIO.input(self.IR02)==True and GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 6)
            if GPIO.input(self.IR01)!=True and GPIO.input(self.IR02)!=True and GPIO.input(self.IR03)!=True:
                self.LMR=(self.LMR | 7)
            if GPIO.input(self.IR01)==True and GPIO.input(self.IR02)!=True and GPIO.input(self.IR03)!=True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR01)!=True and GPIO.input(self.IR02)!=True and GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)


            i = 0

            if self.LMR==4:
                PWM.setMotorModel(-900,-900,900,900) #right
                
                print("4")
            elif self.LMR==6:
                PWM.setMotorModel(2000,2000,2000,2000)
                time.sleep(0.2)
                PWM.setMotorModel(-2000,-2000,2000,2000)
                time.sleep(0.5)
                break
                


                print(6)
            elif self.LMR==1:
                PWM.setMotorModel(1000,1000,-1000,-1000) #left
                print("1")
            elif self.LMR==7:
                #pass
                PWM.setMotorModel(-1000,-1000,-900,-900)

                print("7")
        while True:
            
            self.LMR=0x00
            if GPIO.input(self.IR01)==True and GPIO.input(self.IR02)==True and GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 6)
            if GPIO.input(self.IR01)!=True and GPIO.input(self.IR02)!=True and GPIO.input(self.IR03)!=True:
                self.LMR=(self.LMR | 7)
            if GPIO.input(self.IR01)==True and GPIO.input(self.IR02)!=True and GPIO.input(self.IR03)!=True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR01)!=True and GPIO.input(self.IR02)!=True and GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)


            i = 0

            if self.LMR==4:
                PWM.setMotorModel(-900,-900,900,900) #right
                
                print("4")
            elif self.LMR==6:
                PWM.setMotorModel(2000,2000,2000,2000)
                time.sleep(0.2)
                PWM.setMotorModel(-2000,-2000,2000,2000)
                time.sleep(0.75)
                break


                print(6)
            elif self.LMR==1:
                PWM.setMotorModel(1000,1000,-1000,-1000) #left
                print("1")
            elif self.LMR==7:
                #pass
                PWM.setMotorModel(-1000,-1000,-900,-900)

                print("7")
        while True:
            
            self.LMR=0x00
            # if GPIO.input(self.IR01)==False:
            #     self.LMR=(self.LMR | 4)
            # if GPIO.input(self.IR02)==False:
            #     self.LMR=(self.LMR | 2)
            # if GPIO.input(self.IR03)==False:
            #     self.LMR=(self.LMR self


            if GPIO.input(self.IR01)==True and GPIO.input(self.IR02)==True and GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 6)
            if GPIO.input(self.IR01)!=True and GPIO.input(self.IR02)!=True and GPIO.input(self.IR03)!=True:
                self.LMR=(self.LMR | 7)
            if GPIO.input(self.IR01)==True and GPIO.input(self.IR02)!=True and GPIO.input(self.IR03)!=True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR01)!=True and GPIO.input(self.IR02)!=True and GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            if GPIO.input(self.IR01)!=True and GPIO.input(self.IR02)==True and GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)


            i = 0

            if self.LMR==4:
                PWM.setMotorModel(-900,-900,900,900) #right
                
                print("4")
            elif self.LMR==6:
                PWM.setMotorModel(2000,2000,2000,2000)
                time.sleep(0.13)
                PWM.setMotorModel(2000,2000,-2000,-2000)
                time.sleep(0.5)
                


                print(6)
            elif self.LMR==1:
                PWM.setMotorModel(900,900,-900,-900) #left
                print("1")
            elif self.LMR==7:
                #pass
                PWM.setMotorModel(-700,-700,-600,-600)

                print("7")


            
infrared=Line_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)


#------------------------------------------------------------------------------------------------------------
