from robot import ROBOT
def update():
    right, front, left = ROBOT.get_distances()
    if front < 15:
        ROBOT.right(duration=0.48)
    else:
        if left > 10:
            ROBOT.bear_left(change=10, speed=0.5)
        else:
            ROBOT.forwards(speed=0.5)