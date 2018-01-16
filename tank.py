'''tank.py
The interface for the hardware parts of the robot.
Access motors, ultrasonics from here.
'''

import time

class Tank:
    def __init__(self):
        self.camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32

    def set_tank(self, speed_left, speed_right):
        # Do speed things, get direction from neg/pos
        # Set motor pwms
        pass
    
    def enable_flywheel(self):
        '''Enables the flywheels'''
        pass

    def disable_flywheel(self):
        '''Disables the flywheels'''
        pass

    def get_distance(self, ultra_no):
        '''Get the reported distance by a certain ultrasonic sensor.'''
        pass

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
