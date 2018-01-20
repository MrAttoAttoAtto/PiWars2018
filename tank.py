'''tank.py
The interface for the hardware parts of the robot.
Access motors, ultrasonics from here.
'''

import time
import drive

class Tank(drive.Driver):
    def __init__(self, driver):
        drive.Driver.__init__()
        try:
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)
            self.camera.framerate = 32
        except Exception:
            self.camera = None

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
        
    def forwards(self, speed = 255, time=-1):
        self.set_tank(speed, speed)
        if time > 0:
            time.sleep(time)
            self.halt()

    def halt(self):
        self.turn_motors(0, 0)
        self.turn_motors(1, 0)
    
    def left(self, speed = 255, time = 1):
        turn_motors(0, 255)
        turn_motors(1, )

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
