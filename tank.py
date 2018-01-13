'''tank.py
The interface for the hardware parts of the robot.
Access motors, ultrasonics from here.
'''

class Tank:
    def __init__(self):
        pass
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

