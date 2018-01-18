import time
import drive
#import line
#import rainbow
#import settings
#import tank
import tools
import controller

control = controller.Controller()
driver = drive.Driver()

mode = {
    "line": False,
    "rainbow": False,
    "line": False,
    "maze": False
}

joy_activated = True
joy_last_toggle_time = 0
joy_toggle_delay = 0.5

while True:
    values = control.get_values()
    
    if values['control_buttons']['Start'] and joy_last_toggle_time + joy_toggle_delay < time.time():

        joy_activated = not joy_activated 
        joy_last_toggle_time = time.time()


    if joy_activated:

        leftX = values['left_axes'][0]
        leftY = values['left_axes'][1]

        driver.turn_motors(0, int(tools.translate(leftX, -1, 1, -255, 255)))
        driver.turn_motors(1, int(tools.translate(leftX, -1, 1, -255, 255)))



    if mode['line']:
        pass
    
    if mode['rainbow']:
        pass

    if mode['maze']:
        pass

    

def shift_mode(new_mode):
    for key in mode:
        mode[key] = (key == new_mode)
    

driver.safe_shutdown()