from robot import ROBOT
TURN_DIST = 15
SAFE_F_DIST = 40
COORIDOR_DIST = 40
FOLLOW_DIST = 10
CLOSE_DIST = 5

turning = False
def update():
    '''Proto for right corners... not comprehensive'''
    global turning
    right, front, left = ROBOT.get_distances()
    if not turning:
        if front < TURN_DIST:
            turning = True
        else:
            if left > FOLLOW_DIST:
                ROBOT.bear_left(change=10, speed=0.5)
            elif left < CLOSE_DIST:
                ROBOT.bear_right(change=10, speed=0.5)
            else:
                ROBOT.forwards(speed=0.5)
    else:
        ROBOT.right(speed=0.75)
        if front > SAFE_F_DIST:
            turning = False
