import cv2
import time
import imutils

cap = cv2.VideoCapture('C:/Users/Gerardo/Downloads/Untitled.avi')
fps = cap.get(cv2.CAP_PROP_FPS)  # Obtener los fps del video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Obtener el número total de fotogramas del video
current_frame = 0  # Inicializar el fotograma actual como cero
delay = int(1000/fps)  # Calcula el tiempo de retraso entre cada fotograma
playing = True  # Establecer el indicador de reproducción en verdadero

while True:
    # Si la reproducción está activada
    if playing:
        # Leer un fotograma del video
        ret, frame = cap.read()
        # Si no se puede leer el fotograma, salir del bucle
        if not ret:
            break
        # Mostrar el fotograma
        frame = imutils.resize(frame, width=1200)
        cv2.imshow('video', frame)
        # Incrementar el fotograma actual
        current_frame += 1
    # Esperar un tiempo antes de mostrar el siguiente fotograma
    key = cv2.waitKey(delay)
    # Si se presiona la tecla 'q', salir del bucle
    if key == ord('q'):
        break
    # Si se presiona la tecla 'p', cambiar el indicador de reproducción
    elif key == ord('p'):
        playing = not playing
    # Si se presiona la tecla 'f', adelantar el video en un segundo
    elif key == ord('d'):
        current_frame = min(current_frame + int(fps), total_frames)
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
    # Si se presiona la tecla 'b', retroceder el video en un segundo
    elif key == ord('a'):
        current_frame = max(current_frame - int(fps), 0)
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
