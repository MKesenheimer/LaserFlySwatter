from types import NoneType
import cv2 as cv
import numpy as np 
import time
import math

cap = cv.VideoCapture(2)#my webcam(2),default(0)

while(1):
    # Take each frame
    _, frame = cap.read()
    
    # Convert BGR to HSV
    #hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    
    
    #hsv_c = cv.cvtColor(change, cv.COLOR_BGR2HSV)
    
    
    # define range of blue color in HSV
    #lower = np.array([245,245,245])
    #upper = np.array([255,255,255])

    # Threshold the HSV image to get only blue colors
    #mask = cv.inRange(change, lower, upper)
    
    # Bitwise-AND mask and original image
    #res = cv.bitwise_and(change,change, mask= mask)


    #cv.imshow('res',res)
    #cv.imshow('mask',mask)
    parameter1=100
    img = cv.medianBlur(frame,5)
    cimg = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    circles = cv.HoughCircles(cimg,cv.HOUGH_GRADIENT,2,30,param1=parameter1,param2=175,minRadius=5,maxRadius=200)
    
    if type(circles) != NoneType:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
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
