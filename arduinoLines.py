#pridat trackbars na nastaveni threshold barev 
#pro line, eventualne jine objekty
#
#


import serial
import numpy as np
import time
import cv2 as cv


arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
time.sleep(2)   

cap = cv.VideoCapture(0 + cv.CAP_DSHOW)  

center_left = 175
center_right = 325

lowerBlack = np.array([0, 0, 0])
upperBlack = np.array([255, 255, 20])

while True:

    try:
        _, frame = cap.read()
        frame = cv.resize(frame, (500, 500))
        height = frame.shape[0]
        width = frame.shape[1]

        frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        blur = cv.GaussianBlur(frameHSV, (7,7), 5)

        mask = cv.inRange(blur, lowerBlack, upperBlack)

    except Exception as e:
        print(str(e))

    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)
    
    cv.line(frame, (center_left, 500), (center_left, 0), (0, 0, 255), 10)
    cv.line(frame, (center_right, 500), (center_right, 0), (0, 0, 255), 10)


    if len(contours)>0:
        contour = max(contours, key = cv.contourArea)
        cv.drawContours(frame, contour, -1, (0, 255, 0), 5 )
        if len(contours)>0:
            M = cv.moments(contour)
            if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
        
        cv.circle(frame, (cX, cY), 10, (255, 0, 0), -1)

        if cX > int(width / 2):
            phi = 180 - np.degrees(np.arctan((height - cY) / (cX - int(width / 2))))
                     
        #correct
        if cX < int(width / 2):
            phi = np.degrees(np.arctan((height - cY) / (int(width / 2) - cX )))
            
        print(phi)
        
        ang = round(phi)
        deg = str(ang)
        arduino.write(bytes(deg, 'utf-8'))


        time.sleep(0.05)
        arduino_data = arduino.readline()      
        print("arduino serial: ", arduino_data.decode('utf-8'))
        print("cX: ", cX)
        print("cY: ", cY)

        cv.line(frame, (int(width / 2), height), (cX, cY), (255, 255, 0), 5)


         
    else:
        cX, cY = 0, 0
        
    try:
        hori = np.concatenate((frame, frameHSV), axis=1)
        cv.imshow("window", hori)
    except Exception as e:
        print(str(e))
 
    if cv.waitKey(100) == ord('q'):
        break


cap.release()
cv.destroyAllWindows()

arduino.close()