from robot import ROBOT
from time import time, sleep

def follow_left_wall(middle=False):
    while True:
        distances = ROBOT.get_distances()


        if distances[0] > 40 and middle:
            ROBOT.halt()
            return
        
        print(distances)
        if 0 < distances[1] <= 18 and not middle:
            ROBOT.halt()
            print("wallended")
            return
        elif distances[0] <= 10:
            ROBOT.right(duration=0.06)
            print("bearing right")
        elif distances[2] <= 10 or distances[0] > 20:
            ROBOT.left(duration=0.06)
            print("bearing left")
        else:
            ROBOT.set_tank(0.6, 0.45)

def follow_right_wall(last=False):
    start = time()
    while True:
        distances = ROBOT.get_distances()
        print(distances)

        if last:
            now = time()
            if now - start >= 2.25:
                ROBOT.set_tank(1, 0.8)
                sleep(3)
                ROBOT.halt()
                return

            
        
        if 0 < distances[1] <= 18:
            ROBOT.halt()
            print("wallended")
            
            return
        elif distances[2] <= 10:
            ROBOT.left(duration=0.06)
            print("bearing right")
        elif distances[2] > 20:
            ROBOT.right(duration=0.06)
            print("bearing left")
        else:
            ROBOT.set_tank(0.6, 0.45)

def right_right():
    """
    while True:
        ROBOT.right(duration=0.1)
        distances= ROBOT.get_distances()
        if distances[1] > thresh:
            ROBOT.right(duration=0.1)
            return
    """
    ROBOT.right(duration=0.48)

def left_left(specie=False):
    if specie:
        ROBOT.left(duration=0.38)
    else:
        ROBOT.left(duration=0.48)

start = time()

#follow_left_wall()
#right_right()
#follow_left_wall()
#right_right()
#follow_left_wall)
#right_right()
if ROBOT.get_distances()[1] <= 18:
    left_left()
    left_left()
    annoying=True
else:
    follow_left_wall(middle=True)
ROBOT.set_tank(0.6, 0.45)
sleep(0.6)
left_left()
ROBOT.set_tank(0.6, 0.45)
sleep(0.4)
follow_right_wall()
left_left()
follow_right_wall(True)
diff = time()-start
print(diff)
print(annoying)

