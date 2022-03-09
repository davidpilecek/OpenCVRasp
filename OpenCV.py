import cv2
import numpy as np

r"vids\Piano Tiles 2 - 1. Little Star.mp4"

cap = cv2.VideoCapture(r"vids\Piano Tiles 2 - 1. Little Star.mp4")


while True:

    frame, ret = cap.read()

    cv2.imshow("video", frame)


    if cv2.waitKey(20) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows
