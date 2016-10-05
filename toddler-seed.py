#!/usr/bin/env python
__TODDLER_VERSION__ = "1.0.0"

import cv2
import time

from featureMatching import *
from resourceData import *
from sceneData import *
from settings import *


def InitResources(resources):
    for name in RESOURCE_NAMES:
        resources.append(ResourceData(name))


# Main Toddler class
class Toddler:
    # Initialiser
    def __init__(self,IO):
        # Print a message
        print 'I am a toddler playing in a sandbox'

        # Store the instance of IO for later
        self.IO = IO

        # Add more initialisation code here
        self.hallCounter = 0

        self.visibleResources = [0, 0, 0, 0]

        self.resourcesData = []
        InitResources(self.resourcesData)


    def ResourceIsVisible(self):
        for visible in self.visibleResources:
            if (visible):
                return True


    # This is a callback that will be called repeatedly.
    # It has its dedicated thread so you can keep blocking it.
    def Control(self, OK):
        while OK():
            if hasattr(self, 'inputs'):
                self.lastInputs = self.inputs
                self.inputs = list(self.IO.getInputs())
            else:
                self.inputs = list(self.IO.getInputs())
                self.lastInputs = self.inputs

            self.sensors = self.IO.getSensors()
            print self.sensors

            #print
            #print self.lastInputs
            #print self.inputs

            if self.lastInputs[7] != self.inputs[7]:
                self.hallCounter += 1
            #print 'Travelled distance: %d' % self.hallCounter

            if self.ObstacleToTheRight():
                self.TurnLeft()
            elif self.ObstacleToTheLeft():
                self.TurnRight()
            else:
                self.MoveForward()


    def ObstacleToTheRight(self):
        return self.sensors[0] > 300
    def ObstacleToTheLeft(self):
        return self.sensors[1] > 300


    def STOP(self):
        self.IO.setMotors(0, 0)

    def MoveBackwards(self):
        self.IO.setMotors(100, -100)
    def MoveForward(self):
        self.IO.setMotors(-100, 100)

    def TurnLeft(self):
        self.IO.setMotors(100, 100)
    def TurnRight(self):
        self.IO.setMotors(-100, -100)


    # This is a callback that will be called repeatedly.
    # It has its dedicated thread so you can keep blocking it.
    def Vision(self, OK):
        if (USE_VISION):
            # Set the camera resolution
            self.IO.cameraSetResolution('low')

            while OK():
                # Grab the image
                self.IO.cameraGrab()

                # Read the image
                cameraImage = cv2.cvtColor(self.IO.cameraRead(), cv2.COLOR_BGR2GRAY)

                # Create SceneData instance
                sceneData = SceneData(cameraImage)

                # look for resources in the scene
                self.visibleResources = [0, 0, 0, 0]
                for resourceData in self.resourcesData:
                    FeatureMatching(self, resourceData, sceneData)

                print self.visibleResources

                # Dump next couple of frames...
                for i in range(0, 10):
                    self.IO.cameraGrab()
#

### eof ###
