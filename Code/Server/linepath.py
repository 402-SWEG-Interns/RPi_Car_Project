import time
from Motor import *
from Line_Tracking import *
import RPi.GPIO as GPIO
#from Video import *

line=Line_Tracking()
class LinePath:
    def __init__(self) -> None:
        pass

    def run(self):
        count = 0
        try:
            while True:
                
                if GPIO.input(line.IR01) !=True and GPIO.input(line.IR02) !=True and GPIO.input(line.IR03) != True:
                    PWM.setMotorModel(800,800,750,750)

                elif GPIO.input(line.IR01)==True and GPIO.input(line.IR02)==True and GPIO.input(line.IR03)==True and count <= 1:
                    self.process_line1()
                    count+= 1

                elif GPIO.input(line.IR01)==True and GPIO.input(line.IR02)==True and GPIO.input(line.IR03)==True and count == 2 :
                    self.process_line2()
                    count += 1

                elif GPIO.input(line.IR01)==True and GPIO.input(line.IR02)==True and GPIO.input(line.IR03)==True and count > 2 :
                    PWM.setMotorModel(-700,-700,-650,-650)
                    time.sleep(.05)

                # if line is detected on the right
                elif GPIO.input(line.IR01)!=True and GPIO.input(line.IR03)==True and GPIO.input(line.IR02)!=True :
                    # turn left
                    PWM.setMotorModel(-1700,-1700, 2200, 2200)
                   
                
                # if line is detected on the left
                elif GPIO.input(line.IR01)==True and GPIO.input(line.IR03)!=True and GPIO.input(line.IR02)!=True :
                    # turn right
                    PWM.setMotorModel(2200,2200,-1200,-1200)
                   
                    
        except KeyboardInterrupt:
            print ("\nEnd of program")
            destroy()


    def process_line1(self):
        #stop
        PWM.setMotorModel(0,0,0,0)
        time.sleep(0.1)
        #backwards
        PWM.setMotorModel(-700,-700,-650,-650)
        time.sleep(0.2)
        # turn right
        PWM.setMotorModel(2000,2000,-1500,-1500)
        time.sleep(1)

    def process_line2(self):
        #stop
        PWM.setMotorModel(0,0,0,0)
        time.sleep(0.1)
        #backwards
        PWM.setMotorModel(-700,-700,-650,-650)
        time.sleep(0.2)
        # turn left
        PWM.setMotorModel(-1500,-1500, 2000, 2000)
        time.sleep(1)




    def destroy():
        PWM.setMotorModel(0,0,0,0)   

linepath = LinePath()                
if __name__=='__main__':
    try:
        linepath.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
        
        


