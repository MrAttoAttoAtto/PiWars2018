'''rainbow.py
Code for the "over the rainbow" challenge.
1st time
	turn right, until a ball of one of four colors is seen, append with angle
	^ x3
	check what direction to turn for red
	turn that direction until red spotted
	move forwards until proximity too close
	move backwards a pre-specified distance so that rotation is a-ok

	^ x3 for other colors in order

'''

import time

import cv2
import imutils
from picamera import PiCamera
from picamera.array import PiRGBArray

from settings import (BALL_OFFSET_MAX, MIN_BALL_RADIUS, MINIMUM_AREA_DISTANCE,
                      REVERSE_TIME, SPEED_SCALE, THRESHOLDS)
from robot import ROBOT
from tools import get_centroid

colour_thresholds = [
    "rainbow_red",
    "rainbow_blue",
    "rainbow_yellow",
    "rainbow_green"
]

class Rainbow:
    def __init__(self):
        self.reset()
    
    def update(self, trigger_btn):
        if self.running:
            image = ROBOT.take_picture()
            # resize the frame, blur it, and convert it to the HSV
            # color space
            image = imutils.resize(image, width=600)
            # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            if len(self.order) < 4:
                ROBOT.right()
                for index, color in enumerate(colour_thresholds):
                    if (index not in self.order) and self.ball_aligned(hsv, color):
                        self.order.append(index)
                        self.last = index
            else:
                if self.last != -1:
                    cur_i = self.order.index(self.last)
                    dist_list = self.order[cur_i:] + self.order[:cur_i]
                    dist_cw = self.order.index(self.next)
                    dist_ccw = len(self.order) - self.order.index(self.next)
                    if dist_cw < dist_ccw:
                        self.turn = 0
                    else:
                        self.turn = 1
                    self.last = -1
                elif self.last == len(self.order):
                    self.running = False
                    self.next = 0
                    self.last = -1
                    self.turn = -1
                else:
                    if self.turn == 0:
                        ROBOT.right()
                    else:
                        ROBOT.left()
                    if self.ball_aligned(hsv, colour_thresholds[self.next]):
                        self.turn = 2
                    if self.turn == 2:
                        ROBOT.forwards(SPEED_SCALE)
                        if self.ensure_area_touched():
                            ROBOT.backwards(time=REVERSE_TIME)
                            self.last = self.next
                            self.next = self.last + 1

        if self.running and trigger_btn:
            self.reset()
        elif trigger_btn and not self.running:
            self.running = True

    def ball_aligned(self, image, color):
        working_thresholds = THRESHOLDS[color]

        mask = cv2.inRange(image, working_thresholds[0], working_thresholds[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > MIN_BALL_RADIUS:
                # WHere is the circle?
                width, height = cv2.GetSize(mask)
                if abs(width/2 - center[0]) < BALL_OFFSET_MAX:
                    return True
        return False

    def ensure_area_touched(self):
        if 

    def reset(self):
        self.order = []
        self.running = False

    





def run():
    visited = []
    
    # capture frames from the camera
    while True:
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = ROBOT.take_picture()    
    
        # resize the frame, blur it, and convert it to the HSV
        # color space
        image = imutils.resize(image, width=600)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        for colour, thresholds in colour_thresholds:
            ensure_safe_distance() # TODO
            while not ball_aligned(hsv, thresholds): # THIS WILL NOT WORK TODO (IT NEVER REFRESHES THE IMAGE AND WILL THEREFORE CONTINUE FOREVER)
                ROBOT.left()
            while not ensure_area_touched(): # TODO
                ROBOT.forwards()

        # clear the stream in preparation for the next frame
        raw_capture.truncate(0)
