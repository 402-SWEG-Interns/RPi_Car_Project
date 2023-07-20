from threading import Timer
from threading import Thread

from Motor import *
from servo import *
from Ultrasonic import *
from Line_Tracking import *
import time
import threading
import random
from Led import *


class SearchDestroy:
    def __init__(self):
        self.servo1 = 72
        self.servo = Servo()
        self.servo.setServoPwm('1', 80)
        self.motor = Motor()
        self.object_x = -1
        self.infrared = Line_Tracking()
        self.ultrasonic = Ultrasonic()
        self.led = Led()
        self.found_object = False
        self.object_conf = -1
        self.num_objects_confirmed = 0
        self.object_confirmed = False
    

    def run(self):
        self.ultra_move()
    def run2(self):
        self.move_forward()
        time.sleep(.2)
        self.stop()
        self.found_object = False
        while self.num_objects_confirmed < 3:
            self.objects_confirmed = False
            self.turn_red()

            self.search()
            self.turn_yellow()
            self.center()

            while self.object_conf < .94:
                self.move_forward_slow()

            self.num_objects_confirmed += 1
            self.object_confirmed = True
            self.turn_green()
            time.sleep(1)
            






    
    def search(self):
        while not self.found_object:

                self.scan()
                if self.found_object:
                    return

                self.ultra_move()
                if self.found_object:
                    return
                
                self.line = False
                self.direction = ""
                self.frames_forward = 0
                while not self.line:
                    self.follow_line()
                    if self.found_object:
                        self.line = True
                        self.stop()
                        return

                    time.sleep(.05)

    def follow_line(self):
        
        self.LMR_val = self.infrared.readSensor()
        #print(self.LMR_val)
        if self.LMR_val == 0:
            self.move_forward()
            self.frames_forward += 1
            if self.frames_forward > 10:
                self.direction = "none"
        elif self.LMR_val == 6 or self.LMR_val == 4:
            self.frames_forward = 0
            self.direction = "right"
            self.stop()
            self.servo1 = 170
            self.look()
            self.move_right()
            time.sleep(.025)
            
        elif self.LMR_val == 3 or self.LMR_val == 1:
            self.frames_forward = 0
            self.direction = "left"
            self.stop()
            self.servo1 = 10
            self.look()
            self.move_left()
            time.sleep(.025)
        elif self.LMR_val == 7:
            self.move_backwards()
            time.sleep(.15)
            if self.direction == "right":
                self.move_right()
                time.sleep(.3)
                self.stop()
            elif self.direction == "left":
                self.move_left()
                time.sleep(.3)
                self.stop()
            else:
                n = random.randint(1,2)
                if n == 1:
                    self.move_left()
                    time.sleep(.3)
                    self.stop()
                else:
                    self.move_right()
                    time.sleep(.3)
                    self.stop()

            return 

        pass

    def ultra_move(self):
        self.found_object = False
        self.ultrasonicTimer = threading.Thread(target=self.ultrasonic.run)
        self.ultrasonicTimer.start()
        while not self.found_object:
            time.sleep(.01)
            
            pass
        print("found object")
        self.ultrasonic.stop = True
    
        return
        
    def scan(self):
        print("scanning")
        for i in range(10):
            print("right")
            self.look_right()
            time.sleep(.7)
            if self.found_object:
                return 1
        for i in range(17):
            print("left")
            self.look_left()
            time.sleep(.7)
            if self.found_object:
                return 1
        for i in range(7):
            self.look_right()
            if self.found_object:
                return 1
        return -1

        

    def center(self):

        self.centered = False
        while not self.centered:
            if self.object_x >= 0:
                for i in range(3):
                    self.track_ball()
                    time.sleep(.025)
                time.sleep(.25)
                if self.servo1 < 70:
                    self.move_left()
                    time.sleep(.071)
                    self.stop()
                elif self.servo1 > 74:
                    self.move_right()
                    time.sleep(.071)
                    self.stop()
                else:
                    self.centered = True
            else:
                time.sleep(.2)


    def track_ball(self):
        if self.object_x > 0:
                offset_x=float(self.object_x/400-0.5)*2
                delta_degree_x = 4* offset_x
                self.servo1=self.servo1+delta_degree_x
                if offset_x > -0.075 and offset_x < 0.075:
                    pass
                else:
                    self.servo.setServoPwm("0", int(self.servo1))

    def turn_around(self):
        pass
                    
    
    def look_right(self):
        self.servo1 += 5
        self.servo.setServoPwm("0", int(self.servo1))
    
    def look_left(self):
        self.servo1 -= 5
        self.servo.setServoPwm("0", int(self.servo1))
    
    def look(self):
        self.servo.setServoPwm("0", int(self.servo1))

    def move_right(self):
        self.motor.setMotorModel(1500, 1500, -1500, -1500)
    def move_left(self):
        self.motor.setMotorModel(-1500, -1500, 1500, 1500)
    def move_forward(self):
        self.motor.setMotorModel(800, 800, 800, 800)
    def move_backwards(self):
        self.motor.setMotorModel(-1500, -1500, -1500, -1500)
    def stop(self):
        self.motor.setMotorModel(0,0,0,0)
    def move_forward_slow(self):
        self.motor.setMotorModel(500, 500, 500, 500)

    def turn_red(self):
        for i in range(self.led.strip.numPixels()):
                    self.led.strip.setPixelColor(i, Color(255, 0, 0))
                    self.led.strip.show()
    
    def turn_green(self):
        for i in range(self.led.strip.numPixels()):
                    self.led.strip.setPixelColor(i, Color(0, 255, 0))
                    self.led.strip.show()
    
    def turn_yellow(self):
            for i in range(self.led.strip.numPixels()):
                self.led.strip.setPixelColor(i, Color(30, 230, 255))
                self.led.strip.show()



