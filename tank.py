'''tank.py
The interface for the hardware parts of the robot.
Access motors, ultrasonics from here.
'''

import time

class Tank:
    def __init__(self, driver):
        try:
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)
            self.camera.framerate = 32
        except Exception:
            self.camera = None

        self.driver = driver

    def set_tank(self, speed_left, speed_right):
        driver.turn_motors(0, speed_left)
        driver.turn_motors(1, speed_right)
    
    def enable_flywheel(self):
        '''Enables the flywheels'''
        pass

    def disable_flywheel(self):
        '''Disables the flywheels'''
        pass

    def get_distance(self, ultra_no):
        '''Get the reported distance by a certain ultrasonic sensor.'''
        pass

    def take_picture(self):
        
    def forwards(self, speed = 1, time=-1):
        self.set_tank(speed, speed)
        if time > 0:
            time.sleep(time)
            self.halt()

    def halt(self):
        self.set_tank(0, 0)
    
    def left(self, speed = 1, time=-1):
        self.set_tank(-speed, speed)
        if time > 0:
            time.sleep(time)
            self.halt()

    def right(self, speed = 1, time=-1):
        self.set_tank(speed, -speed)
        if time > 0:
            time.sleep(time)
            self.halt()

    def backwards(self, speed = 1, time=-1):
        self.set_tank(-speed, -speed)
        if time > 0:
            time.sleep(time)
            self.halt()
    
        
        
TANK = Tank()
