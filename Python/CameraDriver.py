__version__ = '0.1.0'

import sys
import time
import os
import cv2
import scipy.misc
import atexit
import Config as cfg
import numpy as np
import subprocess as sp

from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image

class Camera(object):
    def __init__(self, resolution=cfg.IMAGE_RESOLUTION):
        self.cameraProcess = None
        self.resolution = resolution
        self.is_enabled = False

        # pic dump stuff
        self.frame_n = 0
        self.pic_type = ''


    @staticmethod
    def _display_image(img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)

    @staticmethod
    def _save_image(img, path):
        scipy.misc.toimage(img, cmin=0.0, cmax=...).save(os.path.join(cfg.saveimg_path, path))

    def start(self):
        # Video capture parameters
        (w,h) = self.resolution
        self.bytesPerFrame = w * h
        fps = 250 # setting to 250 will request the maximum framerate possible

        videoCmd = "raspividyuv -w "+str(w)+" -h "+str(h)+" --output - --timeout 0 --framerate "+str(fps)+" --luma --nopreview"
        videoCmd = videoCmd.split() # Popen requires that each parameter is a separate string

        self.cameraProcess = sp.Popen(videoCmd, stdout=sp.PIPE) # start the camera
        atexit.register(self.cameraProcess.terminate) # this closes the camera process in case the python scripts exits unexpectedly

        # discard first frame
        _ = self.cameraProcess.stdout.read(bytesPerFrame)
        self.is_enabled = True

    def stop(self):
        self.cameraProcess.terminate() # stop the camera
        cv2.destroyAllWindows()
        self.is_enabled = False

    def get_frame(self):
        self.cameraProcess.stdout.flush()
        frame = np.fromfile(self.cameraProcess.stdout, count=self.bytesPerFrame, dtype=np.uint8)

        if frame.size != bytesPerFrame:
            print("Error: Camera stream closed unexpectedly")
            break

        if cfg.DEBUG_MODE:
            self._save_image(frame)

        return frame

    def show_frame(self, frame):
        (w,h) = self.resolution
        frame.shape = (h,w) # set the correct dimensions for the numpy array
        cv2.imshow("skrrt", frame)

    """ Image recognition functions """

    def preprocess_image(self, img):
        # Greyscale and blur
        if cfg.DEBUG_MODE:
            debug_save_img(img, '{}_{}_raw.jpg'.format(self.pic_series, self.pic_type))

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)

        if cfg.DEBUG_MODE:
            debug_save_img(blur, '{}_{}_blur.jpg'.format(self.pic_series, self.pic_type))

        # Transform image perspective
        pts1 = np.float32([cfg.p0, cfg.p1, cfg.p2, cfg.p3])
        pts2 = np.float32([[0,0],[cfg.POST_TRANSFORM_RES[0],0],[0,cfg.POST_TRANSFORM_RES[1]],cfg.POST_TRANSFORM_RES])
        M = cv2.getPerspectiveTransform(pts1,pts2)
        blur_crop = cv2.warpPerspective(blur,M,(cfg.POST_TRANSFORM_RES[0],cfg.POST_TRANSFORM_RES[1]))
        if cfg.DEBUG_MODE:
            debug_save_img(blur_crop, '{}_{}_transform.jpg'.format(self.pic_series, self.pic_type))

        return blur_crop


if __name__=='__main__':
    c = Camera()
    c.start()
    try:
        while True:
            f = c.get_frame()
            c.show_frame(f)
    
    finally:
        c.stop()
