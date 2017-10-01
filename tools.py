import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

TRIG = 23 #change to whatever they acc are
ECHO = 24

def get_distance():
    '''
    Get the distance from the robot to the nearest wall
    '''

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)

    time.sleep(2*10**-6)

    GPIO.output(TRIG, True)
    time.sleep(10**-5)
    GPIO.output(TRIG, False)

    while not GPIO.input(ECHO):
        pulse_start = time.time()

    while GPIO.input(ECHO):
        pulse_end = time.time()

    duration = pulse_end - pulse_start

    distance = duration * 34300/2

    distance = round(distance, 2)

    return distance
