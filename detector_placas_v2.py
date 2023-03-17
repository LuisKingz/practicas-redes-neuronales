import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def detector_placas(self, image):
    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(image,kernel,iterations=1)
    gray = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5),0)
    canny = cv2.Canny(gray, 50, 200)
    canny = cv2.dilate(canny,None,iterations=1)
    cnts, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        epsilon = 0.09 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        if len(approx) == 4 and area > 800 and area < 6000:
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            aspect_ratio = float(w)/h
            if aspect_ratio > 1.90 and aspect_ratio < 2.5:
                placa = gray[y:y+h, x:x+w]
                return pytesseract.image_to_string(placa, config='--oem 3 --psm 9')



