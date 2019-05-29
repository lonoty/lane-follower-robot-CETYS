import cv2
import numpy as np
import sys
import Tkinter as tk
from Tkinter import *
import Tkconstants, tkFileDialog

image_hsv = None
pixel = (0,0,0) #RANDOM DEFAULT VALUE

ftypes = [

    ('PNG', '*.png;*.PNG'),
    ('GIF', '*.gif;*.GIF'),
    ('JPG', '*.jpg;*.JPG;*.JPEG'),
]

def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y,x]

        #HUE, SATURATION, AND VALUE (BRIGHTNESS) RANGES. TOLERANCE COULD BE ADJUSTED.

        upper1 =  np.array([ 19, 250, 240])
        lower1 =  np.array([  2,  74, 128])
        upper2 =  np.array([ 33, 212, 203])
        lower2 =  np.array([-27,  72, 163])
        upper3 = np.array([208, 140, 178])
        lower3 = np.array([148,  80, 138])
        upper4 = np.array([  9, 157, 155])
        lower4 = np.array([ -1,  97, 115])
        upper5 = np.array([ 14, 250, 145])
        lower5 = np.array([ -6, 190, 105])

        


        #A MONOCHROME MASK FOR GETTING A BETTER VISION OVER THE COLORS
        image_mask = cv2.inRange(image_hsv,lower1,upper1)

        edges = cv2.Canny(image_mask, 30,50)
        cv2.imshow("edges",edges)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
        print(len(lines))
        for x in range(0, len(lines)):

            for x1,y1,x2,y2 in lines[x]:
                cv2.line(image_hsv,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.imshow("aaa", image_hsv)
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
    cv2.imshow("HSV",image_hsv)

    #CALLBACK FUNCTION
    cv2.setMouseCallback("HSV", pick_color)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
