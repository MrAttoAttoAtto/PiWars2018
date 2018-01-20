"""main.py
The script which runs.
"""
import time
import drive
from tank import ROBOT
from modes import line, manual_drive, maze, rainbow
import settings
import tools
import controller

control = controller.Controller()
driver = drive.Driver()

modes = ["manual", "line", "rainbow", "maze"]
mode = "manual"


while True:
    values = control.get_values()
    
    if values['control_buttons']['Start'] and joy_last_toggle_time + joy_toggle_delay < time.time():

        joy_activated = not joy_activated 
        joy_last_toggle_time = time.time()




    if mode == "line":
        line.update()
    
    if mode == "rainbow":
        pass

    if mode == "maze":
        pass

    if mode == "manual":
        leftX = values['left_axes'][0]
        leftY = values['left_axes'][1]

        driver.turn_motors(0, int(tools.translate(leftX, -1, 1, -255, 255)))
        driver.turn_motors(1, int(tools.translate(leftX, -1, 1, -255, 255)))

    

def shift_mode(new_mode):
    for key in mode:
        mode[key] = (key == new_mode)
    

driver.safe_shutdown()