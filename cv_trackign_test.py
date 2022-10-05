import cv2 as cv
import numpy as np 
import time
import math

cap = cv.VideoCapture(2)#my webcam(2),default(0)
_,lf=cap.read()
while(1):
    # Take each frame
    _, frame = cap.read()
    
    # Convert BGR to HSV
    #hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    
    change=((lf-frame)%255)
    cv.imshow('change1',change)
    #hsv_c = cv.cvtColor(change, cv.COLOR_BGR2HSV)
    
    
    # define range of blue color in HSV
    lower = np.array([245,245,245])
    upper = np.array([255,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(change, lower, upper)
    
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(change,change, mask= mask)


    cv.imshow('res',res)
    cv.imshow('mask',mask)
    
    cv.imshow('frame',frame)
    lf=frame

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv.destroyAllWindows()
