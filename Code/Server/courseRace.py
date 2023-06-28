from Motor import *
from Line_Tracking import *
import sys
import time

PWM=Motor()
line = Line_Tracking()

# IR01 = Left
# IR02 = Middle
# IR03 = Right

def runCourse(s):
    turnDirection = 1
    speed = s
    
    PWM.setMotorModel(int(speed*1000), int(speed*1000), int(speed*1000), int(speed*1000))
    while True:
        try:
            if (GPIO.input(line.IR01) and not GPIO.input(line.IR02) and not GPIO.input(line.IR03)) or (GPIO.input(line.IR01) and GPIO.input(line.IR02) and not GPIO.input(line.IR03)):
                # PWM.setMotorModel(int(speed*1500),int(speed*1500),int(speed*-1600),int(speed*-1800)) 
                time.sleep(0.1)
                PWM.setMotorModel(int(speed*-500),int(speed*-500),int(speed*-1500),int(speed*-1500))
                print("Right")
            elif (not GPIO.input(line.IR01) and not GPIO.input(line.IR02) and GPIO.input(line.IR03)) or (not GPIO.input(line.IR01) and GPIO.input(line.IR02) and GPIO.input(line.IR03)):
                # PWM.setMotorModel(int(speed*-1500),int(speed*-1800),int(speed*1500),int(speed*1500))
                PWM.setMotorModel(int(speed*-1500),int(speed*-1500),int(speed*-500),int(speed*-500)) 
                time.sleep(0.2)

                print("Left")
            elif GPIO.input(line.IR01) and GPIO.input(line.IR02) and GPIO.input(line.IR03):
                PWM.setMotorModel(int(speed*1000), int(speed*1000), int(speed*1000), int(speed*1000))
                print("Back")
                time.sleep(0.5)
                PWM.setMotorModel(turnDirection * int(speed*-1500), turnDirection * int(speed*-1500), turnDirection * int(speed*1500), turnDirection * int(speed*1500))
                while True:
                    
                    if not GPIO.input(line.IR01) and not GPIO.input(line.IR02) and not GPIO.input(line.IR03):
                        time.sleep(1)
                        turnDirection *= -1
                        break

            else:
                PWM.setMotorModel(int(speed*1000), int(speed*1000), int(speed*1000), int(speed*1000))
                print("Forward")

        except KeyboardInterrupt:
            print("Program end")
            PWM.setMotorModel(0,0,0,0)  
            break
        except Exception as e:
            print(e)
            PWM.setMotorModel(0,0,0,0)  
            break



runCourse(1)