'''rainbow.py
Code for the "over the rainbow" challenge.
1st time
	turn right, until a ball of one of four colors is seen, append with angle
	^ x3
	check what direction to turn for red
	turn that direction until red spotted
	move forwards until proximity too close
	move backwards a pre-specified distance so that rotation is a-ok

	^ x3 for other colors in order

'''

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import imutils

from tank import TANK
from settings import MIN_BALL_RADIUS, BALL_OFFSET_MAX
from tools import get_centroid

colour_thresholds = {
    "red": ([17, 15, 100], [50, 56, 200]),

}

def ball_aligned(image, threshold):
    mask = cv2.inRange(image, threshold[0], threshold[1])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

	# only proceed if at least one contour was found
    if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > MIN_BALL_RADIUS:
            # WHere is the circle?
            width, height = cv2.GetSize(mask)
            if abs(width/2 - center[0]) < BALL_OFFSET_MAX:
                return True
    
    return False



def run():
    visited = []
    # initialize the camera and grab a reference to the raw camera capture
    camera = TANK.camera
    raw_capture = PiRGBArray(camera, size=(640, 480))
    
    # allow the camera to warmup
    time.sleep(0.1)
    
    # capture frames from the camera
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array    
    
        # resize the frame, blur it, and convert it to the HSV
        # color space
        image = imutils.resize(image, width=600)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        for colour, thresholds in colour_thresholds:
            ensure_safe_distance() # TODO
            while not ball_aligned(hsv, thresholds): # THIS WILL NOT WORK TODO (IT NEVER REFRESHES THE IMAGE AND WILL THEREFORE CONTINUE FOREVER)
                TANK.left()
            while not ensure_area_touched(): # TODO
                TANK.forwards()

        # clear the stream in preparation for the next frame
        raw_capture.truncate(0)
