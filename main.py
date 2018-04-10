"""main.py
The script which runs. The mainloop. Quite frightening.
"""
import sys
import time

import controller
# from modes import line, manual_drive, maze, rainbow
from modes import golf, line, manual_drive, maze2, rainbow
from robot import ROBOT

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = "manual"

    control = controller.Controller()

    MODES = ["manual", "line", "rainbow", "maze", "select", "golf"]
    COLOURS = ["#000000", "#ffffff", "#3f32ae", "#e30ec2", "#e80200", "#16ed75", "#efe305"]

    joy_last_select_time = 0
    selected_mode = "manual"

    JOY_TOGGLE_DELAY = 1
    led_state = True
    led_time = 0

    rainbow_begin = False
    maze2_begin = False

    while True:
        values = control.get_values()

        if values['control_buttons']['Start'] and joy_last_select_time + JOY_TOGGLE_DELAY < time.time() and mode != "selection":
            mode = "selection"
            first = True
            joy_last_select_time = time.time()
            time.sleep(1)

        mode = 'maze'
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
                current_index = MODES.index(selected_mode)
                new_index = 0 if current_index+1 == len(MODES) else current_index+1
                selected_mode = MODES[new_index]

            if values["bumpers"][0]:
                current_index = MODES.index(selected_mode)
                new_index = current_index-1
                selected_mode = MODES[new_index]

            if led_time == 20:
                if led_state:
                    ROBOT.set_colour(COLOURS[0])
                else:
                    ROBOT.set_colour(COLOURS[MODES.index(selected_mode)+1])
                led_state = not led_state
                led_time = 0
            else:
                led_time += 1

            if values['control_buttons']['Back']:
                mode = selected_mode
                ROBOT.set_colour(COLOURS[MODES.index(selected_mode)+1])


        if mode == "line":
            line.update()

        if mode == "rainbow":
            if not rainbow_begin:
                rainbow_begin = True
                rainbown = rainbow.Rainbow()
                rainbown.running = True
            else:
                rainbown.update(0)

        if mode == "maze":
            if not maze2_begin:
                maze2_begin = True
                maze2n = maze2.Maze2()
            else:
                maze2n.update()

        if mode == "manual":
            manual_drive.update(values)
        
        if mode == "golf":
            golf.update(values)



    ROBOT.driver.safe_shutdown()
