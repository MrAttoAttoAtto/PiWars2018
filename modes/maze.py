'''Code for the maze challenge'''

import time

from picamera.array import PiRGBArray
from settings import RESOLUTIONX, RESOLUTIONY, THRESHOLDS
from tank import TANK

color_order = [
    "yellow",
    "blue",
    "white",
    "red",
    "white",
    "blue"
]

def calculate_next_color_centroid(img, thresholds):
    pass

def run():
    # get camera
    camera = TANK.camera
    raw_capture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)

    position = 0

    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array    

        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        cropped_bgr = image[RESOLUTIONY//2-10:RESOLUTIONY//2+10, RESOLUTIONX//2-10:RESOLUTIONX//2+10]

        ret, center_x, center_y = calculate_next_color_centroid()
