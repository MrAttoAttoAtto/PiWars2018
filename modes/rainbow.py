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


import cv2
import numpy as np
from enum import Enum

from settings import (BALL_OFFSET_MAX, MIN_BALL_RADIUS,
                      SPEED_SCALE, THRESHOLDS, DEBUG, RESOLUTIONX, RESOLUTIONY)
from robot import ROBOT
#from tools import get_centroid

class RainbowState(Enum):
    TURNING = 1
    READY_FOR_NEXT = 2
    FINISHED = 3
    MOVING_FORWARD = 4


VISIT_COLOURS = [
    "rainbow_red",
    "rainbow_blue",
    "rainbow_yellow",
    "rainbow_green"
]

class Rainbow:
    def __init__(self):
        self.order = []
        self.visited = []
        self.running = False
        self.last = -1
        self.next = 0
        self.turn = -1
        self.state = RainbowState.READY_FOR_NEXT

    def calculate_next_direction(self):
        # Last to be spotted / visited
        cur_i = self.order.index(self.last)
        # Calculate more efficient distance
        dist_cw = self.order.index(self.next)
        dist_ccw = len(self.order) - self.order.index(self.next)
        if dist_cw < dist_ccw:
            self.turn = 0
        else:
            self.turn = 1

    def find_order(self, image):
        # Turn right
        ROBOT.right()
        # Try to detect balls
        for index, color in enumerate(VISIT_COLOURS):
            if (index not in self.order):
                # Ball has not been detected before
                if self.ball_aligned(image, color)[2] < BALL_OFFSET_MAX:
                    # Ball is aligned, so add the ball to order list.
                    print("FOUND COLOUR "+str(index))
                    self.order.append(index)
                    self.last = index
    
    def update(self, trigger_btn):
        # Should start
        if self.running:
            image = ROBOT.take_picture()

            # If robot has not figured out the order
            if len(self.order) < len(VISIT_COLOURS):
                self.find_order(image)

            else:
                # Order is known, proceed to visit in correct order.

                if self.state == RainbowState.READY_FOR_NEXT:
                    # Has visited all
                    if len(self.visited) == len(VISIT_COLOURS):
                        self.running = False
                        self.visited = []
                        self.next = 0
                        self.last = -1
                        self.turn = -1
                        self.state = RainbowState.FINISHED
                    else:
                        self.next = len(self.visited)
                        self.calculate_next_direction()
                        self.state = RainbowState.TURNING
                elif self.state == RainbowState.TURNING:
                    if self.ensure_safe_distance():
                        if self.turn == 0:
                            ROBOT.right()
                        else:
                            ROBOT.left()
                    else:
                        ROBOT.backwards(SPEED_SCALE)
                    
                    # If robot aligned with ball
                    if self.ball_aligned(image, VISIT_COLOURS[self.next])[2] < BALL_OFFSET_MAX:
                        self.last = self.next
                        self.state = RainbowState.MOVING_FORWARD

                elif self.state == RainbowState.MOVING_FORWARD:
                    ROBOT.forwards(SPEED_SCALE)
                    if self.ensure_area_touched():
                        self.state = RainbowState.READY_FOR_NEXT

        if self.running and trigger_btn:
            self.reset()
        elif trigger_btn and not self.running:
            self.running = True

    def ball_aligned(self, image, color):
        working_thresholds = np.array(THRESHOLDS[color])

        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Get the parts of the image in the specified colour range.
        mask = cv2.inRange(hsv, working_thresholds[0], working_thresholds[1])
        # Make the shapes more regular
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # Show debug image.
        if DEBUG:
            #cv2.imshow("MASK", mask)
            #cv2.waitKey(1)
            pass
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            x = int(x)
            y = int(y)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if DEBUG:
                    cv2.line(image, (x, 0), (x, RESOLUTIONY), (255, 0, 0), 1)
                    cv2.line(image, (0, y), (RESOLUTIONX, y), (255, 0, 0), 1)
                    cv2.drawContours(image, cnts, -1, (0, 255, 0), 1)
                    cv2.imshow("Image", image)
                    cv2.waitKey(1)
            # only proceed if the radius meets a minimum size
            if radius > MIN_BALL_RADIUS:
                # Show debug image

                # Where is the circle?
                height, width = RESOLUTIONY, RESOLUTIONX
                direction = (width/2 < int(x))
                extent = int(abs(width/2 - int(x))/(width/2))
                return (True, direction, extent)
            print("Not big enuph")
        return (False, 0, 0)

    def ensure_area_touched(self):
        dl, dc, dr = ROBOT.get_distance()
        return dc < 16

    def ensure_safe_distance(self):
        dl, dc, dr = ROBOT.get_distance()
        return dl > 12 and dc > 12 and dr > 12


    def reset(self):
        self.visited = []
        self.running = False
        self.next = 0
        self.turn = -1
        self.state = RainbowState.READY_FOR_NEXT


    def full_reset(self):
        self.reset()
        self.order = []

if __name__ == '__main__':
    x = Rainbow()
    while True:
        image = ROBOT.take_picture()
        rain.ball_aligned(image, "rainbow_blue")

