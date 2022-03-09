import numpy as np
import cv2

img = cv2.imread(r"pics\imageNew.jpg")


img = cv2.resize(img, (1080, 920))


hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 150])



mask = cv2.inRange(hsv, lower_blue, upper_blue)

result = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('frame', img)
cv2.imshow('mask', mask)
cv2.imshow("result", result)

cv2.waitKey(0)

cv2.destroyAllWindows()