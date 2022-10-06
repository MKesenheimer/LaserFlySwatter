from types import NoneType
import cv2 as cv
import numpy as np 
import time
import math

cap = cv.VideoCapture(2)#my webcam(2),default(0)

parameter1=100
def update1(value):
    global parameter1
    parameter1=value

parameter2=100
def update2(value):
    global parameter2
    parameter2=value

parameter3=100
def update3(value):
    global parameter3
    parameter3=value




cv.namedWindow("frame")
cv.createTrackbar('Param1', "frame", 0, 500, update1)
cv.createTrackbar('Threshhold(circles)', "frame", 0, 500, update2)
cv.createTrackbar('ValueMaskLower', "frame", 0, 255, update3)

while(1):
    # Take each frame
    _, frame = cap.read()
    
    # Convert BGR to HSV
    #hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    
    
    #hsv_c = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    
    # define range of blue color in HSV
    lower = np.array([parameter3,parameter3,parameter3])
    upper = np.array([255,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(frame, lower, upper)
    
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
    cv.imshow("res",res)

    #cv.imshow('res',res)
    #cv.imshow('mask',mask)
    
    img = cv.medianBlur(res,3)
    cimg = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    circles = cv.HoughCircles(cimg,cv.HOUGH_GRADIENT,2,10,param1=parameter1,param2=parameter2,minRadius=5,maxRadius=200)
    
    if type(circles) != type(None):
        circles = np.uint16(np.around(circles))
        i=circles[0,0]
        # draw the outer circle
        cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)


        cv.imshow('cimg',cimg)
    cv.imshow("edges", cv.Canny(img,parameter1/2,parameter1))
    cv.imshow('frame',frame)
    

    
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv.destroyAllWindows()
