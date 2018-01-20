'''Code for the maze challenge'''

import time

import cv2
from picamera.array import PiRGBArray

from camera import ConstantCamera
from settings import RESOLUTIONX, RESOLUTIONY, THRESHOLDS
from tank import ROBOT
from tools import get_centroid

color_order = [
    "yellow",
    "blue",
    "white",
    "red",
    "white",
    "blue"
]

def calculate_next_color_centroid(img, pos):
    working_color = color_order[pos]
    working_thresholds = THRESHOLDS[working_color]

    mask = cv2.inRange(img, working_thresholds[0], working_thresholds[1])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    center_x, center_y = get_centroid(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if False not in (center_x, center_y):
        return True, center_x, center_y

    else:
        return False, 0, 0

def go_forth():
    frontal_sensor_dist = ROBOT.get_distance()[1]
    while frontal_sensor_dist > 10 or frontal_sensor_dist == 0:
        ROBOT.forwards()


def run():
    position = 0

    while True:
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = ROBOT.take_picture()

        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        cropped_hsv = hsv[RESOLUTIONY//3:RESOLUTIONY*2//3, 0:RESOLUTIONX]

        ret, center_x, center_y = calculate_next_color_centroid(cropped_hsv, position)

        if not ret:
            if position < 4:
                ROBOT.right()
            else:
                ROBOT.left()
            
            continue

        # Here, 10 is an absolute estimate, a complete guess. Testing needed TODO
        # If this IF passes, then it will go forth (!) until it hits a wall (not hit but you get me)
        if RESOLUTIONX-10 <= center_x <= RESOLUTIONX+10:
            go_forth()
            position += 1
        elif center_x < RESOLUTIONX-10:
            ROBOT.left()
        else:
            ROBOT.right()
