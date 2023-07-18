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
import time

class VideoStreaming:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
        self.video_Flag=True
        self.connect_Flag=False
        self.face_x=0
        self.face_y=0
        self.lastSeen = -1
        self.redArea = 0
        self.blueArea = 0
        self.greenArea = 0
        self.yellowArea = 0
        self.current_color = ''

        self.color = ''
        self.TargetFound = False
        
        

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
            print("Stop TCP")

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
                print("is valid image")
        return bValid

    def face_detect(self,img):
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
            MODEL_NAME = 'Sample_TFLite_model'
            GRAPH_NAME = 'detect.tflite'
            LABELMAP_NAME = 'labelmap.txt'
            min_conf_threshold = 0.3
            
            imW, imH = int(400), int(300)

            CWD_PATH = os.getcwd()

            PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

            PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

            frame = img.copy()

            with open(PATH_TO_LABELS, 'r') as f:
                labels = [line.strip() for line in f.readlines()]

            # Have to do a weird fix for label map if using the COCO "starter model" from
            # https://www.tensorflow.org/lite/models/object_detection/overview
            # First label is '???', which has to be removed.
            if labels[0] == '???':
                del(labels[0])

            interpreter = tf.lite.Interpreter(model_path=PATH_TO_CKPT)

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
                boxes_idx, classes_idx, scores_idx = 0, 1, 2

            # Initialize frame rate calculation
            frame_rate_calc = 30

            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            frame_resized = cv2.resize(frame_rgb, (width, height))
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

            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                # Found desired object with decent confidence
                if (((labels[int(classes[i])] == "vase") or (labels[int(classes[i])] == "apple") or (labels[int(classes[i])] == "sports ball") or (labels[int(classes[i])] == "toilet") or (labels[int(classes[i])] == "frisbee") or (labels[int(classes[i])] == "cup") or (labels[int(classes[i])] == "orange"))):
                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))
                    
                    # Draw label
                    object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % ("Ball", int(scores[i]*100)) # Example: 'person: 72%'
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
                self.face_x = float(xmin+xmax/2)
                self.face_y = float(ymin+ymax/2)

            else:
                Stop = '#0#0#0#0\n'
                self.sendData(cmd.CMD_MOTOR+Stop)
                self.sendData(cmd.CMD_MODE+"#"+'six'+"#"+'-2'+"\n")

            # Draw framerate in corner of frame
            cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
            self.color_detect(img)            
        cv2.imwrite('video.jpg', frame)
            
            
    def color_detect(self,img):
        hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        red_lower = np.array([136,87,111], np.uint8)
        red_upper = np.array([180,255,255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    
        green_lower = np.array([45,120,100], np.uint8)
        green_upper = np.array([90,255,255], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    
        blue_lower = np.array([90,150,150], np.uint8)
        blue_upper = np.array([110,255,255], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
        
        yellow_lower = np.array([25,50,70],np.uint8)
        yellow_upper = np.array([39,255,255], np.uint8)
        yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)


        kernel = np.ones((5, 5), "uint8")


        red_mask = cv2.dilate(red_mask, kernel)
        res_red = cv2.bitwise_and(img, img,
                            mask = red_mask)
    
        green_mask = cv2.dilate(green_mask, kernel)
        res_green = cv2.bitwise_and(img, img,
                            mask = green_mask)
    
        blue_mask = cv2.dilate(blue_mask, kernel)
        res_blue = cv2.bitwise_and(img, img,
                            mask = blue_mask)
        
        yellow_mask = cv2.dilate(yellow_mask, kernel)
        res_yellow = cv2.bitwise_and(img, img,
                            mask = yellow_mask)
    
        contours, hierarchy = cv2.findContours(red_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
    
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 3000:
                self.lastSeen = 0
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y),
                                    (x + w, y + h),
                                    (0, 0, 255), 2)
            
                cv2.putText(img, "Red Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))          
        contours, hierarchy = cv2.findContours(green_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
    
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 3000:
                self.lastSeen = 1
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y),
                                    (x + w, y + h),
                                    (0, 255, 0), 2)
            
                cv2.putText(img, "Green Colour", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (0, 255, 0))
            
        contours, hierarchy = cv2.findContours(blue_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
    
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 3000:
                self.lastSeen = 2
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y),
                                    (x + w, y + h),
                                    (255, 0, 0), 2)
            
                cv2.putText(img, "Blue Colour", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (255, 0, 0))

        contours, hierarchy = cv2.findContours(yellow_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
    
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 3000:
                self.lastSeen = 3
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y),
                                    (x + w, y + h),
                                    (35, 255, 255), 2)
            
                cv2.putText(img, "Yellow Colour", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (35, 255, 255))
        cv2.imwrite('video.jpg',img)
        cv2.imwrite("blue.jpg", res_blue)
        cv2.imwrite("red.jpg", res_red)
        cv2.imwrite("green.jpg", res_green)
        cv2.imwrite("yellow.jpg", res_yellow)
    
    
    def colorandball(self,img,color):
        self.color = color
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
            hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            low = []
            upp = []
            
            print(self.color)
            
            colorball = ''
            
            if self.color == 'Red':
                low = [136,87,111]
                upp = [180,255,255]
                colorball = 'Red Ball'         
                
            if self.color == 'Green':
                low = [45,120,100]
                upp = [90,255,255]
                colorball = 'Green Ball'
            
            if self.color == 'Blue':
                low = [90,150,150]
                upp = [110,255,255]
                colorball = 'Blue Ball'
                
            if self.color == 'Yellow':
                low = [25,50,70]
                upp = [39,255,255]
                colorball = 'Yellow Ball'

            
                
            lower = np.array(low, np.uint8)
            upper = np.array(upp, np.uint8)
            
            
            _mask = cv2.inRange(hsvFrame, lower, upper)
            
            kernel = np.ones((5, 5), "uint8")
            
            _mask = cv2.dilate(_mask,kernel)
            res = cv2.bitwise_and(img,img, mask = _mask)
            
                
            MODEL_NAME = 'Sample_TFLite_model'
            GRAPH_NAME = 'detect.tflite'
            LABELMAP_NAME = 'labelmap.txt'
            min_conf_threshold = .3
            
            imW, imH = int(400), int(300)

            CWD_PATH = os.getcwd()

            PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

            PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

            frame = img.copy()

            with open(PATH_TO_LABELS, 'r') as f:
                labels = [line.strip() for line in f.readlines()]

            # Have to do a weird fix for label map if using the COCO "starter model" from
            # https://www.tensorflow.org/lite/models/object_detection/overview
            # First label is '???', which has to be removed.
            if labels[0] == '???':
                del(labels[0])

            interpreter = tf.lite.Interpreter(model_path=PATH_TO_CKPT)

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
                boxes_idx, classes_idx, scores_idx = 0, 1, 2

            # Initialize frame rate calculation
            frame_rate_calc = 30

            frame_rgb = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)

            frame_resized = cv2.resize(frame_rgb, (width, height))
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

            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                # Found desired object with decent confidence
                if (((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)) and ((labels[int(classes[i])] == "vase") or (labels[int(classes[i])] == "apple") or (labels[int(classes[i])] == "sports ball") or (labels[int(classes[i])] == "toilet") or (labels[int(classes[i])] == "frisbee") or (labels[int(classes[i])] == "cup") or (labels[int(classes[i])] == "orange"))):
                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))
                    
                    # Draw label
                    object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (colorball, int(scores[i]*100)) # Example: 'person: 72%'
                    self.TargetFound = True
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
                self.face_x = float(xmin+xmax/2)
                self.face_y = float(ymin+ymax/2)

            else:
                Stop = '#0#0#0#0\n'
                self.sendData(cmd.CMD_MOTOR+Stop)
                self.sendData(cmd.CMD_MODE+"#"+'six'+"#"+'-2'+"\n")

            # Draw framerate in corner of frame
            cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
            self.color_detect(img)            
        cv2.imwrite('video.jpg', frame)
        
            
    # def HyperspaceTracking(self):
    #     self.c=self.Color.text()
    #     Random = self.c.split(",")
        
    #     stream_bytes= self.connection.read(4)
    #     leng=struct.unpack('<L', stream_bytes[:4])
    #     jpg=self.connection.read(leng[0])
        
    #     if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
    #         image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
    #         for i in Random:
    #             self.colorandball(image,i)
                        
        
    def streaming(self,ip):
        stream_bytes = b' '
        try:
            self.client_socket.connect((ip, 8000))
            self.client_socket.settimeout(5)
            self.connection = self.client_socket.makefile('rb')
        except Exception as e:
            print(e)
            print ("command port connect failed")
        while True:
            # try:
                stream_bytes= self.connection.read(4)
                # print("done reading")
                leng=struct.unpack('<L', stream_bytes[:4])
                jpg=self.connection.read(leng[0])
                # print("here1")
                if self.IsValidImage4Bytes(jpg):
                            image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                            if self.video_Flag:
                                # self.face_detect(image)
                                # self.color_detect(image)
                                # self.c=self.Color.text()
                                # self.Random = self.Color.split(",")
                                # print(Random)
                                # self.colorandball(image,self.current_color)
                                # print(self.Color)
                                try:
                                    self.colorandball(image,self.color)
                                except:
                                    self.color_detect(image)
                                # self.colorandball(image,'Red')
                                # self.colorandball(image,'green')
                                # self.colorandball(image,'blue',Randy)
                                # self.colorandball(image,'yellow')
                            self.video_Flag=False
            # except Exception as e:
            #     print (e)
            #     print("streaming")
            #     break
                 
    def sendData(self,s):
        if self.connect_Flag:
            self.client_socket1.send(s.encode('utf-8'))


    def recvData(self):
        data=""
        try:
            data=self.client_socket1.recv(1024).decode('utf-8')
        except:
            print("recvData")
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

        
       