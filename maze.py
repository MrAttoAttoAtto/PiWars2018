'''Code for the maze challenge'''

import time

from picamera.array import PiRGBArray
from settings import RESOLUTIONX, RESOLUTIONY
from tank import TANK

color_order = [
    "yell",
    "blue",
    "white",
    "red",
    "white",
    "blue"
]

def get_main_color(img):
    flags = cv2.KMEANS_RANDOM_CENTERS
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))
    centers = cv2.kmeans(image, 1, None, criteria, 10, flags)[2]

    return list(centers[0])

def run():
    # get camera
    camera = TANK.camera
    raw_capture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)

    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array    

        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        cropped_bgr = image[RESOLUTIONY//2-10:RESOLUTIONY//2+10, RESOLUTIONX//2-10:RESOLUTIONX//2+10]

        major_color = get_main_color(cropped_bgr)
        print(major_color)
