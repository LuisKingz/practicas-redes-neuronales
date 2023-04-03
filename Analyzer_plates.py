import cv2
import pytesseract
import numpy as np
import imutils
import tkinter as tk
from tkinter import ttk, messagebox

flag = True
text_identify = False
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def select_area_of_interest(frame):
    frame = imutils.resize(frame,height=680)
    # Create a copy of the input frame to display the selected area
    frame_copy = frame.copy()
    # Select the area of interest using the cv2.selectROI function
    x, y, w, h = cv2.selectROI('Select Area of Interest', frame_copy,True,False)
    # Close the window
    cv2.destroyAllWindows()
    # Return the selected area as a numpy array of points
    return np.array([[x,y], [x+w,y], [x+w,y+h], [x,y+h]])

def main():
    cap = cv2.VideoCapture('C:/Users/Gerardo/Downloads/Untitled.avi')
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    
    ret, frame = cap.read()
    area_pts = select_area_of_interest(frame)
    if area_pts[0][0] == 0 and area_pts [1][0] == 0 and area_pts[2][0] == 0 and area_pts[3][0] == 0:
        response =  messagebox.askyesno(message="No has seleccionado área de interes, ¿Volver a seleccionar?", title="Título")
        if response:
            area_pts = select_area_of_interest(frame)
        
        else:
            cap.release()
            cv2.destroyAllWindows()  
    
    texto_placa = ""
    while (cap.isOpened()):
        ret, frame = cap.read();
        if ret == False: break
        
        frame = process_frame(frame,area_pts,texto_placa)
        
        cv2.imshow("video", frame)
        k = cv2.waitKey(70) & 0xFF
        if k == 32:
            global flag, text_identify
            if flag:
                cv2.waitKey(-1)
                flag = False
            else:
                cv2.waitKey(50)
                flag = True
        if k == 27: break
        if k == ord("t"):
            text_identify = True
            print("Parar de identificar")
        if k == ord("f"):
            text_identify = False
            print("Volver a identificar")
        
    cap.release()
    cv2.destroyAllWindows()

def process_frame(frame, area_pts,texto_placa):
    global text_identify
    frame = imutils.resize(frame, width=1500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (2, 2))
    canny = cv2.Canny(gray, 80, 150)

    # area_pts = np.array([[500,250],[1190,250],[1190,500],[500,500]])
    
    imAux = create_mask(frame, area_pts, canny)
    image_area = cv2.bitwise_or(canny, canny, mask=imAux)
    #cv2.imshow("image_area",image_area)

    cnts = get_contours(image_area)
    color = (0, 255, 0)  
    for cnt in cnts:
        if text_identify:
            break
        area, approx = get_area_and_approx(cnt)
        if len(approx) == 4 and area > 8000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            placa = gray[y:y+h,x:x+w]
            # cv2.imshow("placa", placa)
            texto_placa = get_plate_text(placa)
            color = (0,255,0)
            if len(texto_placa) < 7 and texto_placa != "":
                texto_placa = ""
                # draw_analysis_area(frame, area_pts, color, texto_movimiento)
                # draw_analysis_area(frame, area_pts, color, texto_movimiento)

    draw_analysis_area(frame, area_pts, color, texto_placa)
    return texto_placa,frame

def create_mask(frame, area_pts, canny):
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    return imAux

def get_contours(image_area):
    return cv2.findContours(image_area, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

def get_area_and_approx(cnt):
    area = cv2.contourArea(cnt)
    epsilon = 0.09 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    return area, approx

def get_plate_text(placa):
    return pytesseract.image_to_string(placa, config='--oem 3 --psm 11 -c tessedit_char_whitelist=ABCDEFGHIJKLMÑNOPQRSTUVWXYZ0123456789')

def draw_analysis_area(frame, area_pts, color, texto_movimiento):
    #cv2.rectangle(frame, (0,0), (frame.shape[1],40), (0,255,0), 3)
    cv2.drawContours(frame, [area_pts], -1, color, 2)
    #cv2.putText(frame, texto_movimiento, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

