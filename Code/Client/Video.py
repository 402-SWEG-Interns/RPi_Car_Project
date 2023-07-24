#!/usr/bin/python 
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import socket
import io
import sys
import struct
import tensorflow as tf
import os
from PIL import Image
from multiprocessing import Process
from Command import COMMAND as cmd
import yolov5

class VideoStreaming():
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
        self.video_Flag=True
        self.connect_Flag=False
        self.object_x=0
        self.object_y=0

        # self.lastSeen = -1

        # self.redArea = 0
        # self.greenArea = 0
        # self.blueArea = 0
        # self.yellowArea = 0

        self.color = ''
    def StartTcpClient(self,IP):
        self.client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def StopTcpcClient(self):
        try:
            self.client_socket.shutdown(2)
            self.client_socket1.shutdown(2)
            self.client_socket.close()
            self.client_socket1.close()
        except:
            pass

    def IsValidImage4Bytes(self,buf): 
        bValid = True
        if buf[6:10] in (b'JFIF', b'Exif'):     
            if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
                bValid = False
        else:        
            try:  
                Image.open(io.BytesIO(buf)).verify() 
            except:  
                bValid = False
        return bValid

    def object_detect(self,img,obj): # Originally 'face_detect()', but now it is 'object_detect()'
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
            print(f'Object order is {obj[0]}, {obj[1]}, then {obj[2]}')

            """hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            red_lower = np.array([136, 87, 111], np.uint8)
            red_upper = np.array([180, 255, 255], np.uint8)
            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

            green_lower = np.array([45, 100, 72], np.uint8)
            green_upper = np.array([90, 255, 255], np.uint8)
            green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

            blue_lower = np.array([94, 80, 2], np.uint8)
            blue_upper = np.array([120, 255, 255], np.uint8)
            blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

            yellow_lower = np.array([25, 50, 70], np.uint8)
            yellow_upper = np.array([35, 255, 255], np.uint8)
            yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

            kernel = np.ones((5, 5), "uint8")

            red_mask = cv2.dilate(red_mask, kernel)
            res_red = cv2.bitwise_and(img, img, mask = red_mask)
        
            green_mask = cv2.dilate(green_mask, kernel)
            res_green = cv2.bitwise_and(img, img, mask = green_mask)
        
            blue_mask = cv2.dilate(blue_mask, kernel)
            res_blue = cv2.bitwise_and(img, img, mask = blue_mask)
            
            yellow_mask = cv2.dilate(yellow_mask, kernel)
            res_yellow = cv2.bitwise_and(img, img, mask = yellow_mask)
        
            contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)"""

            MODEL_NAME = 'Sample_TFLite_model'
            YOLOV5_GRAPH_NAME = 'model.pt'
            LABELMAP_NAME = 'labelmap.txt'
            min_conf_threshold = 0.3 # Original value: 0.3   New Value: 0.2???
            
            imW, imH = int(400), int(300)

            CWD_PATH = os.getcwd()

            PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

            PATH_TO_YOLOV5_GRAPH = os.path.join(CWD_PATH,MODEL_NAME,YOLOV5_GRAPH_NAME)

            frame = img.copy()

            with open(PATH_TO_LABELS, 'r') as f:
                labels = [line.strip() for line in f.readlines()]

            # Have to do a weird fix for label map if using the COCO "starter model" from
            # https://www.tensorflow.org/lite/models/object_detection/overview
            # First label is '???', which has to be removed.
            if labels[0] == '???':
                del(labels[0])

            """interpreter = tf.lite.Interpreter(model_path=PATH_TO_CKPT)

            interpreter.allocate_tensors()
            
            # Get model details
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            height = input_details[0]['shape'][1]
            width = input_details[0]['shape'][2]

            floating_model = (input_details[0]['dtype'] == np.float32)

            input_mean = 127.5
            input_std = 127.5

            # Check output layer name to determine if this model was created with TF2 or TF1,
            # because outputs are ordered differently for TF2 and TF1 models
            outname = output_details[0]['name']

            if ('StatefulPartitionedCall' in outname): # This is a TF2 model
                boxes_idx, classes_idx, scores_idx = 1, 3, 0
            else: # This is a TF1 model
                boxes_idx, classes_idx, scores_idx = 0, 1, 2"""
            
            # Use yolov5
            model = yolov5.load(PATH_TO_YOLOV5_GRAPH)

            # Set model parameters
            model.conf = 0.25  # NMS confidence threshold
            model.iou = 0.45  # NMS IoU threshold
            model.agnostic = False  # NMS class-agnostic
            model.multi_label = True  # NMS multiple labels per box
            model.max_det = 1000  # Maximum number of detections per image

            results = model(frame)
            predictions = results.pred[0].cpu()
            boxes = predictions[:, :4]
            scores = predictions[:, 4]
            classes = predictions[:, 5]
            results.render()

            # Initialize frame rate calculation
            frame_rate_calc = 15

            """frame_rgb = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)

            cv2.imwrite('frameRGB.jpg', frame_rgb) #the inverted colors???

            frame_resized = cv2.resize(frame_rgb, (width, height))

            cv2.imwrite('frameResized.jpg', frame_resized) # resized video for some reason?

            input_data = np.expand_dims(frame_resized, axis=0)

            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            # Perform the actual detection by running the model with the image as input
            interpreter.set_tensor(input_details[0]['index'],input_data)
            interpreter.invoke()

            # Retrieve detection results
            boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects
            scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confidence of detected objects

            max_score = 0
            max_index = 0


            #sports ball should be 36

            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                # Found desired object with decent confidence
                if ( (scores[i] > max_score) and (scores[i] > min_conf_threshold) and (scores[i] <= 1.0) and ((labels[int(classes[i])] == "sports ball") or labels[int(classes[i])] == "apple" or labels[int(classes[i])] == "bowl")):
                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))
                    
                    # Draw label
                    object_name = (self.color + " ball") # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                    label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                    cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                    cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

                    # Record current max
                    max_score = scores[i]
                    max_index = i

            if (max_index != 0):
                ymin = int(max(1,(boxes[max_index][0] * imH)))
                xmin = int(max(1,(boxes[max_index][1] * imW)))
                ymax = int(min(imH,(boxes[max_index][2] * imH)))
                xmax = int(min(imW,(boxes[max_index][3] * imW)))
                self.object_x = float(xmin+xmax/2)
                self.object_y = float(ymin+ymax/2)

            else:
                Stop = '#0#0#0#0\n'
                self.sendData(cmd.CMD_MOTOR+Stop)
                self.sendData(cmd.CMD_MODE+"#"+'six'+"#"+'-2'+"\n")"""
            
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            frame_resized = cv2.resize(frame_rgb, (imW, imH))

            input_data = np.expand_dims(frame_resized, axis=0)

            """# Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            # Perform the actual detection by running the model with the image as input
            interpreter.set_tensor(input_details[0]['index'],input_data)
            interpreter.invoke()

            # Retrieve detection results
            boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects
            scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confidence of detected objects"""

            max_score = 0
            max_index = 0

            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                curr_score = scores[i].numpy
                # Found desired object with decent confidence
                if ( (scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))

                    # Find bounding box center
                    cx = (xmax + xmin) / 2
                    cy = (ymax + ymin) / 2
                    
                    # Draw label
                    object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (object_name, int(curr_score*100)) # Example: 'person: 72%'
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                    label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                    cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                    cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

                    # Record current max
                    max_score = curr_score
                    max_index = i

            """if (max_index != 0):
                ymin = int(max(1,(boxes[max_index][0] * imH)))
                xmin = int(max(1,(boxes[max_index][1] * imW)))
                ymax = int(min(imH,(boxes[max_index][2] * imH)))
                xmax = int(min(imW,(boxes[max_index][3] * imW)))
                self.object_x = float(xmin+xmax/2)
                self.object_y = float(ymin+ymax/2)

            else:
                Stop = '#0#0#0#0\n'
                self.sendData(cmd.CMD_MOTOR+Stop)
                self.sendData(cmd.CMD_MODE+"#"+'six'+"#"+'-2'+"\n")"""

            # Draw framerate in corner of frame
            cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
        
        cv2.imwrite('video.jpg', frame)
    
    def color_detect(self,img,color): # Note that RGB is backwards in this function. Instead, it is BGR, so invert where you put your values.
        """try:
            hvsframe = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            hsc_dic = {"red":(np.array([136, 87, 111], np.uint8),np.array([180, 255, 255], np.uint8)),
                       "green":(np.array([45, 100, 72], np.uint8),np.array([90, 255, 255], np.uint8)),
                       "blue":(np.array([94, 80, 2], np.uint8),np.array([120, 255, 255], np.uint8)),
                       "yellow":(np.array([25, 50, 70], np.uint8),np.array([35, 255, 255], np.uint8))}

            limits = hsc_dic[color.lower()]

            mask = cv2.inRange(hvsframe, limits[0], limits[1])

            res = cv2.bitwise_and(img,img, mask = mask)

            self.object_detect(img,res)

        except: 
            cv2.imwrite('video.jpg',img)
            pass"""

        
        """# Convert the img in 
        # BGR(RGB color space) to
        # HSV(hue-saturation-value)
        # color space
        hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  
        # Set range for red color and 
        # define mask
        red_lower = np.array([136, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
  
        # Set range for green color and 
        # define mask
        green_lower = np.array([25, 52, 72], np.uint8)
        green_upper = np.array([102, 255, 255], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
  
        # Set range for blue color and
        # define mask
        blue_lower = np.array([94, 80, 2], np.uint8)
        blue_upper = np.array([120, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

        # Set range for yellow color and
        # define mask
        yellow_lower = np.array([20, 100, 150], np.uint8)
        yellow_upper = np.array([40, 255, 255], np.uint8)
        yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
      
        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between img and mask determines
        # to detect only that particular color
        kernel = np.ones((5, 5), "uint8")
      
        # For red color
        red_mask = cv2.dilate(red_mask, kernel)
        res_red = cv2.bitwise_and(img, img, mask = red_mask)
      
        # For green color
        green_mask = cv2.dilate(green_mask, kernel)
        res_green = cv2.bitwise_and(img, img, mask = green_mask)
      
        # For blue color
        blue_mask = cv2.dilate(blue_mask, kernel)
        res_blue = cv2.bitwise_and(img, img, mask = blue_mask)

        # For yellow color
        yellow_mask = cv2.dilate(yellow_mask, kernel)
        res_yellow = cv2.bitwise_and(img, img, mask = yellow_mask)
   
        # Creating contour to track red color
        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
              
                cv2.putText(img, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))    
  
        # Creating contour to track green color
        contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y),  (x + w, y + h), (0, 255, 0), 2)
              
                cv2.putText(img, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
  
        # Creating contour to track blue color
        contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
              
                cv2.putText(img, "Blue Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))
        
        # Creating contour to track yellow color
        contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
              
                cv2.putText(img, "Yellow Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255))
        
        cv2.imwrite('video.jpg',img)
        cv2.imwrite('red.jpg',res_red)
        cv2.imwrite('green.jpg',res_green)
        cv2.imwrite('blue.jpg',res_blue)
        cv2.imwrite('yellow.jpg',res_yellow)"""

    def streaming(self,ip,objects):
        stream_bytes = b' '
        try:
            self.client_socket.connect((ip, 8000))
            self.connection = self.client_socket.makefile('rb')
        except:
            #print "command port connect failed"
            pass
        while True:
            try:
                stream_bytes= self.connection.read(4) 
                leng=struct.unpack('<L', stream_bytes[:4])
                jpg=self.connection.read(leng[0])
                if self.IsValidImage4Bytes(jpg):
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if self.video_Flag:
                        self.object_detect(image,objects)
                        # self.color_detect(image,self.color)
                        self.video_Flag=False
            except Exception as e:
                print (e)
                break
                  
    def sendData(self,s):
        if self.connect_Flag:
            self.client_socket1.send(s.encode('utf-8'))

    def recvData(self):
        data=""
        try:
            data=self.client_socket1.recv(1024).decode('utf-8')
        except:
            pass
        return data

    def socket1_connect(self,ip):
        try:
            self.client_socket1.connect((ip, 5000))
            self.connect_Flag=True
            print ("Connection Successful !")
        except Exception as e:
            print ("Connect to server Failed!: Server IP is right? Server is opened?")
            self.connect_Flag=False

if __name__ == '__main__':
    pass

