"""
Should navigate the maze, using a hyped up hug the wall tactic (probs needs some fixing though)
"""
from robot import ROBOT
from settings import DEBUG
from time import sleep

CLOSE_THRESH = 10
SIDE_THRESH = 30
PICKINESS = 20

state = "forwards"
side_dist = 0

def dprint(txt):
    if DEBUG:
        print(txt)

def update():
    distances = ROBOT.get_distance()
    if state == "forwards":
        """Checks if robot has space on either side, i.e a turn, and if so, takes it
        making sure that it is a wide turn so as not to hit a wall""" 

        if distances[0] > SIDE_THRESH:
            ROBOT.set_tank(0.6, -0.1)
            state = "turning"
            side_dist = distances[0]
            dprint("Left turn sighted!")
        elif distances[2] > SIDE_THRESH:
            ROBOT.set_tank(-0.1, 0.6)
            state = "turning"
            side_dist = distances[2]
            dprint("Right turn sighted!")

        elif distances[0] < CLOSE_THRESH:
            ROBOT.bear_right()
            dprint("Bearing right")
        elif distances[2] < CLOSE_THRESH:
            dprint("Bearing left")
            ROBOT.bear_left()

        else:
            ROBOT.forwards()
            dprint("Forwards!")

    elif state == "turning":
        if side_dist - PICKINESS < distances[1] < side_dist + PICKINESS:
            dpront("Turning stopped!")
            ROBOT.forwards()
            state = "forwards"
            sleep(0.5)