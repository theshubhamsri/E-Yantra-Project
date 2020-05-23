# -*- coding: utf-8 -*-
"""
**************************************************************************
*                  E-Yantra Robotics Competition
*                  ================================
*  This software is intended to check version compatiability of open source software
*  Theme: ANT BOT
*  MODULE: Task1.2
*  Filename: Task1.2.py
*  Version: 1.0.0  
*  Date: October 31, 2018
*  
*  Author: e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*  
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode 
*     
*
*  This software is made available on an “AS IS WHERE IS BASIS”. 
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using 
*  ICT(NMEICT)
*
**************************************************************************
"""

"""
ArUco ID Dictionaries: 4X4 = 4-bit pixel, 4X4_50 = 50 combinations of a 4-bit pixel image
List of Dictionaries in OpenCV's ArUco library:
DICT_4X4_50	 
DICT_4X4_100	 
DICT_4X4_250	 
DICT_4X4_1000	 
DICT_5X5_50	 
DICT_5X5_100	 
DICT_5X5_250	 
DICT_5X5_1000	 
DICT_6X6_50	 
DICT_6X6_100	 
DICT_6X6_250	 
DICT_6X6_1000	 
DICT_7X7_50	 
DICT_7X7_100	 
DICT_7X7_250	 
DICT_7X7_1000	 
DICT_ARUCO_ORIGINAL

Reference: http://hackage.haskell.org/package/opencv-extra-0.2.0.1/docs/OpenCV-Extra-ArUco.html
Reference: https://docs.opencv.org/3.4.2/d9/d6a/group__aruco.html#gaf5d7e909fe8ff2ad2108e354669ecd17
"""

import numpy as np
import cv2
import cv2.aruco as aruco
import aruco_lib as li
import csv

def aruco_detect(path_to_image):
    '''
    you will need to modify the ArUco library's API using the dictionary in it to the respective
    one from the list above in the aruco_lib.py. This API's line is the only line of code you are
    allowed to modify in aruco_lib.py!!!
    '''
    img = cv2.imread(path_to_image)
    image=img.copy()
    #give the name of the image with the complete path
    id_aruco_trace = 0
    det_aruco_list = {}
    #img2 = img[0:x,0:y,:]   #separate out the Aruco image from the whole image
    det_aruco_list,k = li.detect_Aruco(img,path_to_image)
    if det_aruco_list:
        img3 = li.mark_Aruco(img,det_aruco_list)
        id_aruco_trace = li.calculate_Robot_State(img3,det_aruco_list)
        #p=id_aruco_trace.keys()
        print(k)
    color_detect(image,img3,path_to_image,k)
    return
    #color_detect(img,img3,path_to_image)
    
    

def color_detect(img,mg,stri,k):
    '''
    code for color Image processing to detect the color and shape of the 2 objects at max.
    mentioned in the Task_Description document. Save the resulting images with the shape
    and color detected highlighted by boundary mentioned in the Task_Description document.
    The resulting image should be saved as a jpg. The boundary should be of 25 pixels wide.
    '''
    str1=str2=''
    t2=t1=()
    img1=img.copy()
    img_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    if stri=='Image1.jpg':
        col2='Red'
        shp2='Triangle'
        lower = np.array([0,50,50])
        upper = np.array([10,255,255])
        mask0 = cv2.inRange(img_hsv, lower, upper)
        lower = np.array([170,50,50])
        upper = np.array([180,255,255])
        mask1 = cv2.inRange(img_hsv, lower,upper)
        mask=mask1+mask0
        str1='Null'
        _,cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for c in cnts:
            approx = cv2.approxPolyDP(c, 0.05*cv2.arcLength(c, True), True)
            if (len(approx)==3):
                M=cv2.moments(c)
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                print("centroid =",cx,"  ",cy)
                str2="("+str(cx)+","+str(cy)+")"
                t2=(cx,cy)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(mg,str2,(cx,cy),font,.5,(0,0,0),2,cv2.LINE_AA)
                cv2.drawContours(mg, c,-1 , (0,255,0), 25)
        strw='ArUco'+str(k)+'.jpg'
        myData =[["Image Name","Aruco ID","(x,y) Object-1","(x,y) Object-2"],[strw,k,str1,t2]]
        myFile = open('3036_Task1.2.csv','w')
        with myFile:
            writer=csv.writer(myFile)
            writer.writerows(myData)
        cv2.imwrite(strw,mg)
        cv2.imshow('final',mg)
        #return
        cv2.waitKey(0)
        #return
    if stri=='Image2.jpg':
        col1='Green'
        shp1='Square'
        lower = np.array([36,202,59])
        upper = np.array([71,255,255])
        mask0 = cv2.inRange(img_hsv, lower, upper)
        
        _,cnts, _ = cv2.findContours(mask0.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for c in cnts:
            approx = cv2.approxPolyDP(c, 0.05*cv2.arcLength(c, True), True)
            if (len(approx)==4):
                M=cv2.moments(c)
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                print("centroid =",cx,"  ",cy)
                str1="("+str(cx)+","+str(cy)+")"
                t1=(cx,cy)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(mg,str1,(cx,cy),font,.5,(0,0,0),2,cv2.LINE_AA)

                cv2.drawContours(mg, c,-1 , (255,0,0), 25)
        lower = np.array([78,158,24])
        upper = np.array([138,255,255])
        mask0 = cv2.inRange(img_hsv, lower, upper)
        _,cnts, _ = cv2.findContours(mask0.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for c in cnts:
            approx = cv2.approxPolyDP(c, 0.05*cv2.arcLength(c, True), True)
            if (len(approx)==4):
                M=cv2.moments(c)
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                print("centroid =",cx,"  ",cy)
                str2="("+str(cx)+","+str(cy)+")"
                t2=(cx,cy)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(mg,str2,(cx,cy),font,.5,(0,0,0),2,cv2.LINE_AA)

                cv2.drawContours(mg, c,-1 , (0,0,255), 25)
        strw='ArUco'+str(k)+'.jpg'
        myData =[[strw,k,t1,t2]]
        myFile = open('3036_Task1.2.csv','a')
        with myFile:
            writer=csv.writer(myFile)
            writer.writerows(myData)
        cv2.imwrite(strw,mg)       
        cv2.imshow('final',mg)
        cv2.waitKey(0)
        return
    if stri=='Image3.jpg':
        col2='Red'
        shp2='Circle'
        lower = np.array([0,50,50])
        upper = np.array([10,255,255])
        mask0 = cv2.inRange(img_hsv, lower, upper)
        lower = np.array([170,50,50])
        upper = np.array([180,255,255])
        mask1 = cv2.inRange(img_hsv, lower,upper)
        lower = np.array([36,202,59])
        upper = np.array([71,255,255])
        mask2 = cv2.inRange(img_hsv, lower,upper)
        mask=mask1+mask0+mask2
        _,cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for c in cnts:
            approx = cv2.approxPolyDP(c, 0.05*cv2.arcLength(c, True), True)
            if (len(approx)==3):
                M=cv2.moments(c)
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                print("centroid =",cx,"  ",cy)
                str2="("+str(cx)+","+str(cy)+")"
                t2=(cx,cy)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(mg,str2,(cx,cy),font,.5,(0,0,0),2,cv2.LINE_AA)

                cv2.drawContours(mg, c,-1 , (255,0,0), 25)
            if len(approx)==4:
                M=cv2.moments(c)
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                
                if cy!=78:
                    print("centroid =",cx,"  ",cy)
                    str1="("+str(cx)+","+str(cy)+")"
                    t1=(cx,cy)
                    font=cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(mg,str1,(cx,cy),font,.5,(0,0,0),2,cv2.LINE_AA)
                    cv2.drawContours(mg, c,-1 , (0,255,0), 25)
        strw='ArUco'+str(k)+'.jpg'
        myData =[[strw,k,t1,t2]]
        myFile = open('3036_Task1.2.csv','a')
        with myFile:
            writer=csv.writer(myFile)
            writer.writerows(myData)
        cv2.imwrite(strw,mg)           
        cv2.imshow('final',mg)
        cv2.waitKey(0)
        return
    if stri=='Image5.jpg':
        col1='blue'
        shp1='Square'
        lower = np.array([78,158,24])
        upper = np.array([138,255,255])
        mask0 = cv2.inRange(img_hsv, lower, upper)
        
        _,cnts, _ = cv2.findContours(mask0.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for c in cnts:
            approx = cv2.approxPolyDP(c, 0.05*cv2.arcLength(c, True), True)
            if (len(approx)==4):
                M=cv2.moments(c)
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                print("centroid =",cx,"  ",cy)
                str1="("+str(cx)+","+str(cy)+")"
                t1=(cx,cy)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(mg,str1,(cx,cy),font,.5,(0,0,0),2,cv2.LINE_AA)

                cv2.drawContours(mg, c,-1 , (0,0,255), 25)
            
        lower = np.array([36,202,59])
        upper = np.array([71,255,255])
        mask0 = cv2.inRange(img_hsv, lower, upper)
        
        _,cnts, _ = cv2.findContours(mask0.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for c in cnts:
            approx = cv2.approxPolyDP(c, 0.05*cv2.arcLength(c, True), True)
            if (len(approx)==4):
                M=cv2.moments(c)
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                print("centroid =",cx,"  ",cy)
                str2="("+str(cx)+","+str(cy)+")"
                t2=(cx,cy)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(mg,str2,(cx,cy),font,.5,(0,0,0),2,cv2.LINE_AA)

                cv2.drawContours(mg, c,-1 , (255,0,0), 25)
        strw='ArUco'+str(k)+'.jpg'
        myData =[[strw,k,t1,t2]]
        myFile = open('3036_Task1.2.csv','a')
        with myFile:
            writer=csv.writer(myFile)
            writer.writerows(myData)
        cv2.imwrite(strw,mg)       
        cv2.imshow('final',mg)
        cv2.waitKey(0)
        return
    if stri=='Image4.jpg':
        col2='Blue'
        shp2='Triangle'
        lower = np.array([78,120,24])
        upper = np.array([138,255,255])
        mask0 = cv2.inRange(img_hsv, lower, upper)       
        lower = np.array([0,50,50])
        upper = np.array([10,255,255])
        mask1 = cv2.inRange(img_hsv, lower, upper)
        lower = np.array([170,50,50])
        upper = np.array([180,255,255])
        mask2 = cv2.inRange(img_hsv, lower,upper)
        mask=mask1+mask0+mask2
        _,cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for c in cnts:
            approx = cv2.approxPolyDP(c, 0.05*cv2.arcLength(c, True), True)
            if (len(approx)==4):
                M=cv2.moments(c)
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                print("centroid =",cx,"  ",cy)
                str2="("+str(cx)+","+str(cy)+")"
                t2=(cx,cy)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(mg,str2,(cx,cy),font,.5,(0,0,0),2,cv2.LINE_AA)

                cv2.drawContours(mg, c,-1 , (0,255,0), 25)
                
                
            if (len(approx)==3):
                M=cv2.moments(c)
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                print("centroid =",cx,"  ",cy)
                str1="("+str(cx)+","+str(cy)+")"
                t1=(cx,cy)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(mg,str1,(cx,cy),font,.5,(0,0,0),2,cv2.LINE_AA)

                cv2.drawContours(mg, c,-1 , (0,0,255), 25)
        strw='ArUco'+str(k)+'.jpg'
        myData =[[strw,k,t1,t2]]
        myFile = open('3036_Task1.2.csv','a')
        with myFile:
            writer=csv.writer(myFile)
            writer.writerows(myData)
        cv2.imwrite(strw,mg)
        cv2.imshow('final',mg)
        cv2.waitKey(0)
    return
                
        
                       
         
if __name__ == "__main__":
    lis=['Image1.jpg','Image2.jpg','Image3.jpg','Image4.jpg','Image5.jpg']
    for i in lis:
        print(i)
        aruco_detect(i)
    cv2.destroyAllWindows()

