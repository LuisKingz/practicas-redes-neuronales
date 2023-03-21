import cv2
import numpy as np
import imutils

video = cv2.VideoCapture('C:/Users/Gerardo/Downloads/Untitled.avi')

while (video.isOpened()):
    ret, frame = video.read()
    frame = imutils.resize(frame,width=550)
    if ret == False: break
    cv2.imshow('Frame', frame)
    k = cv2.waitKey(40) & 0xFF
    if k == 27:
        break
video.release()
cv2.destroyAllWindows()