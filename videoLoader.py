import cv2
from detector_placas_v2 import detector_placas

capture = cv2.VideoCapture('D:/videos_prueba/12_ MIRE.mp4')

while (capture.isOpened()):
    ret, frame = capture.read()
    if (ret == True):
        cv2.imshow("gato0", frame)
        if (cv2.waitKey(30) == ord('s')):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()