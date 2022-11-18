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

i=0
while(1):
    cv.imshow("test",video[i])
    i+=1
    time.sleep(0.1)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break