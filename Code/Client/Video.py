#!/usr/bin/python 
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import socket
import io
import sys
import struct
import yolov5
import tensorflow as tf
import os
from PIL import Image
from multiprocessing import Process
from Command import COMMAND as cmd

class VideoStreaming:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
        self.video_Flag=True
        self.connect_Flag=False
        self.face_x=0
        self.face_y=0
        self.ball_x=0.0
        self.ball_y=0.0
        self.current_color = "blue"
        self.found_ball=False

        self.MODEL_NAME = 'Sample_TFLite_model'
        self.LABELMAP_NAME = 'labelmap.txt'
        self.YOLOV5_GRAPH_NAME = 'best.pt'

        self.min_conf_threshold = 0.2
        self.imW, self.imH = int(400), int(300)

        self.CWD_PATH = os.getcwd()

        self.PATH_TO_LABELS = os.path.join(self.CWD_PATH,self.MODEL_NAME,self.LABELMAP_NAME)

        self.PATH_TO_YOLOV5_GRAPH = os.path.join(self.CWD_PATH,self.MODEL_NAME,self.YOLOV5_GRAPH_NAME)

        self.model.conf = 0.25  # NMS confidence threshold
        self.model.iou = 0.45  # NMS IoU threshold
        self.model.agnostic = False  # NMS class-agnostic
        self.model.multi_label = True # NMS multiple labels per box
        self.model.max_det = 1000  # maximum number of detections per image

        self.model = yolov5.load(self.PATH_TO_YOLOV5_GRAPH)

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

    def face_detect(self,img, mask):
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
            MODEL_NAME = 'Sample_TFLite_model'
            GRAPH_NAME = 'detect.tflite'
            LABELMAP_NAME = 'labelmap.txt'
            min_conf_threshold = 0.285
            
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

            frame_rgb = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

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
                if ((scores[i] > max_score) and (scores[i] > min_conf_threshold) and (scores[i] <= 1.0) and (labels[int(classes[i])] == 'sports ball' or labels[int(classes[i])] == 'apple')):
                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                    self.found_ball = True
                    self.frame_count_noball = 0
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))
                    
                    # Draw label
                    object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                    label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                    cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                    cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))
                    self.ball_x = float(xmin+xmax/2)
                    self.ball_y = float(ymin+ymax/2)
                    #print(self.ball_x)
                   

                    # Record current max
                    max_score = scores[i]
                    max_index = i

            
                else:
            
                    self.frame_count_noball += 1
                    if self.frame_count_noball > 30:
                        self.found_ball = False

            if (max_index != 0):
                ymin = int(max(1,(boxes[max_index][0] * imH)))
                xmin = int(max(1,(boxes[max_index][1] * imW)))
                ymax = int(min(imH,(boxes[max_index][2] * imH)))
                xmax = int(min(imW,(boxes[max_index][3] * imW)))
                self.ball_x = float(xmin+xmax/2)
                self.ball_y = float(ymin+ymax/2)
                #print("[ {} , {} ]".format(self.ball_x,self.ball_y))

            """else:
                Stop = '#0#0#0#0\n'
                self.sendData(cmd.CMD_MOTOR+Stop)
                self.sendData(cmd.CMD_MODE+"#"+'six'+"#"+'-2'+"\n")"""

            # Draw framerate in corner of frame
            cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
        
        cv2.imwrite('video.jpg', frame)


        def find_bottle(self,img):
            if sys.platform.startswith('win') or sys.platform.startswith('darwin'):

                frame = img.copy()
                with open(PATH_TO_LABELS, 'r') as f:
                    labels = [line.strip() for line in f.readlines()]

                # Have to do a weird fix for label map if using the COCO "starter model" from
                # https://www.tensorflow.org/lite/models/object_detection/overview
                # First label is '???', which has to be removed.
                if labels[0] == '???':
                    del(labels[0])

                results = self.model(frame) 
                predictions = results.pred[0].cpu()
                boxes = predictions[:, :4]
                scores = predictions[:, 4]
                classes = predictions[:, 5]
                results.render() 

                # Initialize frame rate calculation
                frame_rate_calc = 30

                frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                frame_resized = cv2.resize(frame_rgb, (imW, imH))
                input_data = np.expand_dims(frame_resized, axis=0)

                max_score = 0
                max_index = 0

                # Loop over all detections and draw detection box if confidence is above minimum threshold
                for i in range(len(scores)):
                    curr_score = scores[i].numpy()
                    # Found desired object with decent confidence
                    if ( (scores[i] > max_score) and (scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                        # Get bounding box coordinates and draw box
                        # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                        ymin = int(max(1,(boxes[i][0] * imH)))
                        xmin = int(max(1,(boxes[i][1] * imW)))
                        ymax = int(min(imH,(boxes[i][2] * imH)))
                        xmax = int(min(imW,(boxes[i][3] * imW)))

                        #find bounding box center
                        cx = (xmax + xmin)/ 2 
                        cy = (ymax + ymin)/ 2 

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

                # Draw framerate in corner of frame
                cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)

            cv2.imwrite('video.jpg', frame)


        
    def color_detect(self, imageFrame, color):
        
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        hsv_dict= {"red": (np.array([111, 45, 35], np.uint8), np.array([180, 255, 255], np.uint8)),
                    "blue":(np.array([87, 60, 45], np.uint8),np.array([110, 255, 255], np.uint8)),
                    "green": (np.array([36, 60, 40], np.uint8), np.array([86, 255, 255], np.uint8)), 
                    "yellow" :(np.array([10, 70, 70], np.uint8), np.array([35, 255, 255], np.uint8))}
        try:
            limits = hsv_dict[color.lower()]
        except:
            self.found_ball = False
            cv2.imwrite('video.jpg', imageFrame)
            return

        mask = cv2.inRange(hsvFrame, limits[0], limits[1])

        res = cv2.bitwise_and(imageFrame, imageFrame, mask = mask)
        cv2.imwrite("red_res.jpg", res)
        self.face_detect(imageFrame, res)
    

            

    def streaming(self,ip):
        stream_bytes = b' '
        try:
            self.client_socket.connect((ip, 8000))
            self.connection = self.client_socket.makefile('rb')
        except:
            print("command port connect failed")
            pass
        while True:
            try:
                stream_bytes= self.connection.read(4) 
                leng=struct.unpack('<L', stream_bytes[:4])
                jpg=self.connection.read(leng[0])
                if self.IsValidImage4Bytes(jpg):
                            image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                            if self.video_Flag:
                                #self.face_detect(image)
                                self.find_bottle(image)
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
