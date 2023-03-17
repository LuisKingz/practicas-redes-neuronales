import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def detector_placas(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(2,2))
    canny = cv2.Canny(gray,80,150)
    cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.09 * cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        if len(approx) == 4 and area > 8000:
            cv2.drawContours(image,[c],0,(0,255,0),2)
            aspect_ratio = float(w)/h
            #if aspect_ratio > 2.4:
            placa = gray[y:y+h,x:x+w]
            return pytesseract.image_to_string(placa,config='--psm 11')
            # cv2.imshow('placa',placa)
            # cv2.moveWindow('placa',880,100)
            # cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
            # cv2.putText(image,text,(x-20,y-10),1,2.2,(0,255,0),1)

def prueba_intancia():
    print("Hola mundo desde el dectector")
    