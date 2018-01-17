#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor


class Driver:
    def __init__(self, address=0x60):
        self.mh = Adafruit_MotorHAT(addr=address)
        
        self.left_motors = (
            self.mh.getMotor(1),
            self.mh.getMotor(2)
        )
        self.right_motors = (
            self.mh.getMotor(3),
            self.mh.getMotor(4),
        )
    
    def turn_motors(self, side, speed):
        if side and speed < 0:
            self.run_motors(self.right_motors, 0)
            self.set_motors(self.right_motors, abs(speed))

        elif side and speed >= 0:
            self.run_motors(self.right_motors, 1)
            self.set_motors(self.right_motors, speed)

        elif not side and speed < 0:
            self.run_motors(self.left_motors, 0)
            self.set_motors(self.left_motors, abs(speed))

        elif not side and speed >= 0:
            self.run_motors(self.left_motors, 1)
            self.set_motors(self.left_motors, speed)
    
    def set_motors(self, motors, speed):
        for motor in motors:
            motor.setSpeed(speed)

    def run_motors(self, motors, direction):
        if direction:
            for motor in motors:
                motor.run(Adafruit_MotorHAT.FORWARD)
        else:
            for motor in motors:
                motor.run(Adafruit_MotorHAT.BACKWARD)


    def safe_shutdown_motors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
