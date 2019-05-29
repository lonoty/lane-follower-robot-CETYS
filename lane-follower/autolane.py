import cv2
import numpy as np
import sys
import Tkinter as tk
import matplotlib.pyplot as plt
from Tkinter import *
import Tkconstants, tkFileDialog
upper1 =  np.array([ 19, 250, 240])
lower1 =  np.array([  2,  74, 128])
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
def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i

    return num
def main():

    global image_hsv, pixel, warped
    list=[]
    #################3OPEN DIALOG FOR READING THE IMAGE FILE
    root = tk.Tk()
    root.withdraw() #HIDE THE TKINTER GUI
    file_path = tkFileDialog.askopenfilename(filetypes = ftypes)
    image_src = cv2.imread(file_path)

    ################# color transformation and filter -------> binary image
    image_hsv = cv2.cvtColor(image_src,cv2.COLOR_BGR2HSV)
    image_mask = cv2.inRange(image_hsv,lower1,upper1)

    ############################ warp tranform ------------> birds eye view
    warped = cv2.warpPerspective(image_mask, M, (640,480))
    warped1 = cv2.warpPerspective(image_src, M, (640,480))
    warped2 = cv2.warpPerspective(image_hsv, M, (640,480))
    ############ for line detection

    edges = cv2.Canny(warped, 30,50)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40, minLineLength= 55,maxLineGap=10,)
    for x in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[x]:
            cv2.line(warped1,(x1,y1),(x2,y2),(0,255,0),2)
            angle = np.arctan2(y1 - y2, x1 - x2) *(180/ np.pi)
            print(angle)
            if ((90< angle <100) or (-100< angle < -90)):
                #derecho
                list.append(0)
            elif(-100 > angle):
                #izquierda
                list.append(1)
            elif(angle > 100):
                #derecha
                list.append(2)

    action =most_frequent(list)

    #print (action)
    #############probabilities of what action it is //////straight: action =0 | left: action = 1 | right: action = 2



    ################################################## actions are based if there is a straight line or curves
    ################################################## straight: action =0 | left: action = 1 | right: action = 2

    if(action== 0):
        ################## peak histogram (where the lines start in the bottom)
        histogram = np.sum(warped[350:,:],axis =0)
        leftp= np.argmax(histogram[:320])
        rightp= np.argmax(histogram[320:])+320

        ### find bad values (true if there is a missing peak/line) and add a tolerance
        lbad = True if((leftp == 0) or (histogram[leftp] < 2000)) else False
        rbad = True if((rightp == 320) or (histogram[rightp] < 2000)) else False

        ################## ERROR from peaks leftbound=165   rightbound=440
        leftbound = 165
        rightbound = 440
        error=0
        count=0
        print(lbad,rbad)
        if(not lbad):
            error =error +(leftp-leftbound)
            count += 1
        if(not rbad):
            error = error+(rightp-rightbound)
            count += 1
        error= error/count
        print(error)
    elif(action == 1):
        print("left")

    elif(action == 2):
        print("right")




    ############### print parameters
    #----number of lines
    #print(len(lines))

    #----- peaks
    #print(leftp, rightp)
    #----- bad or good peaks
    #print(lbad,rbad)
    #----- line error (left = negative  right = positive)
    #print(error)
    ############## matplotlib show
    a = plt.subplot(2,1,1)
    plt.imshow(warped)
    plt.subplot(2,1,2, sharex= a)
    plt.plot(histogram)


    ###############opencv show
    #cv2.imshow("original",image_src)
    #cv2.imshow("edges",edges)
    #cv2.imshow("superior", warped1)
    #cv2.imshow("warpedmask", warped2)
    #cv2.imshow("HSV",warped)


    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
