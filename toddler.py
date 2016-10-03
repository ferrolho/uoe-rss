#!/usr/bin/env python
__TODDLER_VERSION__="1.0.0"

import time
import numpy
import cv2

# Main Toddler class
class Toddler:
    # Initialiser
    def __init__(self,IO):
        # Print a message
        print 'I am a toddler playing in a sandbox'
        # Store the instance of IO for later
        self.IO=IO
        # Add more initialisation code here

    # This is a callback that will be called repeatedly.
    # It has its dedicated thread so you can keep blocking it.
    def Control(self, OK):
        while OK():
            # Add control code here
            time.sleep(0.05)

    # This is a callback that will be called repeatedly.
    # It has its dedicated thread so you can keep blocking it.
    def Vision(self, OK):
        # Set the resolution to low
        self.IO.cameraSetResolution('low')

        while OK():
            # Grab the image
            self.IO.cameraGrab()

            # Read the image
            image = self.IO.cameraRead()

            # Display the image
            self.IO.imshow('My window', image)

            time.sleep(0.05)
