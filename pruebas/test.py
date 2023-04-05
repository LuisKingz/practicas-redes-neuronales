import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry('400x400')

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
color = (0,255,0)

img = np.zeros((400, 400, 3), dtype=np.uint8)

start_x, start_y = None, None

def draw_rect(event):
    global start_x, start_y
    if event.num == 1:
        start_x, start_y = event.x, event.y
    elif event.num == 3:
        x1, y1 = start_x, start_y
        x2, y2 = event.x, event.y
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.create_rectangle(x1, y1, x2, y2, outline="red")

img_tk = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_tk = Image.fromarray(img_tk)
img_tk = ImageTk.PhotoImage(img_tk)

# canvas.bind("<Button-1>", draw_rect)
# canvas.bind("<Button-3>", draw_rect)

def on_drag_start(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def on_drag_motion(event):
    x1, y1 = start_x, start_y
    x2, y2 = event.x, event.y
    #cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    rectangle = canvas.create_rectangle(x1, y1, x2, y2, outline="red")
    point = np.array([[x1,y1],[x1+x2,y1],[x2,y2],[x1,y1+y2]])
 


canvas.bind("<Button-3>", on_drag_start)
canvas.bind("<B3-Motion>", on_drag_motion)

root.mainloop()