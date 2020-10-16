import cv2
import os
import sys
import glob

video_name = 'video.avi'
img_extension = ".jpg"
name_strip = "cv_"

def convert(filepath):
    images = [img for img in os.listdir(filepath) if img.endswith(img_extension) and img.startswith(name_strip)]
    clean_names = [int(i.replace(name_strip, "").replace(img_extension, "")) for i in images]
    clean_names.sort()

    frame = cv2.imread(os.path.join(filepath, images[0]))
    height, width, layers = frame.shape

    codec = cv2.VideoWriter_fourcc(*'DIVX')
    video = cv2.VideoWriter(os.path.join(filepath, video_name), codec, 30, (width,height))

    for image in clean_names:
        filename = name_strip + str(image) + img_extension
        video.write(cv2.imread(os.path.join(filepath, filename)))

    cv2.destroyAllWindows()
    video.release()

if __name__=="__main__":
    convert(sys.argv[1])
