from lumax import *
import time
import math
import sys
import os
import numpy
from coords import coords
import cv2 as cv

# TODO:
# - Die Koordinatenwerte von der Kamera sind von der Auflösung abhängig, d.h. bei Anschluss einer anderen Kamera muss entsprechend skaliert werden.

# Notes:
# col: Coordinate System of Laser
# coc: Coordinate System of Camera

DEBUG = True
VIDEODEVICE = 1

def close_exit(renderer):
    print("Exiting.")
    renderer.close_device()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

def main():
    try:
        # new renderer to render shapes on the laser show device
        renderer = lumax_renderer()

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
        shape = geometry.circle(circle_col[0], circle_col[1], circle_col[2], 100, r, g, b)
        renderer.add_shape_to_frame(shape)

        # send the frame to the device
        print("[INFO] Calibrating...")
        renderer.send_frame(3000)
        time.sleep(1)

        # capture images for calibration
        images = []
        starttime = time.time()
        duration = 10
        maximages = 100
        cap = cv.VideoCapture(VIDEODEVICE)
        while time.time() - starttime <= duration and len(images) < maximages:
            # Take each frame and add to the list
            _, frame = cap.read()
            images.append(frame)
        # cast of list of images to numpy array
        images = numpy.array(images)

        # when all frames captures, close device and print status
        renderer.stop_frame()
        print("[INFO] {} images captured. Continuing with calibration routine...".format(len(images)))
        print("[DEBUG] Shape of images: {}".format(images.shape))

        
        # call the calibration routine
        try:
            coord_transformer = coords(images, circle_col)
        except:
            print("[ERROR] Calibration failed. Probably no circles detected. Try again.")
            close_exit(renderer)


        # coordinates of the circle in the coordinate system of the camera
        circle_coc = coord_transformer.image_coords()
        print("[INFO] CL: Coordinate system of laser; CC: Coordinate system of camera.")
        print("[INFO] Coordinates of circle in CC: {}".format(circle_coc))
        print("[INFO] Original coordinates of circle in CL: {}".format(circle_col))
        print("[INFO] Back-transformed coordinates of circle in CL: {}".format(coord_transformer.laser_coords(circle_coc[0:2])))

        # check: show one image and the found circle
        cv.circle(images[0], (circle_coc[0], circle_coc[1]), circle_coc[2], (0, 0, 255), 3)
        starttime = time.time()
        duration = 2
        while time.time() - starttime <= duration:
            cv.imshow("Calibration", images[0])
            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break
        cv.destroyWindow("Calibration")

        # Test: Die andere Richtung: Zeichne einen Kreis im Koordinatensystem der Kamera
        # und überprüfe mit dem Laser
        tcircle_coc = numpy.array([845, 457 + 20, 137])
        tcircle_col = numpy.zeros((3))
        tcircle_col[0:2] = coord_transformer.laser_coords(tcircle_coc[0:2])
        tcircle_col[2] = coord_transformer.laser_scale(tcircle_coc[2])
        shape = geometry.circle(tcircle_col[0], tcircle_col[1], tcircle_col[2], 100, r, g, b)
        renderer.new_frame()
        renderer.add_shape_to_frame(shape)
        renderer.send_frame(3000)
        time.sleep(1)
        _, timage = cap.read()
        cv.circle(timage, (tcircle_coc[0], tcircle_coc[1]), tcircle_coc[2], (0, 0, 255), 3)
        starttime = time.time()
        duration = 2
        while time.time() - starttime <= duration:
            cv.imshow("Test", timage)
            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break
        renderer.stop_frame()
        cv.destroyWindow("Test")

        # track an object and shoot it with the laser
        while True:
            renderer.stop_frame()
            _, cimage = cap.read()
            gimage = cv.medianBlur(cimage,3)
            gimage = cv.cvtColor(gimage,cv.COLOR_BGR2GRAY)
            hough_circles = cv.HoughCircles(gimage,cv.HOUGH_GRADIENT,2,10,param1=100,param2=100,minRadius=5,maxRadius=200)
            if type(hough_circles) != type(None):
                hough_circles = numpy.uint16(numpy.around(hough_circles))
                best_fit_coc = hough_circles[0,0]
                print("[DEBUG] Found circle at: {}".format(best_fit_coc))
                ccircle_col = numpy.zeros((3), dtype='uint16')
                ccircle_col[0:2] = coord_transformer.laser_coords(best_fit_coc[0:2])
                ccircle_col[2] = coord_transformer.laser_scale(best_fit_coc[2])
                print("[DEBUG] Transformed circle coords in CL: {}".format(ccircle_col))
                #shape = geometry.circle(ccircle_col[0], ccircle_col[1], ccircle_col[2], 100, r, g, b)
                shape1 = geometry.triangle(ccircle_col[0], ccircle_col[1], 
                                           ccircle_col[0] + ccircle_col[2] / 2, ccircle_col[1] + ccircle_col[2] / 2, 
                                           ccircle_col[0] - ccircle_col[2] / 2, ccircle_col[1] + ccircle_col[2] / 2, 
                                           5, r, g, b)
                shape2 = geometry.triangle(ccircle_col[0], ccircle_col[1], 
                                           ccircle_col[0] + ccircle_col[2] / 2, ccircle_col[1] - ccircle_col[2] / 2, 
                                           ccircle_col[0] - ccircle_col[2] / 2, ccircle_col[1] - ccircle_col[2] / 2, 
                                           5, r, g, b)
                shape1 = geometry.rotate_shape(shape1, ccircle_col[0:2], 90)
                shape2 = geometry.rotate_shape(shape2, ccircle_col[0:2], 90)
                renderer.new_frame()
                renderer.add_shape_to_frame(shape1)
                renderer.add_shape_to_frame(shape2)
                renderer.send_frame(1000)
                if DEBUG:
                    cv.circle(cimage, (best_fit_coc[0], best_fit_coc[1]), best_fit_coc[2], (0, 0, 255), 3)
                    cv.imshow("Tracker", cimage)
                    k = cv.waitKey(5) & 0xFF
                    if k == 27:
                        break
        

        # close the device in the end
        renderer.close_device()
        cv.destroyWindow("Tracker")

    except KeyboardInterrupt:
        close_exit(renderer)

# main program
if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description="")
    #parser.add_argument('--posX', dest='posx', type=int, default=500, help='x-position to read the data from')
    #parser.add_argument('--posY', dest='posy', type=int, default=500, help='y-position to read the data from')
    #parser.add_argument('--pack', dest='pack', type=int, default=24, help='y-position to read the data from')
    #args = parser.parse_args()

    main()