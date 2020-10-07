__version__ = '0.1.0'

import sys
import time
import os
import cv2
from PIL import Image
import atexit
import Config as cfg
import numpy as np
import subprocess as sp


class Camera(object):
    def __init__(self, resolution=cfg.IMAGE_RESOLUTION):
        self.cameraProcess = None
        self.resolution = resolution
        self.is_enabled = False

        self.locked_on = False
        self.tlast = 0

        # pic dump stuff
        self.frame_n = 0
        self.pic_type = ''


        self.reset_lock_on()


    @staticmethod
    def _display_image(img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)


    @staticmethod
    def _save_image(img, impath):
        im = Image.fromarray(img)
        im.save(os.path.join(cfg.saveimg_path, impath))


    def start(self):
        # Video capture parameters
        (w,h) = self.resolution
        self.bytesPerFrame = w * h
        fps = 250 # setting to 250 will request the maximum framerate possible

        videoCmd = "raspividyuv -w "+str(w)+" -h "+str(h)+" --output - --timeout 0 --framerate "+str(fps)+" --luma --nopreview"
        videoCmd = videoCmd.split() # Popen requires that each parameter is a separate string

        self.cameraProcess = sp.Popen(videoCmd, stdout=sp.PIPE, bufsize=0) # start the camera
        # atexit.register(self.cameraProcess.terminate) # this closes the camera process in case the python scripts exits unexpectedly

        # discard first frame
        _ = self.cameraProcess.stdout.read(self.bytesPerFrame)
        self.is_enabled = True


    def stop(self):
        self.cameraProcess.terminate() # stop the camera
        cv2.destroyAllWindows()
        self.is_enabled = False


    def cv2_start(self):
        self.cap = cv2.VideoCapture(0)

    def cv2_stop(self):
        self.cap.release()

    def get_frame(self):
        _, img = self.cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if cfg.SAVE_ALL_FRAMES:
            self._save_image(gray, "{}.png".format(self.frame_n))
            self.frame_n += 1

        return gray

    def reset_lock_on(self):
        self.tracker = cv2.TrackerMOSSE_create()
        self.locked_on = False


    def lock_on(self):
        (imgw, imgh) = cfg.IMAGE_RESOLUTION
        (w,h) = cfg.lock_on_size_px
        h_lower = int(imgh/2) - int(h/2)
        w_lower = int(imgw/2) - int(w/2)

        target_bbox = (w_lower, h_lower, w, h)

        frame = self.get_frame()
        self.target_img = frame[h_lower : h_lower + h, w_lower : w_lower + w]

        if cfg.DEBUG_MODE:
            self._save_image(self.target_img, 'lock_on_img.png')

        self.tracker.init(frame, target_bbox)
        self.locked_on = True


    def get_location(self):
        """ returns (h, w) """
        if not self.locked_on:
            raise Exception('Cant track an object if not locked on...duh.')

        frame = self.get_frame()
        ok, bbox = self.tracker.update(frame)

        tnow = time.time()

        if ok:
            h = bbox[1] + int(bbox[3] / 2)
            w = bbox[0] + int(bbox[2] / 2)

            if cfg.DEBUG_MODE:
                print("[{}, {}] - {} fps".format(h, w, 1 / (tnow - self.tlast)))
                self.tlast = tnow
            return (h, w)

        else:
            print('Tracking error')
            return (0,0)


    # def get_frame(self):
    #     self.cameraProcess.stdout.flush()
    #     frame = np.fromfile(self.cameraProcess.stdout, count=self.bytesPerFrame, dtype=np.uint8)

    #     if frame.size != bytesPerFrame:
    #         print("Error: Camera stream closed unexpectedly")
    #         return

    #     if cfg.SAVE_ALL_FRAMES:
    #         self._save_image(frame, "{}.jpg".format(self.frame_n))
    #         self.frame_n += 1

    #     return frame

    def show_frame(self, frame):
        (w,h) = self.resolution
        frame.shape = (h,w) # set the correct dimensions for the numpy array
        cv2.imshow("skrrt", frame)


if __name__=='__main__':
    c = Camera()
    c.cv2_start()
    try:
        print('Camera started')
        # while True:
        #     _ = c.get_frame()

        c.lock_on()
        print('Locked on')

        while True:
            h, w = c.get_location()
    
    finally:
        c.cv2_stop()
