import cv2
from detector.detector_placas_v2 import detector_placas
import numpy as np
import imutils

capture = cv2.VideoCapture('C:/Users/Gerardo/Downloads/Untitled.avi')
aux_placa = ""
while (capture.isOpened()):
    ret, frame = capture.read()
    frame = imutils.resize(frame,width=1080)
    if (ret == True):
        cv2.imshow("gato0", frame)
        placa = detector_placas(frame)
        if(placa != None):
            aux_placa = placa
            print("placa= ",placa)
        if (cv2.waitKey(100) == ord('s')):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()