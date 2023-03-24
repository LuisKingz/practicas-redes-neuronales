import cv2
import pytesseract
import numpy as np
import imutils

def main():
    cap = cv2.VideoCapture('C:/Users/Gerardo/Downloads/Untitled.avi')
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    while (cap.isOpened()):
        ret, frame = cap.read();
        if ret == False: break
        
        roi = draw_roi(frame)
        if roi is not None:
            area_pts = np.array([[roi[0],roi[1]],[roi[2],roi[1]],[roi[2],roi[3]],[roi[0],roi[3]]])
        else:
            area_pts = np.array([[500,250],[1190,250],[1190,500],[500,500]])

        frame = process_frame(frame,area_pts)
        cv2.imshow("video", frame)
        k = cv2.waitKey(70) & 0xFF
        if k == 27: break
        
    cap.release()
    cv2.destroyAllWindows()

def process_frame(frame,area_pts):
    frame = imutils.resize(frame, width=1200)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (2, 2))
    canny = cv2.Canny(gray, 80, 150)
    

    imAux = create_mask(frame, area_pts, canny)
    image_area = cv2.bitwise_or(canny, canny, mask=imAux)

    cnts = get_contours(image_area)
    color, texto_movimiento = (0, 255, 0), "Placa: "
    for cnt in cnts:
        area, approx = get_area_and_approx(cnt)
        if len(approx) == 4 and area > 8000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            placa = gray[y:y+h,x:x+w]
            cv2.imshow("placa", placa)
            texto_movimiento = get_plate_text(placa)
            if texto_movimiento != "":
                color = (0,0,255)
                print(texto_movimiento)
                break

    draw_analysis_area(frame, area_pts, color, texto_movimiento)
    return frame

def create_mask(frame, area_pts, canny):
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    return imAux

def get_contours(image_area):
    cnts, _ = cv2.findContours(image_area, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return cnts

def get_area_and_approx(cnt):
    area = cv2.contourArea(cnt)
    epsilon = 0.09 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    return area, approx

def get_plate_text(placa):
    texto_movimiento = "Placa: " + pytesseract.image_to_string(placa, config='--oem 3 --psm 11')
    return texto_movimiento

def draw_analysis_area(frame, area_pts, color, texto_movimiento):
    cv2.rectangle(frame, (0,0), (frame.shape[1],40), (0,255,0), 3)
    cv2.drawContours(frame, [area_pts], -1, color, 2)
    cv2.putText(frame, texto_movimiento, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

def draw_roi(frame):
    roi_pts = []
    roi_drawing = False
    frame = imutils.resize(frame, width=1200)

    def draw_rectangle(event, x, y, flags, param):
        nonlocal roi_pts, roi_drawing

        if event == cv2.EVENT_LBUTTONDOWN:
            roi_drawing = True
            roi_pts = [(x, y)]
        elif event == cv2.EVENT_MOUSEMOVE:
            if roi_drawing:
                roi_pts.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP:
            roi_drawing = False

    cv2.namedWindow("draw_roi")
    cv2.setMouseCallback("draw_roi", draw_rectangle)

    while True:
        roi_frame = frame.copy()

        if len(roi_pts) == 2:
            cv2.rectangle(roi_frame, roi_pts[0], roi_pts[1], (0, 0, 255), 2)

        cv2.imshow("draw_roi", roi_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            roi_pts = []
        elif key == ord("c"):
            cv2.destroyWindow("draw_roi")
            return roi_pts
main()