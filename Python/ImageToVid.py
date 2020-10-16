import cv2
import os
import sys
import glob

video_name = 'video.avi'
img_extension = ".JPG"

def convert(filepath):
    images = [img for img in os.listdir(filepath) if img.endswith(img_extension)]
    frame = cv2.imread(os.path.join(filepath, images[0]))
    height, width, layers = frame.shape

    codec = cv2.VideoWriter_fourcc(*'DIVX')
    video = cv2.VideoWriter(os.path.join(filepath, video_name), codec, 30, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(filepath, image)))

    cv2.destroyAllWindows()
    video.release()

if __name__=="__main__":
    convert(sys.argv[1])
