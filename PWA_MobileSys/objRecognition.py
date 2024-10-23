import os
from time import sleep
import cv2
from ultralytics import YOLO
import numpy as np

class sessionRecog():
    # global variables
    model = None
    
    # default constructor
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        print("HI")

    # object detection function
    def detect_obj(self, object):
        
        img = np.asarray(object)

        # identify only food, remotes or mobile devices
        self.model.predict(source=img, save=True, classes=[46,47,48,49,50,51,52,53,53,55,65,67])
        
        results = self.model(img)
        for i in results:
            boxes = i.boxes
            
            if len(boxes) != 0:
                print(i.boxes.cls)
                return True
            else:
                return False
        
      