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


def main():

    global image_hsv, pixel, warped,image_src

    #OPEN DIALOG FOR READING THE IMAGE FILE
    root = tk.Tk()
    root.withdraw() #HIDE THE TKINTER GUI
    file_path = tkFileDialog.askopenfilename(filetypes = ftypes)
    image_src = cv2.imread(file_path)
    cv2.imshow("BGR",image_src)

    #CREATE THE HSV FROM THE BGR IMAGE
    image_hsv = cv2.cvtColor(image_src,cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV",image_hsv)
    upper1 =  np.array([ 10, 298, 192])
    lower1 =  np.array([-10, 87,  12])
    upper2 =  np.array([185, 271, 202])
    lower2 =  np.array([165, 141,  22])






    #A MONOCHROME MASK FOR GETTING A BETTER VISION OVER THE COLORS
    image_mask = cv2.inRange(image_hsv,lower1,upper1) + cv2.inRange(image_hsv,lower2,upper2)
    #image_mask = cv2.GaussianBlur(image_mask, (9, 9), 0)
    cv2.imshow("yay",image_mask)


    edges = cv2.Canny(image_mask, 30,50)
    cv2.imshow("edges",edges)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40, minLineLength= 55,maxLineGap=10,)
    for x in range(0, len(lines)):

        for x1,y1,x2,y2 in lines[x]:
            cv2.line(image_src,(x1,y1),(x2,y2),(0,255,0),2)
    cv2.imshow("aaa", image_src)
    #CALLBACK FUNCTION
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
