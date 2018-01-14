'''rainbow.py
Code for the "over the rainbow" challenge.
'''

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

from tank import TANK
import settings

colour_thresholds = {
    "red": ([17, 15, 100], [50, 56, 200]),

}


def ball_aligned(image, threshold):
    mask = cv2.inRange(image, threshold[0], threshold[1])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

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
        if radius > settings.MIN_BALL_RADIUS:
            # WHere is the circle?
            width, height = cv.GetSize(mask)
            if abs(width/2 - center[0]) < settings.BALL_OFFSET_MAX:
                return True
            else:
                return False



def run():
    visited = []
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    
    # allow the camera to warmup
    time.sleep(0.1)
    
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
    
        # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
    
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
    
        # resize the frame, blur it, and convert it to the HSV
        # color space
        image = imutils.resize(image, width=600)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(imagee, cv2.COLOR_BGR2HSV)

        for colour, thresholds in colour_thresholds:
            ensure_safe_distance()
            while not ball_aligned(hsv, thresholds):
                TANK.left()
            while not ensure_area_touched():
                TANK.forwards()



