from ctypes import sizeof
import serial
import numpy as np
import time
import cv2 as cv

#initialize communication with arduino
arduino = serial.Serial('COM3', 115200)
time.sleep(2)

#video capture variable
cap = cv.VideoCapture(0)   

#create variable for indexing corners
count = 0

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

    #divide image into equal rectangles
    cv.line(frame, (0, int(horizontal_center)), (int(width),int(horizontal_center) ), (0,255, 0), 5)
    cv.line(frame, (int(vertical_center), int(height)), (int(vertical_center),0), (0,255, 0), 5)
    
    #avoid error, where vscode would complain about not seeing any corners
    if np.any(corners) != None:
      corners = np.int0(corners) 
    
       #convert numpy array into coordinates of corner
      for i in corners:
      #index corner
       count+=1
      #convert corner array into coordinates of each corner
       x, y = i.ravel() 
       print(i)
       print("corner coordinates: ", x, y)
       

     #create circle around each corner
       cv.circle(frame, (x, y), 20, (255, 0, 0), 5)

       if x > vertical_center and y < horizontal_center:
          print("corner number",count, "is in the upper right part")
          # time.sleep(2)
          arduino.write("4".encode())
         
       elif x < vertical_center and y < horizontal_center:
           print("corner number",count, "is in the upper left part")
           # time.sleep(2)
           arduino.write("3".encode())
          
       elif x > vertical_center and y > horizontal_center :
          print("corner number",count, "is in the lower right part")
         # time.sleep(2)
          arduino.write("2".encode())

       elif x < vertical_center and y > horizontal_center:
          print("corner number",count, "is in the lower left part")
         # time.sleep(2)
          arduino.write("1".encode())

       time.sleep(1)

       cv.imshow("image", frame)
       print(len(corners))
       if cv.waitKey(1) == ord('q'):
         break

         

cap.release()
cv.destroyAllWindows()
arduino.close()


# print("size of image", width, height)

# x = arduino.readline().decode('utf-8')  

# print(x)