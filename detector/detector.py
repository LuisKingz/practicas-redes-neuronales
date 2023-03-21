import cv2
import pytesseract
import numpy as np
import imutils

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


def find_plate(frame):
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
            return texto_movimiento

