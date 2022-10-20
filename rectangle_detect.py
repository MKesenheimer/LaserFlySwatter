
import cv2 as cv
import numpy as np 
import time
import math
THRESHOLD=10
cap = cv.VideoCapture(0)#my webcam(2),default(0)
cv.namedWindow("frame")
while(1):
    # Take each frame
    _, frame = cap.read()
    cv.imshow("frame",frame)
    # Convert BGR to HSV
    #hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    
    
    #hsv_c = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    
    # define range of blue color in HSV
    #lower = np.array([0,0,0])
    #upper = np.array([255,255,255])

    # Threshold the HSV image to get only blue colors
    #mask = cv.inRange(frame, lower, upper)
    
    # Bitwise-AND mask and original image
    #res = cv.bitwise_and(frame,frame, mask= mask)
    

    #cv.imshow('res',res)
    #cv.imshow('mask',mask)
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) 
    Blur=cv.GaussianBlur(gray,(5,5),1) 
    Canny=cv.Canny(Blur,10,50) 


    contours =cv.findContours(Canny,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)[0]


    cntrRect = []

    for i in contours:
        epsilon = 0.1*cv.arcLength(i,True)
        approx = cv.approxPolyDP(i,epsilon,True)
        
        if len(approx) == 4:
            if is_rect(*approx):
                print(approx)
                Corner_dists=[]
                #pythagoras
                cv.drawContours(frame,cntrRect,-1,(0,255,0),2)
                cv.imshow('rects',frame)
                cntrRect.append(approx)
    
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

def is_rect(p1,p2,p3,p4):
    dists=[math.dist(p1,p2),math.dist(p1,p3),math.dist(p1,p4),math.dist(p3,p2),math.dist(p4,p2),math.dist(p3,p4)]
    dists.sort()
    return threshold(dists[0],dists[1],THRESHOLD) and threshold(dists[2],dists[3],THRESHOLD)


def threshold(n1,n2,t):
    return ((n1-n2)**2)**(1/2)<t