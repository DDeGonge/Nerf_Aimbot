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
    def __init__(self, resolution=cfg.video_resolution):
        self.cameraProcess = None
        self.resolution = resolution
        self.is_enabled = False

        self.locked_on = False
        self.tlast = 0

        # pic dump stuff
        self.frame_n = 0
        self.pic_type = ''

        # Setup stuff
        self.tracker = cv2.TrackerKCF_create()
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    @staticmethod
    def _display_image(img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)


    @staticmethod
    def _save_image(img, impath):
        im = Image.fromarray(img)
        im.save(os.path.join(cfg.saveimg_path, impath))


    def start(self):
        self.cap = cv2.VideoCapture(0)

        # Set resolution
        w, h = self.resolution
        self.cap.set(3,w)
        self.cap.set(4,h)
        # self.cap.set(cv2.CAP_PROP_EXPOSURE, 40)
        # self.cap.set(cv2.CAP_PROP_FPS, 40)

        if cfg.DEBUG_MODE:
            self.debug_vid = cv2.VideoWriter(os.path.join(cfg.saveimg_path, 'debug_vid.avi'),cv2.VideoWriter_fourcc(*'DIVX'), 30, (h, w))
            self.track_vid = cv2.VideoWriter(os.path.join(cfg.saveimg_path, 'track_vid.avi'),cv2.VideoWriter_fourcc(*'DIVX'), 30, (h, w))


    def stop(self):
        self.cap.release()
        self.debug_vid.release()
        self.track_vid.release()


    def get_frame(self):
        _, img = self.cap.read()
        img[:,:,2] = np.zeros([img.shape[0], img.shape[1]])  # Remove red channel so laser can stay on
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        r_gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)

        if cfg.DEBUG_MODE:
            self.debug_vid.write(r_gray)

        if cfg.SAVE_FRAMES:
            self.frame_n += 1
            self._save_image(r_gray, '{}.jpg'.format(self.frame_n))

        return r_gray


    def reset_lock_on(self):
        self.tracker.clear()
        self.tracker = cv2.TrackerKCF_create()
        self.locked_on = False


    def lock_on(self, target_bbox = None):
        (imgw, imgh) = cfg.laser_center
        (w,h) = cfg.lock_on_size_px
        h_lower = imgh - int(h/2)
        w_lower = imgw - int(w/2)

        if target_bbox is None:
            target_bbox = (w_lower, h_lower, w, h)

        frame = self.get_frame()
        self.target_img = frame[h_lower : h_lower + h, w_lower : w_lower + w]

        if cfg.DEBUG_MODE:
            self._save_image(self.target_img, 'lock_on_img.jpg')

        self.reset_lock_on()
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

            (a, b, c, d) = (int(j) for j in bbox)
            frame = cv2.rectangle(frame, (a, b), (a + c, b + d), (0, 255,0), 2)

            if cfg.DEBUG_MODE:
                print("[{}, {}] - {} fps".format(h, w, 1 / (tnow - self.tlast)))
                self.tlast = tnow
                self.track_vid.write(frame)

            if cfg.SAVE_FRAMES:
                self._save_image(frame, 'cv_{}.jpg'.format(self.frame_n))

            return (h, w)

        else:
            print('Tracking error')
            if cfg.DEBUG_MODE:
                self.track_vid.write(frame)
            if cfg.SAVE_FRAMES:
                self._save_image(frame, 'cv_{}.jpg'.format(self.frame_n))
            return (0,0)


    def find_face(self):
        frame = self.get_frame()
        faces = self.face_cascade.detectMultiScale(frame, 1.1, 4)

        tnow = time.time()
        if cfg.DEBUG_MODE:
            print("Face Detection - {} fps".format(1 / (tnow - self.tlast)))
            self.tlast = tnow

        if len(faces) > 0:
            [a, b, c, d] = faces[0]
            return (a, b, c, d)
        return None


    def show_frame(self, frame):
        (w,h) = self.resolution
        frame.shape = (h,w) # set the correct dimensions for the numpy array
        cv2.imshow("skrrt", frame)


if __name__=='__main__':
    c = Camera()
    c.start()
    try:
        print('Camera started')
        # while True:
        #     _ = c.get_frame()

        c.lock_on()
        print('Locked on')

        while True:
            h, w = c.get_location()
    
    finally:
        c.stop()
