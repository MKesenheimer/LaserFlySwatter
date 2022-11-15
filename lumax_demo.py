from lumax import *
import time
import math
import sys
import os
import numpy

def main():
    try:
        renderer = lumax_renderer()

        # setup frame, generate circle
        brigthness = 0.45 # 0 to 1
        r = int(brigthness * 255 * 255)
        g = int(brigthness * 255 * 255)
        b = int(brigthness * 255 * 255)
        r = restrict(r, 0, 255 * 255)
        g = restrict(g, 0, 255 * 255)
        b = restrict(b, 0, 255 * 255)
        circle = geometry.new_circle(128 * 255, 128 * 255, 5000, 100, r, g, b)
        renderer.add_shape_to_frame(circle)

        # send the frame to the device
        renderer.send_frame(10000)

        # wait and close device
        time.sleep(100)
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

