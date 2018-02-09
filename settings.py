'''General constants and settings
that may be required between programs
or are just stored here for easy tweaking'''

import json

DEBUG = False

RESOLUTIONX = 640
RESOLUTIONY = 480

address = 0x04

START_HOLD_REQUIRED = 4

# ----COLORS-----
# This is a DICTIONARY of the form:
# {"yellow":[[h_bot, s_bot, v_bot], [h_top, s_top, v_top]], "red":...}
THRESHOLDS = json.load(open("thresholds.json"))

# ----RAINBOW----
MIN_BALL_RADIUS = 10
BALL_OFFSET_MAX = 50

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
MAZE_ROBOT_TURN_TIME = 0.25

# Vars for the forward-moving speed specific to the maze challenge
MAZE_ROBOT_FORWARD_SPEED = 1
MAZE_ROBOT_FORWARD_TIME = 0.25
