import serial
import numpy as np
import time
import cv2 as cv

#initialize communication with arduino
arduino = serial.Serial('COM3', 115200)
time.sleep(2)

#create variable for indexing corners
count = 0

#read source image
img = cv.imread(r"pics\4.png")

#load source dimensions
height = img.shape[0]
width = img.shape[1]

#calculate where the center of the source lies
vertical_center = width / 2
horizontal_center = height / 2

#convert source to grayscale image for efficiency
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#detect corners (source image, max num of corners, 
#confidence, min distance between each corner)
corners = cv.goodFeaturesToTrack(gray, 20, 0.15, 10)
corners = np.int0(corners)

#divide image into equal rectangles
cv.line(img, (0, int(horizontal_center)), (int(width),int(horizontal_center) ), (0,255, 0), 5)
cv.line(img, (int(vertical_center), int(height)), (int(vertical_center),0), (0,255, 0), 5)

#go through each corner
for i in corners:
    #index corner
    count+=1

    #convert numpy array into coordinates of corner
    x, y = i.ravel()

    print("corner coordinates: ", x, y)

    #create circle around each corner
    cv.circle(img, (x, y), 20, (255, 0, 0), 5)

    if x < vertical_center:
         print("corner number",count, "is in the left half")
        #  time.sleep(2)
         arduino.write("4".encode())
      
    elif x > vertical_center:
        print("corner number",count, "is in the right half")
        # time.sleep(2)
        arduino.write("3".encode())

    if y < horizontal_center :
        print("corner number",count, "is in the upper half")
        # time.sleep(2)
        arduino.write("2".encode())
    elif y > horizontal_center:
        print("corner number",count, "is in the lower half")
        # time.sleep(2)
        arduino.write("1".encode())


print("size of image", width, height)

cv.imshow("image", img)

cv.waitKey(0)

x = arduino.readline().decode('utf-8')  

print(x)

arduino.close()