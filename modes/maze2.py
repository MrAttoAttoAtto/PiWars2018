"""
Should navigate the maze, using a hyped up hug the wall tactic (probs needs some fixing though)
"""
from time import sleep

from robot import ROBOT
from settings import DEBUG, MAZE_CLOSE_THRESH, MAZE_PICKINESS, MAZE_SIDE_THRESH


class Maze2:
    def __init__(self):
        self.state = "forwards"
        self.side_dist = 0

    @staticmethod
    def dprint(txt):
        if DEBUG:
            print(txt)

    def update(self):
        distances = ROBOT.get_distance()
        if self.state == "forwards":
            """Checks if robot has space on either side, i.e a turn, and if so, takes it
            making sure that it is a wide turn so as not to hit a wall"""

            if distances[0] > MAZE_SIDE_THRESH:
                ROBOT.set_tank(-0.1, 0.6)
                self.state = "turning"
                self.side_dist = distances[0]
                self.dprint("Left turn sighted!")
            elif distances[2] > MAZE_SIDE_THRESH:
                ROBOT.set_tank(0.6, -0.1)
                self.state = "turning"
                self.side_dist = distances[2]
                self.dprint("Right turn sighted!")

            elif distances[0] < MAZE_CLOSE_THRESH:
                ROBOT.bear_right()
                self.dprint("Bearing right")
            elif distances[2] < MAZE_CLOSE_THRESH:
                self.dprint("Bearing left")
                ROBOT.bear_left()

            else:
                ROBOT.forwards()
                self.dprint("Forwards!")

        elif self.state == "turning":
            if self.side_dist - MAZE_PICKINESS < distances[1] < self.side_dist + MAZE_PICKINESS:
                self.dprint("Turning stopped!")
                ROBOT.forwards()
                self.state = "forwards"
                sleep(0.5)
