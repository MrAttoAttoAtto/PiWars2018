'''tank.py
The interface for the hardware parts of the robot.
Access motors, ultrasonics from here.
'''
from serial import Serial
import time
import camera
from settings import SERIAL_PORT, RGB_PINS
import drive
import atexit
import RPi.GPIO as GPIO
from neopixel import Adafruit_Neopixel


class Robot:
    def __init__(self):
        '''
            All the hardware in the robot.
        '''
        self.last_left = 0
        self.last_right = 0
        try:
            self.ultrasonic_ser = Serial(SERIAL_PORT)
        except:
            print("There is no camera or distance")
        try:
            self.camera = camera.ConstantCamera()
            self.camera.start()
            self.camera.wait_for_ready()
        except Exception as e:
            self.camera = None
            print("There is no camera")

        self.driver = drive.Driver()
        atexit.register(self.shutdown)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        self.pwm = GPIO.PWM(18, 100)
        self.pwm.start(5)

        self.neopixel = Adafruit_Neopixel(1, 12)
        self.neopixel.begin()

        self.flywheels_pin = 17
        GPIO.setup(self.flywheels_pin, GPIO.OUT)

        self.servo_angle = 90
        

    def set_tank(self, speed_left, speed_right):
        '''
            Manually set values for motors.
        '''

        self.driver.turn_motors(0, int(speed_left*255))
        self.driver.turn_motors(1, int(speed_right*255))

        self.last_left = speed_left
        self.last_right = speed_right
    
    def enable_flywheel(self):
        '''Enables the flywheels'''
        GPIO.output(self.flywheels_pin, True)

    def disable_flywheel(self):
        '''Disables the flywheels'''
        GPIO.output(self.flywheels_pin, False)

    def set_colour(self, hex_value):
        '''Change the LED colour'''
        value = hex_value.lstrip('#')
        colour = tuple(int(value[i:i + 2], 16) for i in range(0, 6, 2))
        self.neopixel.setPixelColorRGB(0, *colour)
        self.neopixel.show()


    def get_distances(self):
        '''
        Uses UART Serial over USB to communicate.
        '''
        left = self.get_distance(0)
        middle = self.get_distance(1)
        right = self.get_distance(2)
        return [right, middle, left]

    def get_distance(self, index):
        self.ultrasonic_ser.write(bytes([index]))
        return ord(self.ultrasonic_ser.read())
    
    def take_picture(self):
        return self.camera.get_image()

    def forwards(self, speed=1, duration=-1):
        self.set_tank(speed, speed)
        if duration > 0:
            time.sleep(duration)
            self.halt()

    def halt(self):
        self.set_tank(0, 0)
    
    def left(self, speed=1, duration=-1):
        self.set_tank(-speed, speed)
        if duration > 0:
            time.sleep(duration)
            self.halt()

    def right(self, speed=1, duration=-1):
        self.set_tank(speed, -speed)
        if duration > 0:
            time.sleep(duration)
            self.halt()

    def bear_left(self, change=50, duration=-1, speed=1):
        '''Change is a % of straight ahead'''
        self.set_tank(speed*(1-change/100), speed*1)
    
    def bear_right(self, change=50, duration=-1, speed=1):
        '''Change is a % of straight ahead'''
        self.set_tank(speed*1, speed*(1-change/100))

    def backwards(self, speed=1, duration=-1):
        self.set_tank(-speed, -speed)
        if duration > 0:
            time.sleep(duration)
            self.halt()


    def set_servo(self, angle):
        '''Im only doing this to satisfy pylint'''
        self.pwm.ChangeDutyCycle((angle/180) * 14 + 6)
        self.servo_angle = angle

         
    def shutdown(self):
        self.camera.halt_capture()
        self.halt()
        self.ultrasonic_ser.close()
        GPIO.cleanup()


ROBOT = Robot()
