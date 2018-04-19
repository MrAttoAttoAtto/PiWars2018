from robot import ROBOT
FRONT_THRESH = 10
TURN_DURATION = 0.4
CORRIDOR_THRESH = 40
ALIGN_THRESH = 10
def update():
    right, front, left = ROBOT.get_distances()
    if front < FRONT_THRESH:
        if left > right:
            ROBOT.right(duration=TURN_DURATION, speed=0.5)
        else:
            ROBOT.left(duration=TURN_DURATION, speed=0.5)
    else:
        if ALIGN_THRESH < abs(left-right) < CORRIDOR_THRESH:
            if left < right:
                ROBOT.bear_right(speed=0.5)
            else:
                ROBOT.bear_left(speed=0.5)
        else:
            ROBOT.forwards(speed=0.5)



        
