from tkinter import *
from PIL import Image, ImageTk
from Draggable import Draggable_elements

class App:
    def __init__(self, master):
        self.master = master
        self.zoom_value = 0.5 # initial zoom value
        self.canvas = Canvas(master, width=500, height=500)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.image = Image.open("C:/Users/Gerardo/Downloads/mm/nc2.jpg")

        # Resize the image to fit the window
        self.image = self.image.resize((500, 500), Image.ANTIALIAS)

        # Convert the image to Tkinter-compatible format
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor=NW)
        self.canvas.bind("<Button-1>", Draggable_elements.on_drag_start)
        self.canvas.bind("<B1-Motion>", Draggable_elements.on_drag_motion)
        self.scale = Scale(master, from_=50, to=200, orient=HORIZONTAL, command=self.zoom)
        self.scale.pack(fill=X, padx=10, pady=10)
    
    def zoom(self, value):
        self.zoom_value = int(value)
        new_width = int(self.tk_image.width() * self.zoom_value / 100)
        new_height = int(self.tk_image.height() * self.zoom_value / 100)
        self.zoomed_image = ImageTk.PhotoImage(self.image.resize((new_width, new_height), Image.ANTIALIAS))
        self.canvas.delete(ALL)
        self.canvas.create_image(0, 0, image=self.zoomed_image, anchor=NW)
        
root = Tk()
root.geometry("500x500")
app = App(root)
root.mainloop()
