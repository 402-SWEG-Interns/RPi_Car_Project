import time
from Motor import *
import RPi.GPIO as GPIO
from Line_Tracking import *
line=Line_Tracking()



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
            # if GPIO.input(self.IR01)==False:
            #     self.LMR=(self.LMR | 4)
            # if GPIO.input(self.IR02)==False:
            #     self.LMR=(self.LMR | 2)
            # if GPIO.input(self.IR03)==False:
            #     self.LMR=(self.LMR | 1)


            if GPIO.input(line.IR01)==True and GPIO.input(line.IR02)==True and GPIO.input(line.IR03)==True:
                self.LMR=(self.LMR | 6)
            if GPIO.input(line.IR01)!=True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)!=True:
                self.LMR=(self.LMR | 7)
            if GPIO.input(line.IR01)==True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)!=True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(line.IR01)!=True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)==True:
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
            # if GPIO.input(self.IR01)==False:
            #     self.LMR=(self.LMR | 4)
            # if GPIO.input(self.IR02)==False:
            #     self.LMR=(self.LMR | 2)
            # if GPIO.input(self.IR03)==False:
            #     self.LMR=(self.LMR | 1)


            if GPIO.input(line.IR01)==True and GPIO.input(line.IR02)==True and GPIO.input(line.IR03)==True:
                self.LMR=(self.LMR | 6)
            if GPIO.input(line.IR01)!=True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)!=True:
                self.LMR=(self.LMR | 7)
            if GPIO.input(line.IR01)==True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)!=True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(line.IR01)!=True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)==True:
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
            #     self.LMR=(self.LMR | 1)


            if GPIO.input(line.IR01)==True and GPIO.input(line.IR02)==True and GPIO.input(line.IR03)==True:
                self.LMR=(self.LMR | 6)
            if GPIO.input(line.IR01)!=True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)!=True:
                self.LMR=(self.LMR | 7)
            if GPIO.input(line.IR01)==True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)!=True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(line.IR01)!=True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)==True:
                self.LMR=(self.LMR | 1)
            if GPIO.input(line.IR01)!=True and GPIO.input(line.IR02)==True and GPIO.input(line.IR03)==True:
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
# from Line_Tracking import *
# line=Line_Tracking()
# def run(self):
#     try:
#         while True:
#             if GPIO.input(line.IR01)==True and GPIO.input(line.IR02)==True and GPIO.input(line.IR03)==True:
#                 right()
#             elif GPIO.input(line.IR01)!=True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)==True:
#                 PWM.setMotorModel(-500,-500,800,800) 
#             elif GPIO.input(line.IR01)==True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)!=True:
#                 PWM.setMotorModel(800,800,-500,-500) 
#             elif GPIO.input(line.IR01)!=True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)!=True:
#                 PWM.setMotorModel(-800,-800,-800,-800) 
#                 print(1)

#     except KeyboardInterrupt:
#         print ("\nEnd of program")

# def right(self):
#     PWM.setMotorModel(0,0,0,0) 
#     time.sleep(0.5)
#     PWM.setMotorModel(400,400,400,400) 
#     time.sleep(0.2)
#     PWM.setMotorModel(500,500,-500,-500) 
#     time.sleep(.25)
#     PWM.setMotorModel(0,0,0,0) 

# def left(self):
#     PWM.setMotorModel(0,0,0,0) 


# if __name__ == '__main__':
#     print ('Program is starting ... ')
#     try:
#         infrared.run()
#     except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
#         PWM.setMotorModel(0,0,0,0)

#-------------------------------------------------------------------------------------------------------------

# import numpy as np
# import cv2
  
  
# # Capturing video through webcam
# webcam = cv2.VideoCapture(0)
  
# # Start a while loop
# while(1):
      
#     # Reading the video from the
#     # webcam in image frames
#     _, imageFrame = webcam.read()
  
#     # Convert the imageFrame in 
#     # BGR(RGB color space) to 
#     # HSV(hue-saturation-value)
#     # color space
#     hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
  
#     # Set range for red color and 
#     # define mask
#     red_lower = np.array([136, 87, 111], np.uint8)
#     red_upper = np.array([180, 255, 255], np.uint8)
#     red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
  
#     # Set range for green color and 
#     # define mask
#     green_lower = np.array([25, 52, 72], np.uint8)
#     green_upper = np.array([102, 255, 255], np.uint8)
#     green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
  
#     # Set range for blue color and
#     # define mask
#     blue_lower = np.array([94, 80, 2], np.uint8)
#     blue_upper = np.array([120, 255, 255], np.uint8)
#     blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
      
#     # Morphological Transform, Dilation
#     # for each color and bitwise_and operator
#     # between imageFrame and mask determines
#     # to detect only that particular color
#     kernel = np.ones((5, 5), "uint8")
      
#     # For red color
#     red_mask = cv2.dilate(red_mask, kernel)
#     res_red = cv2.bitwise_and(imageFrame, imageFrame, 
#                               mask = red_mask)
      
#     # For green color
#     green_mask = cv2.dilate(green_mask, kernel)
#     res_green = cv2.bitwise_and(imageFrame, imageFrame,
#                                 mask = green_mask)
      
#     # For blue color
#     blue_mask = cv2.dilate(blue_mask, kernel)
#     res_blue = cv2.bitwise_and(imageFrame, imageFrame,
#                                mask = blue_mask)
   
#     # Creating contour to track red color
#     contours, hierarchy = cv2.findContours(red_mask,
#                                            cv2.RETR_TREE,
#                                            cv2.CHAIN_APPROX_SIMPLE)
      
#     for pic, contour in enumerate(contours):
#         area = cv2.contourArea(contour)
#         if(area > 300):
#             x, y, w, h = cv2.boundingRect(contour)
#             imageFrame = cv2.rectangle(imageFrame, (x, y), 
#                                        (x + w, y + h), 
#                                        (0, 0, 255), 2)
              
#             cv2.putText(imageFrame, "Red Colour", (x, y),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1.0,
#                         (0, 0, 255))    
  
#     # Creating contour to track green color
#     contours, hierarchy = cv2.findContours(green_mask,
#                                            cv2.RETR_TREE,
#                                            cv2.CHAIN_APPROX_SIMPLE)
      
#     for pic, contour in enumerate(contours):
#         area = cv2.contourArea(contour)
#         if(area > 300):
#             x, y, w, h = cv2.boundingRect(contour)
#             imageFrame = cv2.rectangle(imageFrame, (x, y), 
#                                        (x + w, y + h),
#                                        (0, 255, 0), 2)
              
#             cv2.putText(imageFrame, "Green Colour", (x, y),
#                         cv2.FONT_HERSHEY_SIMPLEX, 
#                         1.0, (0, 255, 0))
  
#     # Creating contour to track blue color
#     contours, hierarchy = cv2.findContours(blue_mask,
#                                            cv2.RETR_TREE,
#                                            cv2.CHAIN_APPROX_SIMPLE)
#     for pic, contour in enumerate(contours):
#         area = cv2.contourArea(contour)
#         if(area > 300):
#             x, y, w, h = cv2.boundingRect(contour)
#             imageFrame = cv2.rectangle(imageFrame, (x, y),
#                                        (x + w, y + h),
#                                        (255, 0, 0), 2)
              
#             cv2.putText(imageFrame, "Blue Colour", (x, y),
#                         cv2.FONT_HERSHEY_SIMPLEX,
#                         1.0, (255, 0, 0))
              
#     # Program Termination
#     cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         cap.release()
#         cv2.destroyAllWindows()
#         break