
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
    
    
        


    def safe_shutdown(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	    self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	    self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	    self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)