# imports 
import os
from time import sleep
import cv2
from ultralytics import YOLO
import numpy as np
from flask import jsonify

class sessionRecog():
    # global variables
    model = None
    detected = None
    # default constructor
    def __init__(self):
        self.model = YOLO('yolov8n.pt')

    # object detection function
    def detect_obj(self, object):
        
        img = np.asarray(object)

        # identify only food, remotes or mobile devices
        self.model.predict(source=img, classes=[45, 46,47,48,49,50,51,52,53,53,55,65,67])
        
        results = self.model(img)
        for i in results:
            boxes = i.boxes

            if len(boxes) != 0:
                box = i.boxes[0]
                item_id = int(box.cls)
                item_name = self.model.names[item_id]
                self.detected = {'value': True, 'item': item_name}
                
            else:
                self.detected = {'value': False, 'item': None}
        
    def getDetected(self):
        return self.detected
      