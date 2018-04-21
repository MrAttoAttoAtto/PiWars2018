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
    print("Left: {} Front: {} Right: {}".format(left, front, right))
    if not turning:
        if front < TURN_DIST:
            turning = True
        else:
            if COORIDOR_DIST > left > FOLLOW_DIST:
                print("Bear Left")
                ROBOT.bear_left(change=10, speed=0.5)
            elif left > COORIDOR_DIST:
                print("Turn")
                ROBOT.bear_left(change=40, speed=0.75)
            elif left < CLOSE_DIST:
                print("Bear Right")
                ROBOT.bear_right(change=10, speed=0.5)
            else:
                print("Forwards")
                ROBOT.forwards(speed=0.5)
    else:
        print("Turning")
        ROBOT.right(speed=0.75)
        if front > SAFE_F_DIST:
            turning = False
