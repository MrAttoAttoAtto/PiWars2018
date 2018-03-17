'''
Indeed this isnt even required, but it is a good template for some of the other ones...
'''

import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

from settings import RESOLUTIONX, RESOLUTIONY, DEBUG
from robot import ROBOT
from tools import get_centroid_and_perim

def initialise():
    pass

SENSITIVITY = 75 #lower less sensitive
BEAR_NUM = 35 #le % of bear

def update():
    image = ROBOT.take_picture()


    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Clears the image of noise, makes it smaller (and cropped closer to the robot)
    # Also constructs the contours from the boolean image

    noisy_image = grayscale_image[int(RESOLUTIONY/4):int(RESOLUTIONY/2), 0:RESOLUTIONX]

    clear_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)

    reversed_image = cv2.bitwise_not(clear_image)

    ret, boolean_image = cv2.threshold(reversed_image, 120, 255, cv2.THRESH_BINARY_INV) #THRESH_BINARY_INV

    center_x, center_y, perimeter, contours = get_centroid_and_perim(boolean_image, 1, cv2.CHAIN_APPROX_NONE)

    if False not in (center_x, center_y):

        # Decides which way to go (and does it (IN THE FUTURE)) by the angle at which the line is going
        # Also, the 3/4 and 1/4 are subject to change based on testing

        half_x = RESOLUTIONX//2

        if center_x <= half_x-SENSITIVITY:
            ROBOT.bear_left(BEAR_NUM)
            going = 0
            # Go LEFT

        elif center_x < half_x+SENSITIVITY and center_x > half_x-SENSITIVITY:
            ROBOT.forwards()
            going = 1
            # Go STRAIGHT

        elif center_x >= half_x+SENSITIVITY:
            ROBOT.bear_right(BEAR_NUM)
            going = 2
            # Go RIGHT

        else:
            print("??????????????????????????")


    else:
        print("No Line Found")
        ROBOT.halt()

    if DEBUG:
        try:
            cv2.line(noisy_image, (center_x, 0), (center_x, 720), (255, 0, 0), 1)
            cv2.line(noisy_image, (0, center_y), (1280, center_y), (255, 0, 0), 1)
            cv2.drawContours(noisy_image, contours, -1, (0, 255, 0), 1)
            cv2.imshow('frame', noisy_image)
            cv2.waitKey(1)
        except NameError:
            pass


def run(): #deprecated
    # Gets the camera to take a video, and makes it an array cv2 can work with
    while True:

        image = ROBOT.take_picture() # turns it straight into a nice array

        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Clears the image of noise, makes it smaller (and cropped closer to the robot)
        # Also constructs the contours from the boolean image

        noisy_image = grayscale_image[0:int(RESOLUTIONY/2), 0:RESOLUTIONX]

        clear_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)

        ret, boolean_image = cv2.threshold(clear_image, 60, 255, cv2.THRESH_BINARY_INV)

        center_x, center_y, perimeter, contours = get_centroid_and_perim(boolean_image, 1, cv2.CHAIN_APPROX_NONE)

        if not False in (center_x, center_y):

            # Decides which way to go (and does it (IN THE FUTURE)) by the angle at which the line is going
            # Also, the 3/4 and 1/4 are subject to change based on testing

            if center_x >= RESOLUTIONX * 3/4:
                pass # Go LEFT

            elif center_x < RESOLUTIONX * 3/4 and center_x > RESOLUTIONX * 1/4:
                pass # Go STRAIGHT

            elif center_x <= RESOLUTIONX * 1/4:
                pass # Go RIGHT
            

            cv2.line(noisy_image, (center_x, 0), (center_x, 720), (255, 0, 0), 1)
            cv2.line(noisy_image, (0, center_y), (1280, center_y), (255, 0, 0), 1)

            cv2.drawContours(noisy_image, contours, -1, (0, 255, 0), 1)

        else:
            print("OH DEAR: NO LINE")
            # LINE NOT FOUND

        if DEBUG:
            try:
                cv2.imshow('frame', noisy_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except NameError:
                pass
