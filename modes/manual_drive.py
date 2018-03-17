from robot import ROBOT
import tools

def update(values):
    joyX = int(tools.translate(values['left_axes'][0], -1, 1, -255, 255))
    joyY = int(tools.translate(values['left_axes'][1], -1, 1, -255, 255))

    left_speed = joyX + joyY
    right_speed = joyX - joyY

    ROBOT.driver.turn_motors(0,left_speed)
    ROBOT.driver.turn_motors(1, right_speed)