from lumax import *
import time
import math
import sys
import os
import numpy
from coords import coords
import cv2 as cv

def main():
    try:
        renderer = lumax_renderer()

        # Notes:
        # cl: Coordinate System of Laser
        # cc: Coordinate System of Camera

        # setup frame, generate a circle
        brigthness = 0.45 # 0 to 1
        r = int(brigthness * 255 * 255)
        g = int(brigthness * 255 * 255)
        b = int(brigthness * 255 * 255)
        r = restrict(r, 0, 255 * 255)
        g = restrict(g, 0, 255 * 255)
        b = restrict(b, 0, 255 * 255)
        circle_cc = numpy.array([128 * 255, 128 * 255, 10000])
        circle_shape = geometry.circle(circle_cc[0], circle_cc[1], circle_cc[2], 100, r, g, b)
        renderer.add_shape_to_frame(circle_shape)

        # send the frame to the device
        renderer.send_frame(3000)
        time.sleep(1)

        # capture images for calibration
        images = []
        starttime = time.time()
        duration = 10
        maximages = 100
        cap = cv.VideoCapture(0)
        while time.time() - starttime <= duration and len(images) < maximages:
            # Take each frame
            _, frame = cap.read()
            images.append(frame)
            #cv.imshow('frame',frame)
            #k = cv.waitKey(5) & 0xFF
            #if k == 27:
            #    break

        images = numpy.array(images)
        print("[INFO] {} images captured. Continuing with calibration routine.".format(len(images)))
        print("[DEBUG] Shape of images: {}".format(images.shape))

        # calibration
        coord_transformer = coords(images, circle_cc)
        circle = coord_transformer.img_c
        print("[INFO] Coordinates of circle in camera coordinate system: {}".format(circle))

        for i in range(images.shape[0]):
            cv.circle(images[i],(circle[0],circle[1]),circle[2],(0,0,255),3)

        #for i in range(images.shape[0]):
        #    cv.imshow("test", images[i])
        #    time.sleep(0.1)
        #    k = cv.waitKey(5) & 0xFF
        #    if k == 27:
        #        break

        print("[INFO] Coordinates of circle in laser coordinate system: {}".format(coord_transformer.laser_coords(circle_cc[0:2])))
            

        # close device
        renderer.close_device()

    except KeyboardInterrupt:
        print("Exiting.")
        renderer.close_device()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

# main program
if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description="")
    #parser.add_argument('--posX', dest='posx', type=int, default=500, help='x-position to read the data from')
    #parser.add_argument('--posY', dest='posy', type=int, default=500, help='y-position to read the data from')
    #parser.add_argument('--pack', dest='pack', type=int, default=24, help='y-position to read the data from')
    #args = parser.parse_args()

    main()