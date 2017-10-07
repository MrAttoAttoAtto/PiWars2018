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
