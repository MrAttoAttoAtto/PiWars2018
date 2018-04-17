from robot import ROBOT
FRONT_THRESH = 10
TURN_DURATION = 5
CORRIDOR_THRESH = 20
ALIGN_THRESH = 5
def update():
    right, front, left = ROBOT.get_distances()
    if front < FRONT_THRESH:
        if left < right:
            ROBOT.right(duration=TURN_DURATION)
        else:
            ROBOT.left(duration=TURN_DURATION)
    else:
        if ALIGN_THRESH < abs(left-right) < CORRIDOR_THRESH:
            if left < right:
                ROBOT.bear_right()
            else:
                ROBOT.bear_left()
        else:
            ROBOT.forwards()



        