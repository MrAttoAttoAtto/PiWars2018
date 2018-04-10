'''tank.py
The interface for the hardware parts of the robot.
Access motors, ultrasonics from here.
'''
from smbus import SMBus
import time
import camera
from settings import address
import drive
import atexit
import RPi.GPIO as GPIO


class Robot:
    def __init__(self, ultrasonic_address=address):
        '''
            All the hardware in the robot.
        '''
        self.last_left = 0
        self.last_right = 0

        self.ultrasonic_address = ultrasonic_address
        self.ultrasonic_connection = SMBus(1)
        try:
            self.camera = camera.ConstantCamera()
            self.camera.start()
            self.camera.wait_for_ready()
        except Exception as e:
            self.camera = None

        self.driver = drive.Driver()
        atexit.register(self.shutdown)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
    
        self.pwm = GPIO.PWM(18, 100)
        self.pwm.start(5)

        self.flywheels = [10, 11, 14, 15] #TO BE CONFIRMED
        # Motors across a,b and c,d
        for motor in self.flywheels:
            GPIO.setup(motor, GPIO.OUT)
        

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
        for motor in self.flywheels:
            if motor % 2 == 0:
                GPIO.output(motor, True)
            else:
                GPIO.output(motor, False)

    def disable_flywheel(self):
        '''Disables the flywheels'''
        for motor in self.flywheels:
            GPIO.output(motor, False)

    def set_colour(self, colour_num):
        if 0 <= colour_num <= 5:
            self.ultrasonic_connection.write_byte(self.ultrasonic_address, colour_num)


    def get_distance(self):
        '''
        Uses I2C to talk to an arduino nano, getting all distances from multiple
        ultrasonic sensors
            WIRING:
            RPI's GND = PIN06 -----> ARDUINO NANO'S GND
            RPI'S SDA = GPIO02 = PIN03 -----> ARDUINO NANO'S SDA = A4
            RPI'S SCL = GPI03 = PIN05 -----> ARDUINO NANO'S SCL = A5
        '''
        left = self.ultrasonic_connection.read_byte(self.ultrasonic_address)
        middle = self.ultrasonic_connection.read_byte(self.ultrasonic_address)
        right = self.ultrasonic_connection.read_byte(self.ultrasonic_address)
        return [right, middle, left]

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

    def bear_left(self, change=50, duration=-1):
        '''Change is a % of straight ahead'''
        self.set_tank(1-change/100, 1)
    
    def bear_right(self, change=50, duration=-1):
        '''Change is a % of straight ahead'''
        self.set_tank(1, 1-change/100)

    def backwards(self, speed=1, duration=-1):
        self.set_tank(-speed, -speed)
        if duration > 0:
            time.sleep(duration)
            self.halt()


    def set_servo(self, angle):
        '''Im only doing this to satisfy pylint'''
        self.pwm.ChangeDutyCycle((angle/180) * 14 + 6)

         
    def shutdown(self):
        self.camera._close_event.set()
        self.halt()


ROBOT = Robot()
