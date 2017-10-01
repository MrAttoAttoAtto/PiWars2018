'''
Indeed this isnt even required, but it is a good template for some of the other ones...
'''

import time

import cv2

from picamera import PiCamera
from picamera.array import PiRGBArray

RESOLUTIONX = 160
RESOLUTIONY = 120

camera = PiCamera()

while True:
    # Gets the camera to take a picture, and makes it an array cv2 can work with

    rawCapture = PiRGBArray(camera)

    time.sleep(0.1) # gives time for the init and waiting a bit

    camera.capture(rawCapture, format="bgr") # captures the photo
    image = rawCapture.array() # turns it straight into a nice array

    grayscaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Clears the image of noise, makes it smaller (and cropped closer to the robot)
    # Also constructs the contours from the boolean image

    noisyImage = grayscaleImage[int(RESOLUTIONX/2):RESOLUTIONX, 0:RESOLUTIONX]

    clearImage = cv2.GaussianBlur(grayscaleImage, (5, 5), 0)

    ret, booleanImage = cv2.threshold(clearImage, 60, 255, cv2.THRESH_BINARY_INV)

    im2, contours, hierarchy = cv2.findContours(booleanImage.copy(), 1, cv2.CHAIN_APPROX_NONE)

    if contours:
        # If there are countours (i.e. a line) then find the largest one (the most likely to be your line)
        # Also draws lines on the image so it can be seen by humans (not NEEDED, but good for debugging purposes)

        maxContour = max(contours, key=cv2.contourArea)
        moment = cv2.moments(maxContour)

        momentX = int(moment['m10']/moment['m00'])
        momentY = int(moment['m01']/moment['m00'])

        cv2.line(noisyImage, (momentX, 0), (momentX, 720), (255, 0, 0), 1)
        cv2.line(noisyImage, (0, momentY), (1280, momentY), (255, 0, 0), 1)

        cv2.drawContours(noisyImage, contours, -1, (0, 255, 0), 1)

        # Decides which way to go (and does it (IN THE FUTURE)) by the angle at which the line is going
        # Also, the 3/4 and 1/4 are subject to change based on testing

        if momentX >= RESOLUTIONX * 3/4:
            pass # Go LEFT

        elif momentX < RESOLUTIONX * 3/4 and momentX > RESOLUTIONX * 1/4:
            pass # Go STRAIGHT

        elif momentX <= RESOLUTIONX * 1/4:
            pass # Go RIGHT

    else:
        pass # LINE NOT FOUND

    try:
        cv2.imshow('frame', noisyImage)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except NameError:
        pass
