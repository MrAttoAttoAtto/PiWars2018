'''Code for the maze challenge'''

import cv2

from settings import (MAZE_MAX_X_OFFSET, MAZE_MINIMUM_PERIMETER,
                      MAZE_ROBOT_FORWARD_SPEED, MAZE_ROBOT_FORWARD_TIME,
                      MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME,
                      MAZE_WALL_DISTANCE, RESOLUTIONX, RESOLUTIONY, THRESHOLDS)
from tank import ROBOT
from tools import get_centroid_and_perim

color_order = [
    "maze_yellow",
    "maze_blue",
    "maze_white",
    "maze_red",
    "maze_white",
    "maze_blue"
]

def calculate_next_color_centroid(img, pos):
    working_color = color_order[pos]
    working_thresholds = THRESHOLDS[working_color]

    mask = cv2.inRange(img, working_thresholds[0], working_thresholds[1])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    center_x, center_y, perimeter = get_centroid_and_perim(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if perimeter > MAZE_MINIMUM_PERIMETER: # again, a complete guess
        return True, center_x, center_y

    else:
        return False, 0, 0

def go_forth():
    frontal_sensor_dist = ROBOT.get_distance()[1]
    while frontal_sensor_dist > MAZE_WALL_DISTANCE or frontal_sensor_dist == 0:
        ROBOT.forwards(MAZE_ROBOT_FORWARD_SPEED, MAZE_ROBOT_FORWARD_TIME)
        frontal_sensor_dist = ROBOT.get_distance()[1]


def run():
    position = 0

    while True:
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        if position == 6:
            break

        image = ROBOT.take_picture()

        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        cropped_hsv = hsv[RESOLUTIONY//3:RESOLUTIONY*2//3, 0:RESOLUTIONX]

        ret, center_x, center_y = calculate_next_color_centroid(cropped_hsv, position)

        if not ret:
            if position < 4:
                ROBOT.right(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
            else:
                ROBOT.left(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
            
            continue

        # Here, 10 is an absolute estimate, a complete guess. Testing needed TODO
        # If this IF passes, then it will go forth (!) until it hits a wall (not hit but you get me)
        if (RESOLUTIONX - MAZE_MAX_X_OFFSET) <= center_x <= (RESOLUTIONX + MAZE_MAX_X_OFFSET):
            go_forth()
            position += 1
        elif center_x < RESOLUTIONX-MAZE_MAX_X_OFFSET:
            ROBOT.left(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
        else:
            ROBOT.right(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
    
    while True:
        if ROBOT.get_distance()[1] == 0: #i.e. it's quite far
            ROBOT.forwards()
        
        ROBOT.left(MAZE_ROBOT_TURN_SPEED, MAZE_ROBOT_TURN_TIME)
