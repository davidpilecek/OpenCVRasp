import serial
import numpy as np
import time
import cv2 as cv


cap = cv.VideoCapture(0)



def nothing(x):
	pass

cv.namedWindow('controls')

cv.createTrackbar('x','controls',0,500,nothing)
cv.createTrackbar('y','controls',500,500,nothing)

def crop_img(img, width):

    height_1 = int(cv.getTrackbarPos('x', 'controls'))
    height_2 = int(cv.getTrackbarPos('y', 'controls'))


    vertices = [(0, height_1), (0, height_2),(width , height_2), (width, height_1)]
    vertices = np.array([vertices], np.int32)

    mask = np.zeros_like(img)
    match_mask_color = 255
        
    cv.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv.bitwise_and(img, mask)
    return masked_image



center_left = 175
center_right = 325

lower_black = 0
upper_black = 25

counter = 0

ang1 = 0
ang2 = 0

white_min=3

white_max=12

threshold_max = 130

threshold_min = 60

threshold = 50

T = threshold   

while True:
  
    _, frame = cap.read()
    
    if(type(frame) == type(None)):
        pass
    else:
        frame = cv.resize(frame, (500, 500))
        height, width = frame.shape[:2]

    kernel = np.ones((5,5), np.uint8)

    frameGR = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    erode = cv.erode(frameGR, kernel)

    rc, th = cv.threshold(erode, T, 255, cv.THRESH_BINARY)    


    mask_black = cv.inRange(th, lower_black, upper_black)
    

    contours_black, hierarchy_black = cv.findContours(crop_img(mask_black, width), cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)


    
    cv.line(frame, (center_left, 500), (center_left, 0), (0, 0, 255), 10)
    cv.line(frame, (center_right, 500), (center_right, 0), (0, 0, 255), 10)



    if len(contours_black)>0:

        contour = max(contours_black, key = cv.contourArea)

        cv.drawContours(frame, contour, -1, (0, 255, 0), 5)

        if len(contours_black)>0:
            M = cv.moments(contour)
            if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
        
        cv.circle(frame, (cX, cY), 10, (255, 0, 0), -1)

        if cX > int(width / 2):
            phi = 180 - np.degrees(np.arctan((height - cY) / (cX - int(width / 2))))
                     
        if cX < int(width / 2):
            phi = np.degrees(np.arctan((height - cY) / (int(width / 2) - cX )))
            

        if phi != None :
            cv.putText(frame, str(round(phi)), (center_right, height-50), cv.FONT_HERSHEY_PLAIN, 3, (255,255,255), 5)
        
        counter+=1
        
         
    else:
        cX, cY = 0, 0

    if counter % 2 == 1:
            ang1 = round(phi)
            print("ANG1 ", ang1)

    elif counter % 2==0:
            ang2 = round(phi)
            print("ANG2 ", ang2)

    diff = np.abs(ang1 - ang2)
        
    
    print("DIFF ", diff)

    cv.line(frame, (int(width / 2), height), (cX, cY), (255, 255, 0), 5)
        

    try:
        cv.imshow("window", frame)

    except Exception as e:
        print(str(e))
 
    if cv.waitKey(1) == ord('q'):
        break


cap.release()
cv.destroyAllWindows()
