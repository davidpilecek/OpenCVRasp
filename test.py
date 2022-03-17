import serial
import numpy as np
import time
import cv2 as cv


arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
time.sleep(2)   

cap = cv.VideoCapture(r"C:\Users\David\Documents\git\OpenCVNew\video.mp4")

center_left = 175
center_right = 325

lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 100])

lower_other = np.array([94, 80, 50])
upper_other = np.array([130, 255, 255])


counter = 0

ang1 = 0
ang2 = 0

diff_allow = 50

while True:
  
    _, frame = cap.read()
    
    if(type(frame) == type(None)):
        pass
    else:
        frame = cv.resize(frame, (500, 500))
        height = frame.shape[0]
        width = frame.shape[1]


    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    blur = cv.GaussianBlur(frameHSV, (3,3), 5)

    mask_black = cv.inRange(blur, lower_black, upper_black)
    
    mask_other = cv.inRange(blur, lower_other, upper_other)
    

    contours_black, hierarchy_black = cv.findContours(mask_black, cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)

    contours_other, hierarchy_other = cv.findContours(mask_other, cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)


    
    cv.line(frame, (center_left, 500), (center_left, 0), (0, 0, 255), 10)
    cv.line(frame, (center_right, 500), (center_right, 0), (0, 0, 255), 10)




    if len(contours_other) != 0:

        contour = max(contours_other, key = cv.contourArea)
        cv.drawContours(frame, contour, -1, (255, 0, 0), 3)


    if len(contours_black)>0:

        contour = max(contours_black, key = cv.contourArea)

        cv.drawContours(frame, contour, -1, (0, 255, 0), 5 )

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
            

        if phi != 0 :
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

    if counter % 2 and diff<=diff_allow:
            arduino.write(b"<")
            arduino.write(bytes(str(ang1), 'utf-8'))
            arduino.write(b"*")
            arduino.write(bytes(str(ang1+1), 'utf-8'))
            arduino.write(b">")
            

    elif counter % 2 == 0 and diff<=diff_allow:


            arduino.write(b"<")
            arduino.write(bytes(str(ang2), 'utf-8'))
            arduino.write(b"*")
            arduino.write(bytes(str(ang2+1), 'utf-8'))
            arduino.write(b">")

            
    else:
            print("diff too large")


    arduino_data = arduino.readline()      
        
    try:
            print("arduino serial: ", arduino_data.decode('utf-8'))
    except:
        pass

    cv.line(frame, (int(width / 2), height), (cX, cY), (255, 255, 0), 5)
        
    try:
        hori = np.concatenate((frame, frameHSV), axis=1)
        cv.imshow("window", hori)
    except Exception as e:
        print(str(e))
 
    if cv.waitKey(1) == ord('q'):
        break


cap.release()
cv.destroyAllWindows()

arduino.close()
