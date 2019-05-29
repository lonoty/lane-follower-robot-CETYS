import cv2
import numpy as np
import sys
import Tkinter as tk
from Tkinter import *
import Tkconstants, tkFileDialog
src = np.array([[262,189], [119, 431], [546, 430], [354, 183]], dtype="float32")
dst = np.array([[260, -0], [260, 465], [380, 465], [380, 0]], dtype="float32")
M = cv2.getPerspectiveTransform(src, dst)
image_hsv = None
pixel = (0,0,0) #RANDOM DEFAULT VALUE

ftypes = [

    ('PNG', '*.png;*.PNG'),
    ('GIF', '*.gif;*.GIF'),
    ('JPG', '*.jpg;*.JPG;*.JPEG'),
]

def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = warped[y,x]

        #HUE, SATURATION, AND VALUE (BRIGHTNESS) RANGES. TOLERANCE COULD BE ADJUSTED.

        upper =  np.array([pixel[0] + 10, pixel[1] + 80, pixel[2] + 50])
        lower =  np.array([pixel[0] - 5, pixel[1] - 80, pixel[2] - 50])
        print(pixel)
        print(lower, upper)

        #A MONOCHROME MASK FOR GETTING A BETTER VISION OVER THE COLORS
        image_mask = cv2.inRange(warped,lower,upper)
        cv2.imshow("Mask",image_mask)
        aaa= cv2.Canny(image_mask, 20,50)
        cv2.imshow("canny", aaa)

def main():

    global image_hsv, pixel, warped

    #OPEN DIALOG FOR READING THE IMAGE FILE
    root = tk.Tk()
    root.withdraw() #HIDE THE TKINTER GUI
    file_path = tkFileDialog.askopenfilename(filetypes = ftypes)
    image_src = cv2.imread(file_path)
    cv2.imshow("BGR",image_src)


    #CREATE THE HSV FROM THE BGR IMAGE
    image_hsv = cv2.cvtColor(image_src,cv2.COLOR_BGR2HSV)
    warped = cv2.warpPerspective(image_hsv, M, (640,480))
    cv2.imshow("HSV",warped)

    #CALLBACK FUNCTION
    cv2.setMouseCallback("HSV", pick_color)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
