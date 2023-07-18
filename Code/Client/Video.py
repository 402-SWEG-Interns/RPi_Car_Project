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
        self.face_x=0
        self.face_y=0
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

    def find_bottle(self,img):
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
            MODEL_NAME = 'Sample_TFLite_model'
            LABELMAP_NAME = 'labelmap.txt'
            YOLOV5_GRAPH_NAME = 'allbest.pt'

            min_conf_threshold = 0.2
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

            # Use yolov5
            model = yolov5.load(PATH_TO_YOLOV5_GRAPH)

            # set model parameters
            model.conf = 0.25  # NMS confidence threshold
            model.iou = 0.45  # NMS IoU threshold
            model.agnostic = False  # NMS class-agnostic
            model.multi_label = True # NMS multiple labels per box
            model.max_det = 1000  # maximum number of detections per image

            results = model(frame) 
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

    def streaming(self,ip):
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
                        if self.video_Flag:
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

