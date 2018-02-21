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
            raise e
            self.camera = None

        self.driver = drive.Driver()
        atexit.register(self.shutdown)

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
        pass

    def disable_flywheel(self):
        '''Disables the flywheels'''
        pass

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
        #TODO ADD MIDDLE ULTRASONIC TO ARDUINO AND WORKING RIGHT TO ARDUINO
        middle = self.ultrasonic_connection.read_byte(self.ultrasonic_address)
        right = self.ultrasonic_connection.read_byte(self.ultrasonic_address)
        return [left, middle, right]

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
        '''Change is a % of the prior speed'''
        prior_left = self.last_left
        prior_right = self.last_right

        self.set_tank(prior_left*change/100, prior_right)
        if duration > 0:
            time.sleep(duration)
            self.set_tank(prior_left, prior_right)
    
    def bear_right(self, change=50, duration=-1):
        '''Change is a % of the prior speed'''
        prior_left = self.last_left
        prior_right = self.last_right

        self.set_tank(prior_left, prior_right*change/100)
        if duration > 0:
            time.sleep(duration)
            self.set_tank(prior_left, prior_right)

    def backwards(self, speed=1, duration=-1):
        self.set_tank(-speed, -speed)
        if duration > 0:
            time.sleep(duration)
            self.halt()

    def shutdown(self):
        self.camera._close_event.set()
        self.halt()


ROBOT = Robot()
