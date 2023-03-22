import cv2
import pytesseract
import numpy as np
import imutils

cap = cv2.VideoCapture('C:/Users/Gerardo/Downloads/Untitled.avi')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg = cv2.createBackgroundSubtractorMOG2()
texto_movimiento = ""
while (cap.isOpened()):
    ret, frame = cap.read(cv2.IMREAD_GRAYSCALE)
    if ret == False:
        break
    frame = imutils.resize(frame, width=1300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (3, 3))
    # gray = cv2.medianBlur(gray,5)
    canny = cv2.Canny(gray, 80, 150)
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 255, 0), 3)
    color = (0, 255, 0)

    area_pts = np.array([[500, 200], [1200, 200], [1200, 700], [500, 700]])
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_or(canny, canny, mask=imAux)

    cnts, _ = cv2.findContours(
        image_area, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        epsilon = 0.09 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if len(approx) == 4 and area > 3000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            placa = gray[y:y+h, x:x+w]

            # MOSTRAR LA PLACA ENCONTRADA EN UNA VENTANA
            # cv2.imshow("placa", placa)
            config = '--oem 3 --psm 9 -c tessedit_char_whitelist=ABCDEFGHIJKLMÑNOPQRSTUVWXYZ0123456789'
            try:
                texto_movimiento = pytesseract.image_to_string(
                    placa, config=config)
                characters_to_remove = "!()@—*“>+-/,'|£#%$&^_~"
                placa_nueva = texto_movimiento
                for character in characters_to_remove:
                    placa_nueva = texto_movimiento.replace(character, "")

                if placa_nueva != "" and len(placa_nueva) > 5 and len(placa_nueva) < 8:
                    color = (0, 0, 255)
                    print("placa= ", placa_nueva)
                    break
                else:
                    print("placa= ")
            except IOError as e:
                print("Error (%s)." % e)

    cv2.drawContours(frame, [area_pts], -1, color, 2)
    cv2.putText(frame, placa_nueva, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("video", frame)
    # cv2.imshow("imgAux", fgmask)

    # MOSTRAR LA SEGUNDA VENTANA QUE SE PASO A ESCALA DE GRISES CON LOS DEMAS FILTROS
    # cv2.imshow("image_area", image_area)

    k = cv2.waitKey(50) & 0xFF
    if k == 27:
        break
    if k == "s":
        cap.pause()

cap.release()
cv2.destroyAllWindows()
