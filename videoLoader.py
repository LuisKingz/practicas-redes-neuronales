import cv2
from detector.detector_placas_v2 import detector_placas

# capture = cv2.VideoCapture('C:/Users/Gerardo/Downloads/Untitled.avi')
capture = cv2.VideoCapture('C:/proyectos/Untitled.avi')
aux_placa = ""
while (capture.isOpened()):
    ret, frame = capture.read()
    if (ret == True):
        cv2.imshow("gato0", frame)
        placa = detector_placas(frame)
        if(placa != None):
            aux_placa = placa
            print("placa= ",placa)
        if (cv2.waitKey(30) == ord('s')):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()