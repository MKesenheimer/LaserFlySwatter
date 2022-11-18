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
        # coordinates of the circle in the coordinate system of the laser
        circle_col = numpy.array([128 * 255, 128 * 255, 8000])
        circle_shape = geometry.circle(circle_col[0], circle_col[1], circle_col[2], 100, r, g, b)
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
            # Take each frame and add to the list
            _, frame = cap.read()
            images.append(frame)
        # cast of list of images to numpy array
        images = numpy.array(images)

        # when all frames captures, close device and print status
        renderer.close_device()
        print("[INFO] {} images captured. Continuing with calibration routine...".format(len(images)))
        print("[DEBUG] Shape of images: {}".format(images.shape))

        
        # call the calibration routine
        coord_transformer = coords(images, circle_col)
        # coordinates of the circle in the coordinate system of the camera
        circle_coc = coord_transformer.image_coords()
        print("[INFO] CL: Coordinate system of laser; CC: Coordinate system of camera.")
        print("[INFO] Coordinates of circle in CC: {}".format(circle_coc))
        print("[INFO] Original coordinates of circle in CL: {}".format(circle_col))
        print("[INFO] Back-transformed coordinates of circle in CL: {}".format(coord_transformer.laser_coords(circle_coc[0:2])))

        # check: show one image and the found circle
        cv.circle(images[0], (circle_coc[0], circle_coc[1]), circle_coc[2], (0, 0, 255), 3)
        starttime = time.time()
        duration = 1
        while time.time() - starttime <= duration:
            cv.imshow("Calibration", images[0])
            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break

        time.sleep(5)

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