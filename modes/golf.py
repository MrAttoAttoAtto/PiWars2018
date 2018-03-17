from robot import ROBOT
import tools

def update(values):
    if values["button_pad"]['A']:
        ROBOT.set_servo(13)
    else:
        joyY = int(tools.translate(values['right_axes'][1], -1, 1, 6, 20))
        ROBOT.set_servo(joyY)