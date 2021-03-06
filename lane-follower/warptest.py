import cv2
import numpy as np
import sys
import Tkinter as tk
from Tkinter import *
import Tkconstants, tkFileDialog
src = np.array([[27, 425], [600, 428], [525, 5], [126, 6]], dtype="float32")
dst = np.array([[100, 480], [540, 480], [540, 0], [100, 0]], dtype="float32")
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

        print(x,y)

def main():
    global image_src


    #OPEN DIALOG FOR READING THE IMAGE FILE
    root = tk.Tk()
    root.withdraw() #HIDE THE TKINTER GUI
    file_path = tkFileDialog.askopenfilename(filetypes = ftypes)
    image_src = cv2.imread(file_path)
    cv2.imshow("BGR",image_src)
    warped = cv2.warpPerspective(image_src, M, (640,480))
    cv2.imshow("warped",warped)
    cv2.setMouseCallback("BGR", pick_color)

    #CREATE THE HSV FROM THE BGR IMAGE

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
