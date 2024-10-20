import os
from time import sleep
import cv2

class sessionRecog(object):
    # default constructor
    def __init__(self, personID = 1):
        
        self.video = cv2.VideoCapture(0)
        
    def __del__(self):

        self.video.release()
     
    def get_frames(self):
        ret, self.frames = self.video.read()
        resized_frame = cv2.resize(self.frames, (420, 420))
        ret, jpeg = cv2.imencode('.jpg', resized_frame)
        return jpeg.tobytes()
      