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
        self.LMR=0x00
        while self.LMR != 7:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            


            if self.LMR==2:
                PWM.setMotorModel(800,800,800,800)
                print("2")
            elif self.LMR==4:
                PWM.setMotorModel(2500,2500,-1500,-1500) #shift right
                print("4")
            
            elif self.LMR==1:
                PWM.setMotorModel(-1500,-1500,2500,2500) #shift left
                print("1")
            elif self.LMR==3:
                PWM.setMotorModel(-1500,-1500,2500,2500) #shift left
                print("3")
            if self.LMR==0:
                PWM.setMotorModel(700,700,800,800) #straight
                print("0")

        
        PWM.setMotorModel(0,0,0,0)
        time.sleep(.5)
        PWM.setMotorModel(-800,-800,-800,-800)
        time.sleep(.3)
        PWM.setMotorModel(1500,1500,-1500,-1500)
        time.sleep(1)
        print("7")

        #SECOND TURN
        self.LMR=0x00
        while self.LMR != 7:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            


            if self.LMR==2:
                PWM.setMotorModel(800,800,800,800)
                print("2")
            elif self.LMR==4:
                PWM.setMotorModel(2000,2000,-1500,-1500) #shift right
                print("4")
            
            elif self.LMR==1:
                PWM.setMotorModel(-1500,-1500,2500,2500) #shift left
                print("1")
            elif self.LMR==3:
                PWM.setMotorModel(-1500,-1500,2500,2500) #shift left
                print("3")
            if self.LMR==0:
                PWM.setMotorModel(800,800,800,800) #straight
                print("0")

        
        PWM.setMotorModel(0,0,0,0)
        time.sleep(.5)
        PWM.setMotorModel(-800,-800,-800,-800)
        time.sleep(.1)
        PWM.setMotorModel(1500,1500,-1500,-1500)
        time.sleep(1)
        print("7")
        


        #THIRD TURN
        self.LMR=0x00
        while self.LMR != 7:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            


            if self.LMR==2:
                PWM.setMotorModel(800,800,800,800)
                print("2")
            elif self.LMR==4:
                PWM.setMotorModel(2500,2500,-1500,-1500) #shift right
                print("4")
            
            elif self.LMR==1:
                PWM.setMotorModel(-1500,-1500,2500,2500) #shift left
                print("1")
            elif self.LMR==3:
                PWM.setMotorModel(-1500,-1500,2500,2500) #shift left
                print("3")
            if self.LMR==0:
                PWM.setMotorModel(800,800,800,800) #straight
                print("0")

        
        PWM.setMotorModel(0,0,0,0)
        time.sleep(.5)
        PWM.setMotorModel(-800,-800,-800,-800)
        time.sleep(.1)
        PWM.setMotorModel(-1500,-1500,1500,1500)
        time.sleep(1)
        print("7")
        


        #FOURTH TURN
        self.LMR=0x00
        while self.LMR != 7:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            


            if self.LMR==2:
                PWM.setMotorModel(800,800,800,800)
                print("2")
            elif self.LMR==4:
                PWM.setMotorModel(2500,2500,-1500,-1500) #shift right
                print("4")
            
            elif self.LMR==1:
                PWM.setMotorModel(-1500,-1500,2500,2500) #shift left
                print("1")
            elif self.LMR==3:
                PWM.setMotorModel(-1500,-1500,2500,2500) #shift left
                print("3")
            if self.LMR==0:
                PWM.setMotorModel(800,800,800,800) #straight
                print("0")
            

        
        PWM.setMotorModel(0,0,0,0)
        time.sleep(.5)
        PWM.setMotorModel(-800,-800,-800,-800)
        time.sleep(.1)
        PWM.setMotorModel(-1500,-1500,1500,1500)
        time.sleep(1)
        print("7")


        self.LMR=0x00
        while self.LMR != 7:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            


            if self.LMR==2:
                PWM.setMotorModel(800,800,800,800)
                print("2")
            elif self.LMR==4:
                PWM.setMotorModel(2500,2500,-1500,-1500) #shift right
                print("4")
            
            elif self.LMR==1:
                PWM.setMotorModel(-1500,-1500,2500,2500) #shift left
                print("1")
            elif self.LMR==3:
                PWM.setMotorModel(-1500,-1500,2500,2500) #shift left
                print("3")
            if self.LMR==0:
                PWM.setMotorModel(800,800,800,800) #straight
                print("0")
        


infrared=Line_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)
