import numpy as np
import math
import time
import cv2 as cv
import os
from coords import coords




print(os.listdir())
cap = cv.VideoCapture(".\images\circle2.mov")
ret = True
frames=[]
while ret:
    ret, img = cap.read() # read one frame from the 'capture' object; img is (H, W, C)
    #print(ret)
    if ret:
        frames.append(img)
video = np.stack(frames, axis=0)
print(video.shape)
c_system=(coords(video,[100,100,5000]))
frame=video[20]
print(c_system.img_c)
for index,circle in enumerate(c_system.img_circles):
    if index<len(video-1):
        frame=np.add(video[index]//2,video[index+1]//2)
        img = cv.medianBlur(frame,3)
        cimg = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        circles = cv.HoughCircles(cimg,cv.HOUGH_GRADIENT,2,10,param1=100,param2=100,minRadius=5,maxRadius=200)
        if type(circles) != type(None):
            circles = np.uint16(np.around(circles))
            i=circles[0,0]
            # draw the outer circle
            cv.circle(video[index],(i[0],i[1]),i[2],(255,255,0),2)
            # draw the center of the circle
            #cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
            




    cv.circle(video[index],(circle[0],circle[1]),circle[2],(0,255,0),2)

i=0
while(1):
    cv.imshow("test",video[i])
    i+=1
    time.sleep(0.1)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break