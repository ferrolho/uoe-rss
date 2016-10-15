#!/usr/bin/env python
__TODDLER_VERSION__ = "1.0.0"

import cv2
import numpy as np
import time

from featureMatching import *
from random import randint
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
        self.IO.servoEngage()
        self.ResetServo()

        # Add more initialisation code here
        self.hallCounter = 0

        self.visibleResources = [0, 0, 0, 0]

        self.resourcesData = []
        InitResources(self.resourcesData)


    def ResourceIsVisible(self):
        for visible in self.visibleResources:
            if visible:
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
            #print self.sensors

            #print
            #print self.lastInputs
            #print self.inputs

            if self.lastInputs[7] != self.inputs[7]:
                self.hallCounter += 1
            #print 'Travelled distance: %d' % self.hallCounter

            if self.RightWhisker():
                self.EvadeRight()
            elif self.LeftWhisker():
                self.EvadeLeft()
            else:
                if self.ObstacleToTheRight():
                    self.TurnLeft()
                elif self.ObstacleToTheLeft():
                    self.TurnRight()
                else:
                    self.MoveForward()

    # Temporary code for MM1
    def ResetServo(self):
        self.SetServoPosition(2)
    def SetServoPosition(self, position):
        self.IO.servoSet(position * 180 / 5 + 10)
        #self.IO.servoDisengage()

    def RightWhisker(self):
        return self.inputs[0]
    def LeftWhisker(self):
        return self.inputs[1]

    def ObstacleToTheRight(self):
        return self.sensors[0] > IR_THRESHOLD
    def ObstacleToTheLeft(self):
        return self.sensors[1] > IR_THRESHOLD


    def STOP(self):
        self.IO.setMotors(0, 0)

    def MoveBackwards(self):
        self.IO.setMotors(-70, -70)
    def MoveForward(self):
        self.IO.setMotors(70, 70)

    def EvadeLeft(self):
        self.IO.setMotors(-70, 0)
    def EvadeRight(self):
        self.IO.setMotors(0, -70)

    def TurnLeft(self):
        self.IO.setMotors(70, -70)
    def TurnRight(self):
        self.IO.setMotors(-70, 70)


    def ScanForCubeFarAway(self, rawCameraImage):
        hsv = cv2.cvtColor(rawCameraImage, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_bound = np.array([100, 40, 0])
        upper_bound = np.array([130, 255, 255])

        # threshold the HSV image to get only blue colors
        img = cv2.inRange(hsv, lower_bound, upper_bound)

        kernel = np.ones((5, 5), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

        ret, thresh = cv2.threshold(img, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            cnt = contours[0]
            M = cv2.moments(cnt)

            # centroid coords
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            cv2.line(rawCameraImage, (cx, cy), (cx, cy), (0, 0, 255), 20)
            print cx, cy

        self.IO.imshow('raw', rawCameraImage)


    def ScanForImages(self):
        cameraImage = cv2.resize(rawCameraImage, None, fx = 0.6, fy = 0.6, interpolation = cv2.INTER_CUBIC)
        cameraImage = cv2.cvtColor(cameraImage, cv2.COLOR_BGR2GRAY)

        # Create SceneData instance
        sceneData = SceneData(cameraImage)

        # look for resources in the scene
        self.visibleResources = [0, 0, 0, 0]
        for resourceData in self.resourcesData:
            FeatureMatching(self, resourceData, sceneData)

        if self.ResourceIsVisible():
            for i in range(4):
                if self.visibleResources[i]:
                    if i > 1:
                        i += 1
                    self.SetServoPosition(i)
        else:
            self.ResetServo()


    # This is a callback that will be called repeatedly.
    # It has its dedicated thread so you can keep blocking it.
    def Vision(self, OK):
        if (USE_VISION):
            # Set the camera resolution
            self.IO.cameraSetResolution('medium')

            while OK():
                # Grab the image
                self.IO.cameraGrab()

                # Read the image
                rawCameraImage = self.IO.cameraRead()

                self.ScanForCubeFarAway(rawCameraImage)

                # Dump next couple of frames...
                for i in range(0, 10):
                    self.IO.cameraGrab()
#

### eof ###
