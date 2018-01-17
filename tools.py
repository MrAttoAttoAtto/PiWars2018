import time
import RPi.GPIO as GPIO

from settings import ULTRASONIC_TRIG, ULTRASONIC_ECHO

GPIO.setmode(GPIO.BCM)

def get_distance():
    '''
    Get the distance from the robot to the nearest wall
    '''

    GPIO.setup(ULTRASONIC_TRIG, GPIO.OUT)
    GPIO.setup(ULTRASONIC_ECHO, GPIO.IN)

    GPIO.output(ULTRASONIC_TRIG, False)

    time.sleep(2*10**-6)

    GPIO.output(ULTRASONIC_TRIG, True)
    time.sleep(10**-5)
    GPIO.output(ULTRASONIC_TRIG, False)

    while not GPIO.input(ULTRASONIC_ECHO):
        pulse_start = time.time()

    while GPIO.input(ULTRASONIC_ECHO):
        pulse_end = time.time()

    duration = pulse_end - pulse_start

    distance = duration * 34300/2

    distance = round(distance, 2)

    return distance

def get_centroid(boolean_image, *args):

    im2, contours, hierarchy = cv2.findContours(boolean_image.copy(), *args)

    if contours:
        # If there are countours (i.e. a line) then find the largest one (the most likely to be your line)
        # Also draws lines on the image so it can be seen by humans (not NEEDED, but good for debugging purposes)

        max_contour = max(contours, key=cv2.contourArea)
        moment = cv2.moments(max_contour)

        center_x = int(moment['m10']/moment['m00'])
        center_y = int(moment['m01']/moment['m00'])

        return center_x, center_y
    
    else:
        return (False, False)