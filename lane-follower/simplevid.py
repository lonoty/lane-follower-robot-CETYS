import cv2
import numpy as np
import sys

video = cv2.VideoCapture(0)
while True:
    check, image_src = video.read()
    if check == True:
        cv2.imshow("aaa", image_src)
        cv2.waitKey(1)
