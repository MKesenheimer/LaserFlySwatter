import numpy as np
import math
import time
import cv2 as cv


class coords():
    def __init__(self,laser_c,img_c):
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
        
        





