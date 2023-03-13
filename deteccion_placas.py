import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

placa = []
image = cv2.imread('uploads/imagen_1601928518208_b1_S1_001_1_charlotte.jpg')

# cambio de colores de bgr a escalas de blancos
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# atenuar la imagen del ruido
gray = cv2.blur(gray,(2,2))
canny = cv2.Canny(gray,80,150)
#engrosar areas blancas
#canny = cv2.dilate(canny,None,iterations=1)


cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#dibular los contornos
# cv2.drawContours(image,cnts,-1,(0,255,0),1)

for c in cnts:
    area = cv2.contourArea(c)
    # print(area)
    x,y,w,h = cv2.boundingRect(c)
    epsilon = 0.09 * cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    if len(approx) == 4 and area > 8000:
        print('area', area)
        cv2.drawContours(image,[c],0,(0,255,0),2)
        aspect_ratio = float(w)/h
        #if aspect_ratio > 2.4:
        placa = gray[y:y+h,x:x+w]
        text = pytesseract.image_to_string(placa,config='--psm 11')
        print('placa', text)
        cv2.imshow('placa',placa)
        cv2.moveWindow('placa',880,100)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
        cv2.putText(image,text,(x-20,y-10),1,2.2,(0,255,0),1)

cv2.imshow('Image',image)
# cv2.imshow('Canny',gray)
cv2.moveWindow('Image',45,10)
cv2.waitKey(0)