"""
Should navigate the maze, using a hyped up hug the wall tactic (probs needs some fixing though)
"""
import queue
import threading
from time import sleep

import cv2
import numpy as np

from robot import ROBOT
from settings import (DEBUG, MAZE_CLOSE_THRESH, MAZE_PICKINESS,
                      MAZE_ROBOT_TURN_TIME, MAZE_SIDE_THRESH,
                      MIN_MARKER_RADIUS, THRESHOLDS)


class Maze2:
    def __init__(self):
        self.state = "forwards"
        self.side_dist = 0
        self.count = 0
        self.turn = 0
        self.follow_side = 2
        self.side = 0
        self.detection_queue = queue.Queue(1)

        self.detection_thread = threading.Thread(None, self.detect_marker)
        self.detection_thread.setDaemon(True)
        self.detection_thread.start()

    @staticmethod
    def dprint(txt):
        if DEBUG:
            print(txt)

    def update(self):
        #The original maze2
        """
        self.count += 1

        distances = ROBOT.get_distance()
        if self.count > 1000:
            self.dprint(distances)
            self.count = 0
        if self.state == "forwards":
            Checks if robot has space on either side, i.e a turn, and if so, takes it
            making sure that it is a wide turn so as not to hit a wall

            if distances[0] > MAZE_SIDE_THRESH or distances[0] == 0:
                self.dprint("Left turn sighted Wall on the left is {} away!".format(distances[0]))
                self.state = "turning"
                self.side_dist = distances[0]
                sleep(0.3)
                ROBOT.set_tank(-1, 1)
            elif distances[2] > MAZE_SIDE_THRESH or distances[2] == 0:
                self.dprint("Right turn sighted Wall on the right is {} away!".format(distances[2]))
                self.state = "turning"
                self.side_dist = distances[2]
                sleep(0.3)
                ROBOT.set_tank(1, -1)


            elif 0 < distances[0] < MAZE_CLOSE_THRESH:
                ROBOT.bear_right()
                self.dprint("Bearing right")
            elif 0 < distances[2] < MAZE_CLOSE_THRESH:
                self.dprint("Bearing left")
                ROBOT.bear_left()

            else:
                ROBOT.forwards(speed=0.5)
                self.dprint("Forwards!")

        elif self.state == "turning":
            #self.dprint("Turning! Waiting for {}, getting {}".format(self.side_dist, distances[1]))
            if distances[1] >= MAZE_PICKINESS:
                self.dprint("Turning stopped!")
                ROBOT.forwards(speed=0.5)
                self.state = "forwards"
                sleep(0.5)
        """
        #The second maze2
        """
        distances = ROBOT.get_distance()

        
        if distances[self.follow_side] > 10 or distances[self.follow_side] == 0:
            print("Bear RIGHT {}".format(distances[self.follow_side]))
            if self.follow_side == 0:
                ROBOT.bear_left(change=100)
            else:
                ROBOT.bear_right(change=100)
        elif distances[self.follow_side] <= 5:
            print("Bear LEFT {}".format(distances[self.follow_side]))
            if self.follow_side == 0:
                ROBOT.bear_right(change=100)
            else:
                ROBOT.bear_left(change=100)
        else:
            print("{} From right wall, going forwards".format(distances[self.follow_side]))
            ROBOT.forwards(speed=0.5)
        """
        #the third maze2

        '''
        distances = ROBOT.get_distance()
        print(distances)
        print("LEFT = " + str(ROBOT.last_left) + " RIGHT = " + str(ROBOT.last_right))
        if distances[2] > 60 and 0 < distances[1] <= 15:
            ROBOT.right(duration=0.25)
            print("turning right")
        #if 0 < distances[0] < 30 and 0 < distances[1] <=15:
         #   ROBOT.right(duration=0.2)
          #  
           # print("turning right")
        elif 0 < distances[2] <= 10 and distances[0] > distances[2]:
            ROBOT.left(duration=0.05)
            print("bearing left")
        elif 0 < distances[0] <= 10 and distances[2] > distances[0]:
            ROBOT.right(duration=0.05)
            print("bearing right")
        else:
            ROBOT.forwards(speed=0.25)
            print("forwards")
        '''

        '''
        #the third.five maze2 (with direction changeness :))
        should_change_section = bool(self.detection_queue.qsize()) if self.side == 0 else False

        turn_function = ROBOT.right if self.side == 0 else ROBOT.left
    
        distances = ROBOT.get_distance()
        if distances[abs(self.side-2)] <= 15 and distances[1] <= 15:
            turn_function(duration=0.25)
        elif 0 < distances[2] <= 10 and distances[0] > distances[2]:
            ROBOT.left(duration=0.05)
            #print("bearing left")
        elif 0 < distances[0] <= 10 and distances[2] > distances[0]:
            ROBOT.right(duration=0.05)
            #print("bearing right")
        else:
            ROBOT.forwards(speed=0.25)
            self.side = 2 if should_change_section else self.side

    def detect_marker(self):
        while True:
            image = ROBOT.take_picture()

            working_thresholds = np.array(THRESHOLDS["MAZE_MARKER"])

            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv, working_thresholds[0], working_thresholds[1])
            # Make the shapes more regular
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            if cnts:
                max_contour = max(cnts, key=cv2.contourArea)
                ((x_pos, y_pos), radius) = cv2.minEnclosingCircle(max_contour)
                x_pos = int(x_pos)
                y_pos = int(y_pos)

                if radius > MIN_MARKER_RADIUS:
                    self.detection_queue.put(True)
    '''

    #the mazest simples

    distances = ROBOT.get_distance()
    print(distances)
    if distances[0] > distances[2] and distances[0] > 60 and distances[1] <= 15:
        ROBOT.left(duration=0.1)
        print("left")
    elif distances[2] > distances[0] and distances[2] > 60 and distances[1] <= 15:
        ROBOT.right(duration=0.1)
        print("right")
    else:
        ROBOT.forwards(speed=0.25)
        print("forwards")
    