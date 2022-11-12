from lumax import *
import time
import math
import sys
import os

def restrict(x, minx, maxx):
    return max(min(maxx, x), minx)

def main():
    global lhandle
    print("API version: {}".format(lumax.get_api_version()))
    print("Number of physical devices: {}".format(lumax.get_physical_devices()))
    lhandle = lumax.open_device(1, 0)
    print("Lumax handle: {}".format(lhandle))

    print("SetTTL return: {}".format(lumax.setTTL(lhandle, 0)))

    ret, timeToWait, bufferChanged = lumax.wait_for_buffer(lhandle, 17)
    print("WaitForBuffer return: {}, {}, {}".format(ret, timeToWait, bufferChanged))

    brigthness = 0.45 # 0 to 1
    r = int(brigthness * 255 * 255)
    g = int(brigthness * 255 * 255)
    b = int(brigthness * 255 * 255)
    r = restrict(r, 0, 255 * 255)
    g = restrict(g, 0, 255 * 255)
    b = restrict(b, 0, 255 * 255)
    # generiere einen Kreis mit 100 Punkten
    npoints = 100
    points = lpoints(npoints)
    for i in range(0, npoints):
        x, y = lumax.circle_point(128 * 255, 128 * 255, 5000, i, npoints)
        points.struct_arr[i].x = x
        points.struct_arr[i].y = y
        points.struct_arr[i].r = r
        points.struct_arr[i].g = g
        points.struct_arr[i].b = b

    # print the points
    #for i in range(0, points.length):
    #    print("p{} = {}, {}, {}, {}, {}".format(i, points.struct_arr[i].x, points.struct_arr[i].y, points.struct_arr[i].r, points.struct_arr[i].g, points.struct_arr[i].b))

    ret, timeToWait = lumax.send_frame(lhandle, points, 10000, 0)
    print("SendFrame return: {}, {}".format(ret, timeToWait))
    ret, timeToWait, bufferChanged = lumax.wait_for_buffer(lhandle, 17)
    time.sleep(100)

    print("StopFrame return: {}".format(lumax.stop_frame(lhandle)))
    print("CloseDevice return: {}".format(lumax.close_device(lhandle)))

# main program
if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description="")
    #parser.add_argument('--posX', dest='posx', type=int, default=500, help='x-position to read the data from')
    #parser.add_argument('--posY', dest='posy', type=int, default=500, help='y-position to read the data from')
    #parser.add_argument('--pack', dest='pack', type=int, default=24, help='y-position to read the data from')
    #args = parser.parse_args()

    global lhandle
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting.")
        lumax.stop_frame(lhandle)
        lumax.close_device(lhandle)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
