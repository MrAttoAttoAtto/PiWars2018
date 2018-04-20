'''General constants and settings
that may be required between programs
or are just stored here for easy tweaking'''

import json
import numpy as np

DEBUG = True

RESOLUTIONX = 640
RESOLUTIONY = 480

SERIAL_PORT = "/dev/ttyUSB0"

START_HOLD_REQUIRED = 4

RGB_PINS = [25, 24, 23]

# ----COLORS-----
# This is a DICTIONARY of the form:
# {"yellow":[[h_bot, s_bot, v_bot], [h_top, s_top, v_top]], "red":...}
PURE_THRESHOLDS = json.load(open("thresholds.json"))

THRESHOLDS = {}

for key, value in PURE_THRESHOLDS.items():
    THRESHOLDS[key] = np.array(value)

# ----RAINBOW----
MIN_BALL_RADIUS = 10
BALL_OFFSET_MAX = 160
REVERSE_TIME = 1
SPEED_SCALE = 0.8/2
ENABLE_TURN_CORRECTION = True
ENABLE_FIRST_TURN_CORRECTION = False
TURN_CORRECTION_TIME = 0.2

#------MAZE------

# This var is the max X offset of the centroid for
# the robot still to go forwards (in px)
MAZE_MAX_X_OFFSET = 10

# This var is the minimum perimeter of the detected color
# for it to be considered legitimate (in px?)
MAZE_MINIMUM_PERIMETER = 25

# This var is the distance away from the wall at which the robot
# stops moving and turns again (in cm)
MAZE_WALL_DISTANCE = 10

# Vars for the turn speed specific to the maze challenge
MAZE_ROBOT_TURN_SPEED = 1
MAZE_ROBOT_TURN_TIME = 0.55

# Vars for the forward-moving speed specific to the maze challenge
MAZE_ROBOT_FORWARD_SPEED = 1
MAZE_ROBOT_FORWARD_TIME = 0.25

#-------MAZE 2.0-----
MAZE_CLOSE_THRESH = 15
MAZE_SIDE_THRESH = 42
MAZE_PICKINESS = 40
MIN_MARKER_RADIUS = 10

#-------LINE---------
LINE_SENSITIVITY = 100 #lower less sensitive
LINE_BEAR_NUM = 25 #le % of bear
