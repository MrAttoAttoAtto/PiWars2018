
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
 
import time

class Drive:
    def __init__(self, address=0x60):
        self.mh = Adafruit_MotorHAT(addr=address)
        
        self.left_motors = (
            self.mh.getMotor(0),
            self.mh.getMotor(1)
        )
        self.right_motors = (
            self.mh.getMotor(2),
            self.mh.getMotor(3),
        )
    
    def turn_motors(self, side, direction):
        if side and direction < 0:
            self.run_motors(right_motors, 0)
            self.set_motors(right_motors, abs(speed))

        elif side and direction >= 0:
            self.run_motors(right_motors, 1)
            self.set_motors(right_motors, speed)

        elif not side and direction < 0:
            self.run_motors(left_motors, 0)
            self.set_motors(left_motors, abs(speed))

        elif not side and direction >= 0:
            self.run_motor(right_motors, 1):
            self.set_motors(right_motors, speed)
    
    def set_motors(self, motors, speed):
        for motor in motors:
            motor.setSpeed(speed)

    def run_motors(self, motors, direction):
        if direction:
            for motor in motors:
                motor.run(Adafruit_MotorHAT.FORWARD)
        else:
            for motor in motors:
                motor.run(Adafruit_DCMotor.BACKWARD)


    def safe_shutdown_motors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	    self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	    self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	    self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)