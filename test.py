from robot import ROBOT

def follow_left_wall():
    distances = ROBOT.get_distances()
    if distances[1] <= 10:
        ROBOT.halt()
        return
    elif distances[0] > distances[2]:
        ROBOT.bear_left(speed=0.5)
        print("bear left")
    elif distances[2] > distances[0]:
        ROBOT.bear_right(speed=0.5)
        print("bear right")
    else:
        ROBOT.forwards(speed=0.5)

follow_left_wall()
