import serial
import numpy as np
import time
import cv2 as cv


arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
time.sleep(2)   

cap = cv.VideoCapture(0 + cv.CAP_DSHOW)  

center_left = 175
center_right = 325

lower_black = np.array([0, 0, 0])
upper_black = np.array([255, 255, 20])
counter = 0

ang1 = 0
ang2 = 0

#trackbar callback fucntion does nothing but required for trackbar
def nothing(x):
	pass


diff_allow = 30

#create a seperate window named 'settings' for trackbar
cv.namedWindow('settings')
cv.resizeWindow("settings", 640, 240)
#create trackbar in 'settings' window with name lower/upper_black'

cv.createTrackbar("lower_black", "settings", 0, 255, nothing)
cv.createTrackbar("upper_black", "settings", 255, 255, nothing)

lower_blacktest = int(cv.getTrackbarPos("lower_black","settings"))
upper_blacktest = int(cv.getTrackbarPos("upper_black","settings"))

while True:


    try:
        _, frame = cap.read()
        if(type(frame) == type(None)):
            pass
        else:
            frame = cv.resize(frame, (500, 500))

        height = frame.shape[0]
        width = frame.shape[1]

        frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        blur = cv.GaussianBlur(frameHSV, (7,7), 5)

        mask = cv.inRange(blur, lower_black, upper_black)

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
                     
        if cX < int(width / 2):
            phi = np.degrees(np.arctan((height - cY) / (int(width / 2) - cX )))
            
        counter+=1
        
# pokud je momentalni deg o 50 vetsi, nez predchozi, neposilej ho, pokud se ale vyskytne 2x za sebou v range +-10
# tak jej pust

        if counter % 2 == 1:
            ang1 = round(phi)
            print("ANG1 ", ang1)

        elif counter % 2==0:
            ang2 = round(phi)
            print("ANG2 ", ang2)

        diff = np.abs(ang1 - ang2)

        
        print("DIFF ", diff)

        if counter % 2 and diff<=50:
            arduino.write(bytes(str(ang1), 'utf-8'))
            print("ANG1WRITE")

        elif counter % 2 == 0 and diff<=50:
            arduino.write(bytes(str(ang2), 'utf-8'))
            print("ANG2WRITE")
        else:
            print("diff too large")

        time.sleep(0.05)

        arduino_data = arduino.readline()      
        print("arduino serial: ", arduino_data.decode('utf-8'))
        
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