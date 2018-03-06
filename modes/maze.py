'''Code for the maze challenge'''

import cv2

from settings import (MAZE_MAX_X_OFFSET, MAZE_MINIMUM_PERIMETER,
                      MAZE_ROBOT_FORWARD_SPEED, MAZE_ROBOT_FORWARD_TIME,
                      MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME,
                      MAZE_WALL_DISTANCE, RESOLUTIONX, RESOLUTIONY, THRESHOLDS)
from robot import ROBOT
from tools import get_centroid_and_max_contour

class Maze:
    def __init__(self):
        self.color_order = [
            "maze_yellow",
            "maze_blue",
            "maze_white",
            "maze_red",
            "maze_white",
            "maze_blue"
        ]

        self.position = 0
        self.is_going_forth = False

    def calculate_next_color_centroid(self, img, pos):
        '''
        Basically takes an images and the position of the robot (as a number)
        and outputs the centers of the colored wall if it is valid and exists
        '''

        # gets the relevant threshold from the central database
        working_color = self.color_order[pos]
        working_thresholds = THRESHOLDS[working_color]

        # does the masking to get the part which falls into that category
        mask = cv2.inRange(img, working_thresholds[0], working_thresholds[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        center_x, center_y, max_contour, contours = get_centroid_and_max_contour(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # again, a complete guess, but this filters out really small ones that are not actually real
        if cv2.arcLength(max_contour, True) > MAZE_MINIMUM_PERIMETER:
            return True, center_x, center_y

        else:
            return False, 0, 0

    @staticmethod
    def go_forth():
        left, frontal_sensor_dist, right = ROBOT.get_distance()

        while frontal_sensor_dist > MAZE_WALL_DISTANCE or frontal_sensor_dist == 0:
            if 0 < left < 5:
                ROBOT.right(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
            elif 0 < right < 5:
                ROBOT.left(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
            else:
                ROBOT.forwards(MAZE_ROBOT_FORWARD_SPEED, MAZE_ROBOT_FORWARD_TIME)

            left, frontal_sensor_dist, right = ROBOT.get_distance()

    def no_loop_go_forth(self):
        '''
        Same as above, but made for the no-loop system that Joe likes
        '''
        left, frontal_sensor_dist, right = ROBOT.get_distance()

        if frontal_sensor_dist > MAZE_WALL_DISTANCE or frontal_sensor_dist == 0:
            if 0 < left < 5:
                ROBOT.right(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
            elif 0 < right < 5:
                ROBOT.left(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
            else:
                ROBOT.forwards(MAZE_ROBOT_FORWARD_SPEED, MAZE_ROBOT_FORWARD_TIME)
        
        else:
            # updates the variable to stop the go_forthyness of the next run
            self.is_going_forth = False

    def run(self):
        '''
        Guess.

        But seriously it runs the loopy version of the maze navigation code
        '''
        position = 0

        while True:
            # if this statement is fulfilled, it means its at the final stretch
            if position == 6:
                break

            # grab the raw NumPy array representing the image, 
            # then convert and crop it for processing

            image = ROBOT.take_picture()

            # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            cropped_hsv = hsv[RESOLUTIONY//3:RESOLUTIONY*2//3, 0:RESOLUTIONX]

            # actually process the image for the centroids
            ret, center_x, center_y = self.calculate_next_color_centroid(cropped_hsv, position)

            # if there were no valid thresholds, just make it turn
            # ased on where it is in the maze and then restart the loop
            if not ret:
                if position < 4:
                    ROBOT.right(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
                else:
                    ROBOT.left(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)

                continue

            # Here, 10 is an absolute estimate, a complete guess. Testing needed TODO
            # If this IF passes, then it will go forth (!) until it hits a wall (not hit but you get me)
            # basically calculates whether it's pointing directly at the wall, and if so, gogogo!
            # otherwise turn in the relevant direction (actually this should probably be slow TODO)
            if (RESOLUTIONX - MAZE_MAX_X_OFFSET) <= center_x <= (RESOLUTIONX + MAZE_MAX_X_OFFSET):
                self.go_forth()
                position += 1
            elif center_x < RESOLUTIONX-MAZE_MAX_X_OFFSET:
                ROBOT.left(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
            else:
                ROBOT.right(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
        
        while True:
            if ROBOT.get_distance()[1] == 0: #i.e. it's quite far
                ROBOT.forwards()
            
            ROBOT.left(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)

    def update(self):
        '''
        No loop version of the above for snazz
        '''

        if self.is_going_forth:
            self.no_loop_go_forth()
            return

        almost_finished = False

        if not self.position >= 6:
            image = ROBOT.take_picture()

            # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            cropped_hsv = hsv[RESOLUTIONY//3:RESOLUTIONY*2//3, 0:RESOLUTIONX]

            ret, center_x, center_y = self.calculate_next_color_centroid(cropped_hsv, self.position)

            if not ret:
                if self.position < 4:
                    ROBOT.right(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
                else:
                    ROBOT.left(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
                return

            # Here, 10 is an absolute estimate, a complete guess. Testing needed TODO
            # If this IF passes, then it will go forth (!) until it hits a wall (not hit but you get me)
            if (RESOLUTIONX - MAZE_MAX_X_OFFSET) <= center_x <= (RESOLUTIONX + MAZE_MAX_X_OFFSET):
                self.is_going_forth = True
                self.position += 1
            elif center_x < (RESOLUTIONX - MAZE_MAX_X_OFFSET):
                ROBOT.left(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
            else:
                ROBOT.right(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
            return

        # This is actually really hacky, because the way that we see whether the robot is looking at the exit (i.e. the endless tunnel)
        # is by checking if the distance sensors can not sense the wall (because it is too far away) or just is far away
        if ROBOT.get_distance()[1] == 0 or ROBOT.get_distance()[1] > 175:
            ROBOT.forwards()
            self.position = 7
        else:
            ROBOT.left(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
