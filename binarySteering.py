#from turtle import right
import config as c
import serial
import numpy as np
import time
import cv2 as cv

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)
time.sleep(2)   

path = r"video.mp4"

cap = cv.VideoCapture(2)

phi = None
counter = 0

ang1 = 0
ang2 = 0

left_wheel = 0

right_wheel = 0


speed = 80

centRange = 15

right_angle_max = 90 + centRange
left_angle_max = 90 - centRange

pwmMin = 180

pwmMax = 255 * speed/100


center_left = 175
center_right = 325

lower_color = 250
upper_color = 255

diff_allow = 50

threshold = 185


def nothing(x):
	pass

cv.namedWindow('controls')

cv.createTrackbar('x','controls',200,500,nothing)
cv.createTrackbar('y','controls',500,500,nothing)

def crop_img(img, width):
    #crop image into area of interest
    height_1 = int(cv.getTrackbarPos('x', 'controls'))
    height_2 = int(cv.getTrackbarPos('y', 'controls'))
    vertices = [(0, height_1), (0, height_2),(width , height_2), (width, height_1)]
    vertices = np.array([vertices], np.int32)

    #create pure black frame size of image
    mask = np.zeros_like(img)

    match_mask_color = 255

    #create pure white frame in area of interest
    cv.fillPoly(mask, vertices, match_mask_color)
    
    #return image with other area than AOI non-reactive to contour seeking algorithm
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
    global pwmMin
    
    if (ang <= right_angle_max and ang >= left_angle_max):
        left_wheel = pwmMin
        right_wheel = pwmMin
    elif (ang > right_angle_max):
        #turn right
        left_wheel = pwmMin
        right_wheel = 0
    elif (ang < left_angle_max):
        #turn left
        left_wheel = 0
        right_wheel = pwmMin 
            

    return left_wheel, right_wheel

def straight(): 
    global pwmMax  
    global pwmMin


T = threshold   

while True:
  
    _, frame = cap.read()
    
    if(type(frame) == type(None)):
        pass
    else:
        frame = cv.resize(frame, (500, 500))
        height, width = frame.shape[:2]


    try:
        frameGR = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    except Exception as e:
        print("Camera device already in use: ", str(e))
        
    kernel = np.ones((5,5), np.uint8)

    erode = cv.erode(frameGR, kernel)

    rc, th = cv.threshold(erode, T, 255, cv.THRESH_BINARY)    

    #to make area of interest the color black, uncomment following line and decrease threshold level in config file
    #th = cv.bitwise_not(th)

    mask = cv.inRange(th, lower_color, upper_color)
    

    contours, hierarchy = cv.findContours(crop_img(mask, width), cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)


    if len(contours)>0:

        contour = max(contours, key = cv.contourArea)

        cv.drawContours(frame, contour, -1, (0, 255, 0), 5)

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
    print(phi)        

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