from tkinter import *
from PIL import Image, ImageTk

class App:
    def __init__(self, master):
        self.master = master
        self.zoom_value = 100 # initial zoom value
        self.canvas = Canvas(master, width=500, height=500)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.image = Image.open("C:/Users/Gerardo/Downloads/mm/nc2.jpg")

        # Resize the image to fit the window
        self.image = self.image.resize((500, 500), Image.ANTIALIAS)

        # Convert the image to Tkinter-compatible format
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_id = self.canvas.create_image(0, 0, image=self.tk_image, anchor=NW)
        self.scale = Scale(master, from_=50, to=200, orient=HORIZONTAL, command=self.zoom)
        self.scale.pack(fill=X, padx=10, pady=10)
    
    def zoom(self, value):
        self.zoom_value = int(value)
        new_width = int(self.image.width * self.zoom_value / 100)
        new_height = int(self.image.height * self.zoom_value / 100)
        self.zoomed_image = ImageTk.PhotoImage(self.image.resize((new_width, new_height), Image.ANTIALIAS))
        self.canvas.itemconfig(self.image_id, image=self.zoomed_image)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # get current coordinates of the center of the canvas
        cx = self.canvas.winfo_width() // 2
        cy = self.canvas.winfo_height() // 2

        # move the image to the center of the canvas
        self.canvas.move(self.image_id, cx - self.canvas.canvasx(cx), cy - self.canvas.canvasy(cy))
        
root = Tk()
app = App(root)
root.mainloop()