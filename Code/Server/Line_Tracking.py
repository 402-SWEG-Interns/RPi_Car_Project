import time
from Motor import *
from servo import *
import RPi.GPIO as GPIO
class Line_Tracking:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23

        self.x_pos = 0
        self.objFound = False
        self.servoX = 0

        self.loop = 0

        self.LMR = 0
        



        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)
    def run(self):
        self.pwm_S=Servo()
        self.pwm_S.setServoPwm('0',100)

        PWM.setMotorModel(800,800,800,800)
        time.sleep(1.5)

        while True:

            
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)

            if self.servoX >= 85 and self.servoX <= 95 and self.x_pos != 0:
                
                
                PWM.setMotorModel(800,800,800,800)
                time.sleep(.1)
                PWM.setMotorModel(0,0,0,0)
                time.sleep(.1)


            elif self.servoX >95:
                print("right")
                PWM.setMotorModel(1500,1500,-2000,-2000)
                time.sleep(.05)
                PWM.setMotorModel(0,0,0,0)
                time.sleep(.8)
            elif self.servoX <85:
                print("left")
                PWM.setMotorModel(-2000,-2000,1500,1500)
                time.sleep(.05)
                PWM.setMotorModel(0,0,0,0)
                time.sleep(.8)

            elif self.x_pos == 0:
                PWM.setMotorModel(-2000,-2000,1500,1500)
                time.sleep(.05)
                PWM.setMotorModel(0,0,0,0)
                time.sleep(.8)



            if self.LMR == 7:
                
                #if self.loop == 0:
                #self.loop += 1
                PWM.setMotorModel(-0,-0,-0,-0)
                time.sleep(1)
                PWM.setMotorModel(-800,-800,-800,-800)
                time.sleep(.5)
                PWM.setMotorModel(-800,-800,1000,1000)
                time.sleep(.5)

                self.pwm_S.setServoPwm('0',100)
                self.servoX = 100
                     



                """  if self.loop == 1:
                    self.loop += 1
                    PWM.setMotorModel(-800,-800,-800,-800)
                    time.sleep(.5)

                if self.loop == 2:
                    self.loop += 10
                    PWM.setMotorModel(-800,-800,-800,-800)
                    time.sleep(.5)

                if self.loop == 3:
                    self.loop += 1
                    PWM.setMotorModel(-800,-800,-800,-800)
                    time.sleep(.5) """

               
                
                


            
            
infrared=Line_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)
