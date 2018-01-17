import drive
import time

Stukov = drive.Driver()

while (True):
    print("Forward! ")

    print("\tSpeed up...")
    for i in range(255):
        Stukov.turn_motors(1, i)
        Stukov.turn_motors(2, i)
        time.sleep(0.01)

    print( "\tSlow down...")
    for i in reversed(range(255)):
        Stukov.turn_motors(1, i)
        Stukov.turn_motors(2, i)
        time.sleep(0.01)

    print ("Backward! ")

    print( "\tSpeed up...")
    for i in range(255):
        Stukov.turn_motors(1, i)
        Stukov.turn_motors(2, i)
        time.sleep(0.01)
        
    print ("\tSlow down...")
    for i in reversed(range(255)):
        Stukov.turn_motors(1, i)
        Stukov.turn_motors(2, i)
        time.sleep(0.01)
        print ("Release")
        myMotor.run(Adafruit_MotorHAT.RELEASE)
    time.sleep(1.0)
