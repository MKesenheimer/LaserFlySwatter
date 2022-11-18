import numpy as np
import math
import time
import cv2 as cv


class coords():
    def __init__(self,frames,laser_circle):
        img_circles=[]
        for i in range(len(frames)-1):
            cframe=np.add(frames[i]//2,frames[i+1]//2)
            hsv = cv.cvtColor(cframe, cv.COLOR_BGR2HSV)
            img = cv.medianBlur(hsv,3)
            cimg = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
            circles = cv.HoughCircles(cimg,cv.HOUGH_GRADIENT,2,10,param1=100,param2=100,minRadius=5,maxRadius=200)
            if type(circles) != type(None):
                circles = np.uint16(np.around(circles))
                c=circles[0,0]
                # draw the outer circle
                img_circles.append(c)
        def sortkey(iteration):
            def rf(c):
                return(c[iteration])
            return rf
        img_circles.sort(key=sortkey(0))
        img_circles=np.array(img_circles)[int(len(img_circles)/10):1-int(len(img_circles)/10)]
        img_circles=list(img_circles)
        img_circles.sort(key=sortkey(1))
        img_circles=np.array(img_circles)[int(len(img_circles)/10):1-int(len(img_circles)/10)]
        img_circles=list(img_circles)
        img_circles.sort(key=sortkey(2))
        img_circles=np.array(img_circles)[int(len(img_circles)/10):1-int(len(img_circles)/10)]
        img_c=[np.sum(img_circles[:,0])/len(img_circles),np.sum(img_circles[:,1])/len(img_circles),np.sum(img_circles[:,2])/len(img_circles)]    
        print(img_c)
        self.build_coords(laser_circle,img_c)
    def build_coords(self,laser_c,img_c):
        self.laser_c=laser_c
        self.img_c=img_c
        self.img_scale=laser_c[2]/img_c[2]
        self.x_shift=laser_c[0]-(img_c[0]*self.img_scale)
        self.y_shift=laser_c[1]-(img_c[1]*self.img_scale)
    def laser_coords(self,img_coords):
        xI,yI=img_coords
        x=(xI*self.img_scale)+self.x_shift
        y=(yI*self.img_scale)+self.y_shift
        return x,y
        
        





