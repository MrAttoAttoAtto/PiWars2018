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
    ROBOT.right(duration=0.3)

def left_left():
    ROBOT.left(duration=0.2)


start = time()

follow_left_wall()
right_right()
follow_left_wall()
right_right()
follow_left_wall()
right_right()

follow_left_wall(True)


distances = ROBOT.get_distances()
while distances[1] > 15:
    distances = ROBOT.get_distances()
    ROBOT.set_tank(0.6, 0.4)
ROBOT.halt()

left_left()
follow_right_wall()
left_left()
follow_right_wall()
left_left()

print(time()-start)

