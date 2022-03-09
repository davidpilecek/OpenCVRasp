from ctypes import sizeof
import numpy as np
import time
import cv2 as cv

#video capture variable
cap = cv.VideoCapture(0)   

#create variable for indexing corners
count = 0

def empty():
   return

cv.namedWindow("ParametersCanny")
cv.resizeWindow("ParametersCanny", 640, 240)
cv.createTrackbar("Threshold1", "ParametersCanny", 150, 255, empty)
cv.createTrackbar("Threshold2", "ParametersCanny", 255, 255, empty)

#ONLY TAKES ODD NUMBERS
cv.namedWindow("ParametersGauss")
cv.resizeWindow("ParametersGauss", 640, 240)
cv.createTrackbar("Threshold1", "ParametersGauss", 150, 255, empty)
cv.createTrackbar("Threshold2", "ParametersGauss", 255, 255, empty)


while True:
   #ret is a boolean value, tells us whether camera is available
   #frame is the frame
    ret, frame = cap.read()
   
    #load source dimensions
    height = frame.shape[0]
    width = frame.shape[1]
    
    #calculate where the center of the source lies
    vertical_center = width / 2
    horizontal_center = height / 2

    #convert source to grayscale image for efficiency
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
 
    #detect corners (source image, max num of corners, 
    #minimal confidence, min distance between each corner)
    corners = cv.goodFeaturesToTrack(gray, 1, 0.9, 50)

    cv.line(frame, (int(width/8*3), 0), (int(width/8*3),int(height) ), (0,255, 0), 5)
    cv.line(frame, (int(width/8*5), 0), (int(width/8*5),int(height) ), (0,255, 0), 5)
    
    imgBlur = cv.GaussianBlur(frame, (9, 9), 5)
    imgGray = cv.cvtColor(imgBlur, cv.COLOR_BGR2GRAY)

    threshold1 = cv.getTrackbarPos("Threshold1", "ParametersCanny")
    threshold2 = cv.getTrackbarPos("Threshold2", "ParametersGauss")

    imgCanny = cv.Canny(imgGray, threshold1, threshold2)

    cv.imshow("image", frame)
    cv.imshow("imageblur", imgBlur)
    cv.imshow("imageGray", imgGray)
    cv.imshow("imageCanny", imgCanny)

    if cv.waitKey(1) == ord('q'):
     break

         

cap.release()
cv.destroyAllWindows()