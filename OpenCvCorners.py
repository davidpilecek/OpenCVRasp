import cv2
import numpy as np


img = cv2.imread(r"pics\PLC010_06.jpg")



gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 2000, 0.15, 10)

corners = np.int0(corners)


cv2.waitKey(0)