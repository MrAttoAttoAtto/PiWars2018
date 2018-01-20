import time

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

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)