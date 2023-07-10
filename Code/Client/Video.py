#!/usr/bin/python 
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import socket
import io
import sys
import struct
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

        self.lastSeen = -1
        # self.redArea = 0
        # self.blueArea = 0
        # self.greenArea = 0
        # self.yellowArea = 0
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

    def face_detect(self,img):
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray,1.3,5)
            if len(faces)>0 :
                for (x,y,w,h) in faces:
                    self.face_x=float(x+w/2.0)
                    self.face_y=float(y+h/2.0)
                    img= cv2.circle(img, (int(self.face_x),int(self.face_y)), int((w+h)/4), (0, 255, 0), 2)
            else:
                self.face_x=0
                self.face_y=0
        cv2.imwrite('video.jpg',img)
        
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
                                self.ColorDetect(image) ##9483273984329849238379
                                # self.face_detect(image)
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

    def ColorDetect(self,img): 
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'): 

            hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 




            red_lower = np.array([136,87,111], np.uint8) 

            red_upper = np.array([180,255,255], np.uint8) 

            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 




            green_lower = np.array([45,100,72], np.uint8) 

            green_upper = np.array([90,255,255], np.uint8) 

            green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 




            blue_lower = np.array([90,150,150], np.uint8) 

            blue_upper = np.array([110,255,255], np.uint8) 

            blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 




            yellow_lower = np.array([21,100,100], np.uint8) 

            yellow_upper = np.array([30,255,255], np.uint8) 

            yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper) 




            kernel = np.ones((5,5), "uint8") 




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

            




            contours, hiearchy = cv2.findContours(red_mask, 

                                                cv2.RETR_TREE, 

                                                cv2.CHAIN_APPROX_SIMPLE) 

            for pic, contour in enumerate(contours): 
                area = cv2.contourArea(contour) 

                if(area > 3000): 
                    self.lastSeen = 0
                    x,y,w,h = cv2.boundingRect(contour) 

                    img = cv2.rectangle(img, (x,y), 

                                        (x + w, y + h), 

                                        (0,0,255), 2) 

                    cv2.putText(img, "Red Color", (x,y), 

                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, 

                                (0,0,255)) 

                    

            contours, hiearchy = cv2.findContours(green_mask, 

                                                cv2.RETR_TREE, 

                                                cv2.CHAIN_APPROX_SIMPLE) 

            for pic, contour in enumerate(contours): 
                area = cv2.contourArea(contour) 

                if(area > 3000): 
                    self.lastSeen = 1
                    x,y,w,h = cv2.boundingRect(contour) 

                    img = cv2.rectangle(img, (x,y), 

                                        (x + w, y + h), 

                                        (0,255,0), 2) 

                    cv2.putText(img, "Green Color", (x,y), 

                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, 

                                (0,255,0)) 

                    




            contours, hiearchy = cv2.findContours(blue_mask, 

                                                cv2.RETR_TREE, 

                                                cv2.CHAIN_APPROX_SIMPLE) 

            for pic, contour in enumerate(contours): 
                area = cv2.contourArea(contour) 

                if(area > 3000): 
                    self.lastSeen = 2
                    x,y,w,h = cv2.boundingRect(contour) 

                    img = cv2.rectangle(img, (x,y), 

                                        (x + w, y + h), 

                                        (255,0,0), 2) 

                    cv2.putText(img, "Blue Color", (x,y), 

                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, 

                                (255,0,0)) 

                    

            contours, hiearchy = cv2.findContours(yellow_mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

            for pic, contour in enumerate(contours): 
                area = cv2.contourArea(contour) 
                if(area > 3000): 
                    self.lastSeen = 3
                    x,y,w,h = cv2.boundingRect(contour)
                    img = cv2.rectangle(img, (x,y), (x + w, y + h), (0,255,255), 2) 
                    cv2.putText(img, "Yellow Color", (x,y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                                (0,255,255)) 
                    
            cv2.imshow("Multiple Color Detection in Real-Time", img) 
            cv2.imwrite('video.jpg', img) 
            
        

 

if __name__ == '__main__':
    pass

