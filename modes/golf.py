from robot import ROBOT
from modes import manual_drive


def update(values):
    manual_drive.update(values)
    if values["button_pad"]['A']:
        ROBOT.set_servo(90)
    else:
        joyY = values['right_axes'][1]
        print(joyY)
        ROBOT.set_servo(ROBOT.servo_angle+(joyY*6))
