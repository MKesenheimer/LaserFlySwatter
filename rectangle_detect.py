from types import NoneType
import cv2 as cv
import numpy as np 
import time
import math

while(1):
    # Take each frame
    _, frame = cap.read()
    
    # Convert BGR to HSV
    #hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    
    
    #hsv_c = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    
    # define range of blue color in HSV
    lower = np.array([0,0,0])
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
    ret, thresh = cv.threshold(cimg, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    cv.drawContours(img, [cnt], 0, (0,255,0), 3)
    cv.imshow("contoures",img)
