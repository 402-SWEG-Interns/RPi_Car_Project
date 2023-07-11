from colorchange import *
import cv2
import numpy as np 
import sys


class DetectColors:
    def __init__(self):
        self.colors_detected = []
        self.last_color = ""
        

    def color_detect(self, imageFrame):
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
          

        
            hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        
            # Set range for red color and 
            # define mask
            red_lower = np.array([160, 87, 111], np.uint8)
            red_upper = np.array([180, 255, 255], np.uint8)
            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
        
            # Set range for green color and 
            # define mas
            green_lower = np.array([40, 190, 75], np.uint8)
            green_upper = np.array([86, 255, 255], np.uint8)
            green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
        
            # Set range for blue color and
            # define mask
            blue_lower = np.array([87, 130, 125], np.uint8)
            blue_upper = np.array([110, 255, 255], np.uint8)
            blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

            yellow_lower = np.array([24, 190, 111], np.uint8)
            yellow_upper = np.array([30, 255, 255], np.uint8)
            yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
            
            # Morphological Transform, Dilation
            # for each color and bitwise_and operator
            # between imageFrame and mask determines
            # to detect only that particular color
            kernel = np.ones((5, 5), "uint8")
            
            # For red color
            red_mask = cv2.dilate(red_mask, kernel)
            res_red = cv2.bitwise_and(imageFrame, imageFrame, 
                                    mask = red_mask)
            
            # For green color
            green_mask = cv2.dilate(green_mask, kernel)
            res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                        mask = green_mask)
            
            # For blue color
            blue_mask = cv2.dilate(blue_mask, kernel)
            res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                                    mask = blue_mask)
            
            yellow_mask = cv2.dilate(yellow_mask, kernel)
            res_yellow = cv2.bitwise_and(imageFrame, imageFrame,
                                    mask = yellow_mask)

            
            previous_colors = self.colors_detected
            found_color = []
            

           
            # Creating contour to track red color
            contours, hierarchy = cv2.findContours(red_mask,
                                                cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)

            found_color = []

           
            size = 300
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    found_color.append('red')
                    if 'red' not in self.colors_detected:
                        self.colors_detected.append('red')
                        self.last_color = 'red'
                        return
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                            (x + w, y + h), 
                                            (0, 0, 255), 2)
                    
                    cv2.putText(imageFrame, "Red Color", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                (0, 0, 255))    
            
                    
        

            
            
            # Creating contour to track green color
            contours, hierarchy = cv2.findContours(green_mask,
                                                cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
            
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    found_color.append('green')
                    if 'green' not in self.colors_detected:
                        self.colors_detected.append('green')
                        self.last_color = 'green'
                        return
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                            (x + w, y + h),
                                            (0, 255, 0), 2)
                    
                    cv2.putText(imageFrame, "Green Color", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1.0, (0, 255, 0))
        
                                     
            # Creating contour to track blue color
            contours, hierarchy = cv2.findContours(blue_mask,
                                                cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
         
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    found_color.append('blue')
                    if 'blue' not in self.colors_detected:                     
                        self.colors_detected.append('blue')
                        self.last_color = 'blue'
                        return
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y),
                                            (x + w, y + h),
                                            (255, 0, 0), 2)
                    
                    cv2.putText(imageFrame, "Blue Color", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.0, (255, 0, 0))
                    
            # Creating contour to track yellow color
            contours, hierarchy = cv2.findContours(yellow_mask,
                                                cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)

                    
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    found_color.append('yellow')
                    if 'yellow' not in self.colors_detected:
                        self.colors_detected.append('yellow')
                        self.last_color = 'yellow'
                        return
                    
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                            (x + w, y + h), 
                                            (255, 255, 0), 2)
                    
                    cv2.putText(imageFrame, "Yellow Color", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                (0, 0, 255))    
            
            
            for color in self.colors_detected:
                if color not in found_color:
                    self.colors_detected.remove(color)

            cv2.imwrite('video.jpg',imageFrame)
            cv2.waitKey(1) 