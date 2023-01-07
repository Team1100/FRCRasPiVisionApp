#!/usr/bin/env python3
from cscore import CameraServer
from networktables import NetworkTablesInstance
from apriltag import apriltag

import time
import cv2
import json
import numpy as np
import math
import threading

class CameraView(object):
    def __init__(self, camera, vertFOV, horizFOV, elevationOfTarget, elevationOfCamera, angleFromHoriz):
        self.camera = camera
        self.width = self.camera['width']
        self.height = self.camera['height']
        self.vertFOV = vertFOV
        self.horizFOV = horizFOV
        self.elevationOfTarget = elevationOfTarget
        self.elevationOfCamera = elevationOfCamera
        self.angleFromHoriz = angleFromHoriz


class Target(object):
    def __init__(self, camera, coor, id):
        self.id = id
        self.normalizedY = (coor[1] - camera.height/2)/(camera.height/2) * -1
        self.normalizedX = (coor[0] - camera.width/2)/(camera.width/2)
        self.pitch = (self.normalizedY/2) * camera.vertFOV
        self.yaw = (self.normalizedX/2) * camera.horizFOV
        #(height of target (meters) - height of camera(meters))/tan(pitch + angle of camera)
        self.distanceToTarget = (camera.elevationOfTarget - camera.elevationOfCamera) / math.tan(math.radians(self.pitch + camera.angleFromHoriz))



class VisionApplication(object):
    def __init__(self):
        self.TITLE = "apriltag_view"
        self.TAG = "tag36h11"
        self.MIN_MARGIN = 10
        self.FONT = cv2.FONT_HERSHEY_SIMPLEX
        self.RED = 0,0,255
        self.detector = apriltag(self.TAG)

        self.imgResult = None
        self.team = None

        self.targetDetected = False

        self.distanceFromTarget = 0
        self.vision_nt = None 

        self.usingComputerIP = True 

        # Initialize configuration
        self.config = self.readConfig()
        self.team = self.config["team"]
        #TODO: Fill out values below
        #vertFOV = 
        #horizFOV = 
        #elevationOfTarget = 
        #elevationOfCamera = 
        #angleFromHoriz = 
        self.camera = CameraView(self.config['cameras'][0], 48.94175846, 134.3449419, 1.8288, 0.9779, 20.93552078)

        # Initialize Camera Server
        self.initializeCameraServer()

        # Initialize NetworkTables Client
        self.initializeNetworkTables()

    def readConfig(self):
        config = None
        with open('/boot/frc.json') as fp:
            config = json.load(fp)
        return config

    def initializeCameraServer(self):
        cserver = CameraServer.getInstance()
        cserver.startAutomaticCapture()

        self.cvsrc = cserver.putVideo("visionCam", self.camera.width,self.camera.height)
        
        self.sink = CameraServer.getInstance().getVideo()



    def initializeNetworkTables(self):
        # Table for vision output information
        ntinst = NetworkTablesInstance.getDefault()
        
        cond = threading.Condition()
        notified = [False]

        def connectionListener(connected, info):
            print(info, '; Connected=%s' % connected)
            with cond:
                notified[0] = True
                cond.notify()

        # Decide whether to start using team number or IP address
        if self.usingComputerIP:
            ip = '192.168.102.168' #ip of the computer
            print("Setting up NetworkTables client for team {} at {}".format(self.team,ip))
            ntinst.startClient(ip)
        else:
            ntinst.startClientTeam(self.team)

        ntinst.addConnectionListener(connectionListener, immediateNotify=True)

        with cond:
            print("Waiting")
            if not notified[0]:
                cond.wait()

        print("Connected!")
        
        self.vision_nt = ntinst.getTable('Shuffleboard/Vision')

    def runApplication(self):
        while True:
            camCenter = (self.camera.width)/2
            input_img1 = None
            frame_time1, input_img1 = self.sink.grabFrame(input_img1)
            
            
            # Notify output of error and skip iteration
            if frame_time1 == 0:
                self.cvsrc.notifyError(self.sink.getError())
                print("Error on line 126 with grabbing frame")
                continue


            greys = cv2.cvtColor(input_img1, cv2.COLOR_BGR2GRAY)
            dets = self.detector.detect(greys)

            # array of Target classes
            targets = []

            for det in dets:
                if det["margin"] >= self.MIN_MARGIN:
                    rect = det["lb-rb-rt-lt"].astype(int).reshape((-1,1,2))
                    cv2.polylines(input_img1, [rect], True, self.RED, 2)
                    ident = str(det["id"])
                    pos = det["center"].astype(int) + (-10,10)
                    targets.append(Target(self.camera,pos,det["id"]))
                    cv2.putText(input_img1, ident, tuple(pos), self.FONT, 1, self.RED, 2)
            
            if not targets: 
                # If no apriltags are detected, targetDetected is set to false
                self.vision_nt.putNumber('targetDetected',0)
            else: 
                # If AprilTags are detected, targetDetected is set to true 
                self.vision_nt.putNumber('targetDetected',1)
                #prints to the output on the web dashboard
                print(self.camera.width)
                self.vision_nt.putNumber('targetX',targets[0].normalizedX)
                self.vision_nt.putNumber('targetY',targets[0].normalizedY)
                self.vision_nt.putNumber('distanceToTarget',targets[0].distanceToTarget)
            
            self.cvsrc.putFrame(input_img1) 

def main():
    visionApp = VisionApplication()
    visionApp.runApplication()

main()   
