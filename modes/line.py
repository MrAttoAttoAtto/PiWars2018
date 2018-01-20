'''
Indeed this isnt even required, but it is a good template for some of the other ones...
'''

import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

from camera import ConstantCamera
from settings import DEBUG, RESOLUTIONX, RESOLUTIONY
from tank import TANK
from tools import get_centroid


def run():
    # Gets the camera to take a video, and makes it an array cv2 can work with

    continuous_camera = TANK.camera

    while True:

        image = continuous_camera.get_image() # turns it straight into a nice array

        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Clears the image of noise, makes it smaller (and cropped closer to the robot)
        # Also constructs the contours from the boolean image

        noisy_image = grayscale_image[0:int(RESOLUTIONY/2), 0:RESOLUTIONX]

        clear_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)

        ret, boolean_image = cv2.threshold(clear_image, 60, 255, cv2.THRESH_BINARY_INV)

        center_x, center_y = get_centroid(boolean_image, 1, cv2.CHAIN_APPROX_NONE)

        if not False in (center_x, center_y):

            # Decides which way to go (and does it (IN THE FUTURE)) by the angle at which the line is going
            # Also, the 3/4 and 1/4 are subject to change based on testing

            if center_x >= RESOLUTIONX * 3/4:
                pass # Go LEFT

            elif center_x < RESOLUTIONX * 3/4 and center_x > RESOLUTIONX * 1/4:
                pass # Go STRAIGHT

            elif center_x <= RESOLUTIONX * 1/4:
                pass # Go RIGHT
            

            #cv2.line(noisyImage, (centerX, 0), (centerX, 720), (255, 0, 0), 1)
            #cv2.line(noisyImage, (0, centerY), (1280, centerY), (255, 0, 0), 1)

            #cv2.drawContours(noisyImage, contours, -1, (0, 255, 0), 1)

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
