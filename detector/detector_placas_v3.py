import cv2
import pytesseract
import numpy as np
import imutils

cap = cv2.VideoCapture('C:/Users/Gerardo/Downloads/Untitled.avi')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()

while (cap.isOpened()):
    ret, frame = cap.read();
    if ret == False: break
    frame = imutils.resize(frame,width=1200)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(2,2))
    canny = cv2.Canny(gray,80,150)
    # DIBUJAR UN RECTANGULO EN FRAM, PARA SEÑALAR EL ESTADO 
    # DEL AREA EN ANALISIS (MOVIMIENTO  DETECTADO O NO DETECTADO)
    cv2.rectangle(frame,(0,0),(frame.shape[1],40),(0,255,0),3)
    color = (0,255,0)
    texto_movimiento = "Placa: "

    area_pts = np.array([[500,250],[1190,250],[1190,500],[500,500]])
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_or(canny, canny, mask=imAux)

    cnts,_ = cv2.findContours(image_area,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        epsilon = 0.09 * cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        if len(approx) == 4 and area > 8000:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            placa = gray[y:y+h,x:x+w]
            cv2.imshow("placa", placa)
            texto_movimiento = "Placa: " + pytesseract.image_to_string(placa,config='--oem 3 --psm 11')
            if texto_movimiento != "":              
                color = (0,0,255)
                print(texto_movimiento)
                break

    cv2.drawContours(frame,[area_pts],-1,color,2)
    cv2.putText(frame, texto_movimiento,(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,color,2)
    cv2.imshow("video", frame)
    # cv2.imshow("imgAux", fgmask)
    cv2.imshow("image_area", image_area)
    k = cv2.waitKey(70) & 0xFF
    if k == 27: break

cap.release()
cv2.destroyAllWindows()
