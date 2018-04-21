from robot import ROBOT
import tools

SPEED = 1

def update(values, not_max=False):
    global SPEED
    joyX = int(tools.translate(values['left_axes'][0], -1, 1, -255, 255))
    joyY = int(tools.translate(values['left_axes'][1], -1, 1, -255, 255))

    if values["d_pad"]["Up"]:
        SPEED = 1
    elif values["d_pad"]["Down"]:
        SPEED = 0.5

    print(SPEED)

    left_speed = joyX + joyY
    right_speed = joyY - joyX

    
    left_speed *= SPEED
    right_speed *= SPEED

    ROBOT.driver.turn_motors(0, int(left_speed))
    ROBOT.driver.turn_motors(1, int(right_speed))
