import numpy as np
import math
import time
import cv2 as cv

DEBUG = 1

class coords():
    def __sortkey(iteration):
        def rf(c):
            return(c[iteration])
        return rf

    def __init__(self,frames,laser_circle):
        # coordinates of the detected circle
        circle_coc=[]
        
        # calculate the average of navg frames
        navg = 10
        avg_frames = []
        for i in range(0, len(frames) - 1, navg):
            avg = frames[i]//navg
            for j in range(1, navg):
                # print("[DEBUG] i + j = {}".format(i + j))
                avg = np.add(avg, frames[i+j]//navg)
            avg_frames.append(avg)
        avg_frames = np.array(avg_frames)

        # DEBUG
        if DEBUG:
            print("[DEBUG] Length of frames = {}".format(len(frames)))
            print("[DEBUG] Length of averages = {}".format(len(avg_frames)))
            for i in range(len(avg_frames)):
                cv.imshow("Averages", avg_frames[i])
                k = cv.waitKey(5) & 0xFF
                if k == 27:
                    break
            cv.destroyWindow("Averages")

        # detect the circle
        for i in range(len(avg_frames)):
            img = cv.medianBlur(frames[i],3)
            cimg = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
            circles = cv.HoughCircles(cimg,cv.HOUGH_GRADIENT,2,10,param1=100,param2=100,minRadius=5,maxRadius=200)
            if type(circles) != type(None):
                circles = np.uint16(np.around(circles))
                c=circles[0,0]
                # draw the outer circle
                circle_coc.append(c)
                
        circle_coc.sort(key=coords.__sortkey(0))
        circle_coc=np.array(circle_coc)[int(len(circle_coc)/10):1-int(len(circle_coc)/10)]
        circle_coc=list(circle_coc)
        circle_coc.sort(key=coords.__sortkey(1))
        circle_coc=np.array(circle_coc)[int(len(circle_coc)/10):1-int(len(circle_coc)/10)]
        circle_coc=list(circle_coc)
        circle_coc.sort(key=coords.__sortkey(2))
        circle_coc=np.array(circle_coc)[int(len(circle_coc)/10):1-int(len(circle_coc)/10)]
        img_c=np.array([np.average(circle_coc[:,0]), np.average(circle_coc[:,1]), np.average(circle_coc[:,2])], dtype="uint16")
        self.__build_coords(laser_circle,img_c)
        self.circle_coc=circle_coc
        

    def __build_coords(self,laser_c,img_c):
        self.laser_c = laser_c
        self.img_c = img_c
        radius_l = laser_c[2]
        radius_c = img_c[2]
        self.img_scale = int(radius_l/radius_c)
        self.x_shift = int(laser_c[0]-(img_c[0]*self.img_scale))
        self.y_shift = int(laser_c[1]-(img_c[1]*self.img_scale))
        print("[DEBUG] x_shift: {}".format(self.x_shift))
        print("[DEBUG] y_shift: {}".format(self.y_shift))
        print("[DEBUG] img_scale: {}".format(self.img_scale))

    def laser_coords(self,img_coords):
        xI,yI=img_coords
        x=(xI*self.img_scale)+self.x_shift
        y=(yI*self.img_scale)+self.y_shift
        return x,y
        
    def laser_scale(self,scale):
        return scale*self.img_scale
        
    def image_coords(self):
        return self.img_c
        
#  0 --------------------------> 255 * 255
#  |
#  |
#  |
#  |
#  |
#  |
#  V
#  255 * 255