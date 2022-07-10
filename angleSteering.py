#from turtle import right
import serial
import numpy as np
import time
import cv2 as cv

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)
time.sleep(2)   

path = r"video.mp4"

cap = cv.VideoCapture(0)

speed = 80

def nothing(x):
	pass

cv.namedWindow('controls')

cv.createTrackbar('x','controls',250,500,nothing)
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


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def swerve(ang):

    global pwmMax  
    ratio = None 

    if(ang!=0):
        ratio = 90/ang
    else:
        ratio = 1

    base_speed = pwmMax

    right_wheel = round(base_speed * ratio)
    left_wheel = round(base_speed)

    return left_wheel, right_wheel



left_wheel = 0

right_wheel = 0

pwmMin = 140

pwmMax = 255 * speed/100

phi = None
center_left = 175
center_right = 325

lower_black = 250
upper_black = 255

diff_allow = 50

counter = 0

ang1 = 0
ang2 = 0

white_min=3

white_max=12


threshold = 180

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

    #th = cv.bitwise_not(th)


    mask_black = cv.inRange(th, lower_black, upper_black)
    

    contours_black, hierarchy_black = cv.findContours(crop_img(mask_black, width), cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)


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


    if phi != None:
     if counter % 2 == 1:
            ang1 = round(phi)

     elif counter % 2==0:
            ang2 = round(phi)

    diff = np.abs(ang1 - ang2)
        

    if counter % 2 == 0 and diff<=diff_allow:
            left_wheel, right_wheel = swerve(ang1)
    elif counter % 2 == 1 and diff<=diff_allow:
            left_wheel, right_wheel = swerve(ang2)

            
    else:
            print("diff too large")

    arduino.write(b"<")
    arduino.write(bytes(str(left_wheel), 'utf-8'))
    arduino.write(b"*")
    arduino.write(bytes(str(right_wheel), 'utf-8'))
    arduino.write(b">")


    arduino_data = arduino.readline()      
        



    try:
            print("arduino serial: ", arduino_data.decode('utf-8'))
    except:
        pass

    cv.line(frame, (int(width / 2), height), (cX, cY), (255, 255, 0), 5)
        
    try:
        cv.imshow("windowframe", frame)
       
        

    except Exception as e:
        print(str(e))
 
    if cv.waitKey(1) == ord('q'):
            arduino.write(b"<")
            arduino.write(bytes(str(0), 'utf-8'))
            arduino.write(b"*")
            arduino.write(bytes(str(0), 'utf-8'))
            arduino.write(b">")
            break


cap.release()
cv.destroyAllWindows()

arduino.close()