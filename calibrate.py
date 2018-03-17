'''Python file for color calibration at the event'''

import colorsys
import json
import time

import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

from settings import RESOLUTIONX, RESOLUTIONY, THRESHOLDS

def get_main_color(img):
    '''
    Calculates the main color by using a k-means algorithm, after having
    formatted the image array correctly
    '''
    flags = cv2.KMEANS_RANDOM_CENTERS
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))
    img = np.float32(img)
    centers = cv2.kmeans(img, 1, None, criteria, 10, flags)[2]

    return list(centers[0])

def calibrate_spec(color, cam):
    '''
    Takes a pic, gets the average color of the 20x20 middle bit, and sets,
    if the user thinks it looks good, the threshold to around those values globally
    '''

    #assert color in THRESHOLDS

    camera = cam
    raw_capture = PiRGBArray(camera, size=(640, 480))

    # time to be put into place
    input("Press enter to take photograph")

    camera.capture(raw_capture, format='bgr')

    image = raw_capture.array

    cropped_bgr = image[RESOLUTIONY//2-10:RESOLUTIONY//2+10, RESOLUTIONX//2-10:RESOLUTIONX//2+10]

    image = cv2.rectangle(image, (RESOLUTIONX//2+10, RESOLUTIONY//2+10), (RESOLUTIONX//2-10, RESOLUTIONY//2-10), (255, 255, 255))
    cv2.imshow("YOO", image)
    cv2.waitKey()

    major_color = get_main_color(cropped_bgr)
    print("RGB: " + str(major_color))

    hsv_major_color = list(colorsys.rgb_to_hsv(major_color[0], major_color[1], major_color[2]))
    hsv_major_color[0] = (hsv_major_color[0]*179)
    hsv_major_color[1] = (hsv_major_color[1]*255)

    print("HSV: " + str(hsv_major_color))

    confirmation = input("Does this look okay? [y/N] ")

    if confirmation.lower() == "y":
        min_thresh = [coolio-10 for coolio in hsv_major_color]
        max_thresh = [hsv_major_color[0]+10, 255, 255]


        THRESHOLDS[color] = [min_thresh, max_thresh]
        print(THRESHOLDS[color])
        json.dump(THRESHOLDS, open("thresholds.json", "w"), sort_keys=True, indent=4)


        return True

    return False

def calibrate_all():
    '''Calibrates all of the colors in the threshold dictionary from scratch'''

    camera = PiCamera()
    camera.resolution = (640, 480)

    for key in THRESHOLDS:
        confirmation = input("The next color is \"{}\". Press q + [enter] to go to the next color or [enter] to start the 3 sec countdown to take the picture: ".format(key))

        if confirmation.lower() == "q":
            continue

        while True:
            ret = calibrate_spec(key, camera)

            if not ret:
                redo_quest = input("You seemed to cancel that image, do you want to take it again? [Y/n] ")

                if redo_quest.lower() == "n":
                    break

            else:
                break

if __name__ == "__main__":
    calibrate_all()
