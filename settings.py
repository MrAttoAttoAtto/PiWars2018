'''General constants and settings
that may be required between programs
or are just stored here for easy tweaking'''

import json

DEBUG = False

ULTRASONIC_TRIG = 23
ULTRASONIC_ECHO = 24

RESOLUTIONX = 640
RESOLUTIONY = 480

# ----COLORS-----
# This is a DICTIONARY of the form:
# {"yellow":[[h_bot, s_bot, v_bot], [h_top, s_top, v_top]], "red":...}
THRESHOLDS = json.load(open("thresholds.json"))

# ----RAINBOW----
MIN_BALL_RADIUS = 10
BALL_OFFSET_MAX = 50