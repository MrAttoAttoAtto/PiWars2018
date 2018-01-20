#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor


class Driver:
    def __init__(self, address=0x60):
        self.mh = Adafruit_MotorHAT(addr=address)

        self.motors = (
            (
                self.mh.getMotor(1),
                self.mh.getMotor(2)
            ),
            (
                self.mh.getMotor(3),
                self.mh.getMotor(4),
            )
        )

    #Some testeroos that probably will be removed later
    '''
    def smooth_left(self, left_speed):
        right_speed = max(0, (left_speed * 0.07) ** 2 - 10 * -1)
        self.turn_motors(0, left_speed)
        self.turn_motors(1, right_speed)

    def smooth_right(self, right_speed):
        left_speed = max(0, (right_speed * 0.07) ** 2 - 10 * -1)
        self.turn_motors(1, right_speed)
        self.turn_motors(0, left_speed)
    '''

    def turn_motors(self, side, speed):
        pos = lambda speed: 1 if speed >= 0 else 0
    
        self.run_motors(self.motors[side], pos(speed))
        self.set_motors(self.motors[side], abs(speed))

    def set_motors(self, motors, speed):
        for motor in motors:
            motor.setSpeed(abs(speed))

    def run_motors(self, motors, direction):
        if direction:
            for motor in motors:
                motor.run(Adafruit_MotorHAT.FORWARD)
        else:
            for motor in motors:
                motor.run(Adafruit_MotorHAT.BACKWARD)


    def safe_shutdown(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
