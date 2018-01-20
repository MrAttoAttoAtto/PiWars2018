'''Code for the maze challenge'''

import time

import cv2
from picamera.array import PiRGBArray

from camera import ConstantCamera
from settings import RESOLUTIONX, RESOLUTIONY, THRESHOLDS
from tank import TANK

color_order = [
    "yellow",
    "blue",
    "white",
    "red",
    "white",
    "blue"
]

def calculate_next_color_centroid(img, pos):
    pass

def run():
    # get camera
    continuous_camera = TANK.camera

    position = 0

    while True:
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = continuous_camera.get_image()

        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        cropped_bgr = image[RESOLUTIONY//3:RESOLUTIONY*2//3, 0:RESOLUTIONX]

        ret, center_x, center_y = calculate_next_color_centroid(cropped_bgr, position)
