"""main.py
The script which runs. The mainloop. Quite frightening.
"""
import time
import drive
from robot import ROBOT
#from modes import line, manual_drive, maze, rainbow
from modes import rainbow
import settings
import tools
import controller
import leds

def shift_mode(new_mode):
    global mode
    global selection_mode
    
    mode = new_mode
    selection_mode = False
    new_color = mode_colours[modes.index(new_mode)]

    ROBOT.set_colour(modes.index(new_mode))

control = controller.Controller()

mode_index = 0
modes = ["manual", "line", "rainbow", "maze", "select"]
mode_colours = ["red", "cyan", "orange", "magenta", "white"]
mode = "manual"

selection_mode = False
joy_last_select_time = 0
selected_mode = "manual"

joy_toggle_delay = 1
led_state = True
led_time = 0

rainbow_begin = False


def shift_mode(new_mode):
    global mode
    global selection_mode
    
    mode = new_mode
    selection_mode = False
    new_color = mode_colours[modes.index(new_mode)]

    leds.changecolor(new_color)

while True:
    values = control.get_values()
    

    if values['control_buttons']['Start'] and joy_last_select_time + joy_toggle_delay < time.time() and not selection_mode:
        print("b")
        selection_mode = not selection_mode
        mode = "selection"
        joy_last_select_time = time.time()


    if mode == "selection":
        if values["button_pad"]['A']:
            selected_mode = "line"
            
        elif values["button_pad"]['B']:
            selected_mode = "rainbow"

        elif values["button_pad"]['Y']:
            selected_mode = "maze"

        elif values["button_pad"]['X']:
            selected_mode = "manual"
        
        if values["bumpers"][1]:
            mode_index += 1
            if mode_index == len(modes):
                mode_index = 0
            selected_mode = modes[mode_index]

        if values["bumpers"][0]:
            mode_index -= 1
            if mode_index == -1:
                mode_index = 0
            selected_mode = modes[mode_index]

        if led_time == 20:
            if led_state:
                ROBOT.set_colour(0)
            else:
                ROBOT.set_colour(modes.index(selected_mode)+1)
            led_state = not led_state
            led_time = 0
        else:
            led_time += 1

        if values['control_buttons']['Start']:
            shift_mode(selected_mode)
        
                    

    if mode == "line":
        pass

    if mode == "rainbow":
        if not rainbow_begin:
            rainbow_begin = True
            rainbown = rainbow.Rainbow()
        else:
            rainbown.update(values['button_pad']['Y'])

    if mode == "maze":
        pass

    if mode == "manual":
        joyX = int(tools.translate(values['left_axes'][0], -1, 1, -255, 255))
        joyY = int(tools.translate(values['left_axes'][1], -1, 1, -255, 255))

        left_speed = joyX + joyY
        right_speed = joyX - joyY

        ROBOT.driver.turn_motors(0,left_speed)
        ROBOT.driver.turn_motors(1, right_speed)

ROBOT.driver.safe_shutdown()
