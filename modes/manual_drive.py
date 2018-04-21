from robot import ROBOT
import tools

SPEED = 0.5

def update(values, not_max=False):
    joyX = int(tools.translate(values['left_axes'][0], -1, 1, -255, 255))
    joyY = int(tools.translate(values['left_axes'][1], -1, 1, -255, 255))

    left_speed = joyX + joyY
    right_speed = joyY - joyX

    if not_max:
        left_speed *= SPEED
        right_speed *= SPEED

    ROBOT.driver.turn_motors(0,left_speed)
    ROBOT.driver.turn_motors(1, right_speed)
