from robot import ROBOT

while True:
    distances = ROBOT.get_distances()
    while distances[1] >= 18:
        distances = ROBOT.get_distances()
        if abs(distances[0] - distances[2]) <= 8:
            ROBOT.set_tank(-1, -1)
            distances = ROBOT.get_distances()
        elif distances[0] - distances[2] >= 8:
            while distances[0] - distances[1] >= 8:
                ROBOT.get_distances()
                ROBOT.set_tank(-1, 180/255)
        else:
            while distances[0] - distances[2] >= 8:
                ROBOT.set_tank(180/255, -1)
    while distances[1] <= 200:
        distances = ROBOT.get_distances()
        ROBOT.set_tank(-1, 1)
    while distances[1] >= 18:
        distances = ROBOT.get_distances()
        if abs(distances[0] - distances[2]) <= 8:
            ROBOT.set_tank(-1, -1)
            distances = ROBOT.get_distances()
        elif distances[0] - distances[2] >= 8:
            while distances[0] - distances[2] >= 8:
                distances = ROBOT.get_distances()
                ROBOT.set_tank(-1, 180/255)
        else:
            while distances[2] - distances[0] >= 8:
                distances = ROBOT.get_distances()
                ROBOT.set_tank(180/255, -1)
    while distances[1] <= 40:
        ROBOT.set_tank(-1 , 1)
    while distances[1] >= 18:
        distances = ROBOT.get_distances()
        if abs(distances[0] - distances[2]) <= 8:
            ROBOT.set_tank(-1 , -1)
            distances = ROBOT.get_distances()
        elif distances[0] - distances[2] >= 8:
            while distances[0] - distances[2] >= 8:
                distances = ROBOT.get_distances()
                ROBOT.set_tank(-1, 180/255)
        else:
            while distances[2] - distances[0] >= 8:
                distances = ROBOT.get_distances()
                ROBOT.set_tank(180/255, -1)
    while distances[1] <= 40:
        ROBOT.set_tank(-1, 1)
    while distances[1] >= 18:
        distances = ROBOT.get_distances()
        if abs(distances[0] - distances[2]) <= 8:
            ROBOT.set_tank(-1 , -1)
            distances = ROBOT.get_distances()
        elif distances[0] - distances[2] >= 8:
            while distances[0] - distances[2] >= 8:
                distances = ROBOT.get_distances()
                motors.RightMotors(-255)
                motors.LeftMotors(-180)
        else:
            while distances[2] - distances[0] >= 8:
                distances = ROBOT.get_distances()
                ROBOT.set_tank(-1, -180/255)
    while distances[1] <= 40:
        ROBOT.set_tank(1, -1)
    while distances[1] >= 18:
        distances = ROBOT.get_distances()
        if abs(distances[0] - distances[2]) <= 8:
            ROBOT.set_tank(1, 1)
            distances = ROBOT.get_distances()
        elif distances[0] - distances[2] >= 8:
            while distances[0] - distances[2] >= 8:
                distances = ROBOT.get_distances()
                ROBOT.set_tank(1, 180/255)
        else:
            while distances[2] - distances[0] >= 8:
                distances = ROBOT.get_distances()
                ROBOT.set_tank(180/255, 1)
    while distances[1] <= 100:
        ROBOT.set_tank(-1, 1)
    while distances[1]>=18:
        distances = ROBOT.get_distances()
        if abs(distances[0] - distances[2]) <= 8:
            ROBOT.set_tank(1, 1)
            distances = ROBOT.get_distances()
        elif distances[0] - distances[2] >= 8:
            while distances[0] - distances[2] >= 8:
                distances = ROBOT.get_distances()
                ROBOT.set_tank(1, 180/255)
        else:
            while distances[2] - distances[0] >= 8:
                distances = ROBOT.get_distances()
                ROBOT.set_tank(180/255, 1)