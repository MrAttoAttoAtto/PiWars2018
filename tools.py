import time

from smbus import SMBus
from settings import address

"""
WIRING:
RPI's GND = PIN06 -----> ARDUINO NANO'S GND
RPI'S SDA = GPIO02 = PIN03 -----> ARDUINO NANO'S SDA = A4
RPI'S SCL = GPI03 = PIN05 -----> ARDUINO NANO'S SCL = A5
"""

def get_distance():
    global address
    '''
    Uses I2C to talk to an arduino nano, getting all distances from multiple
    ultrasonic sensors
    '''

    bus = SMBus(1)
    left = bus.read_byte(address)
    #TODO ADD MIDDLE ULTRASONIC TO ARDUINO AND WORKING RIGHT TO ARDUINO
    middle = 1
    right = bus.read_byte(address)
    return [left, middle, right]

    

def get_centroid(boolean_image, *args):

    im2, contours, hierarchy = cv2.findContours(boolean_image.copy(), *args)

    if contours:
        # If there are countours (i.e. a line) then find the largest one (the most likely to be your line)
        # Also draws lines on the image so it can be seen by humans (not NEEDED, but good for debugging purposes)

        max_contour = max(contours, key=cv2.contourArea)
        moment = cv2.moments(max_contour)

        center_x = int(moment['m10']/moment['m00'])
        center_y = int(moment['m01']/moment['m00'])

        return center_x, center_y
    
    else:
        return (False, False)