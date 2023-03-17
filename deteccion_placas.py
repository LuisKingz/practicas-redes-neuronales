import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

placa = []
# image = cv2.imread('uploads/imagen_1601928518208_b1_S1_001_1_charlotte.jpg')
# image = cv2.imread('uploads/imagen_1601927515540_b1_S1_001_1_charlotte.jpg')
# image = cv2.imread('uploads/imagen_1601930196542_b1_S1_001_1_charlotte.jpg')
image = cv2.imread('uploads/imagen_1601589420833_b1_S1_001_1_charlotte.jpg')
# image = cv2.imread('uploads/imagen_1601928709889_b1_S1_001_1_charlotte.jpg')
# image = cv2.imread('uploads/imagen_1601915278227_b1_S1_001_1_charlotte.jpg')
# image = cv2.imread('uploads/imagen_1601929129809_b1_S1_001_1_charlotte.jpg')


kernel = np.ones((1, 1), np.uint8)
erosion = cv2.erode(image,kernel,iterations=1)
# cambio de colores de bgr a escalas de blancos
gray = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)
# atenuar la imagen del ruido
gray = cv2.GaussianBlur(gray, (5, 5),0)
canny = cv2.Canny(gray, 50, 200)
# engrosar areas blancas

canny = cv2.dilate(canny,None,iterations=1)


cnts, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE)
# dibular los contornos
# cv2.drawContours(image,cnts,-1,(0,255,0),2)

for c in cnts:
    area = cv2.contourArea(c)
    x, y, w, h = cv2.boundingRect(c)
    epsilon = 0.09 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    if len(approx) == 4 and area > 4000 and area < 9000:
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        aspect_ratio = float(w)/h
        # if aspect_ratio > 2:
        placa = gray[y:y+h, x:x+w]
        text12 = pytesseract.image_to_string(placa, config='--oem 3 --psm 9')
        print("placa= " ,text12)
        cv2.imshow('placa', placa)
        cv2.moveWindow('placa', 880, 100)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.putText(image, text12, (x-20, y-10),1, 2.2, (0, 255, 0), 1)

cv2.imshow('Image', image)
cv2.imshow('Canny', gray)
# cv2.imshow('erode', erosion)
cv2.moveWindow('Image', 45, 10)
cv2.waitKey(0)
