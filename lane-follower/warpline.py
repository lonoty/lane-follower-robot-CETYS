import cv2
import numpy as np
import sys
import Tkinter as tk
from Tkinter import *
import Tkconstants, tkFileDialog
src = np.array([[2, 386], [626, 386], [422, 159], [190, 159]], dtype="float32")
dst = np.array([[100, 480], [540, 480], [540, 0], [100, 0]], dtype="float32")
M = cv2.getPerspectiveTransform(src, dst)

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
    warped1 = cv2.warpPerspective(image_src, M, (640,480))
    #CREATE THE HSV FROM THE BGR IMAGE
    image_hsv = cv2.cvtColor(image_src,cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV",image_hsv)
    upper1 =  np.array([181, 262, 231])
    lower1 =  np.array([165,  62,  35])





    #A MONOCHROME MASK FOR GETTING A BETTER VISION OVER THE COLORS
    image_mask = cv2.inRange(image_hsv,lower1,upper1)
    #image_mask = cv2.GaussianBlur(image_mask, (9, 9), 0)
    cv2.imshow("yay",image_mask)

    warped = cv2.warpPerspective(image_mask, M, (640,480))
    cv2.imshow("warped",warped)
    edges = cv2.Canny(warped, 30,50)
    cv2.imshow("edges",edges)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40, minLineLength= 55,maxLineGap=10,)

    for x in range(0, len(lines)):

        for x1,y1,x2,y2 in lines[x]:
            cv2.line(warped1,(x1,y1),(x2,y2),(0,255,0),2)
    cv2.imshow("aaa", warped1)
    #CALLBACK FUNCTION
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
