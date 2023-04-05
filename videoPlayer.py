import tkinter as tk
import cv2
import imutils
import numpy as np
import PIL.Image, PIL.ImageTk
from tkinter import ttk, filedialog
from Analyzer_plates import select_area_of_interest,process_frame
from Draggable import Draggable_elements


class VideoPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Reproductor de Video")
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)
    
        self.grid_master = tk.Frame(self.master)
        
        self.playing = False
        self.paused = False
        self.started = False
        self.texto_placas = ""
        self.plate = ""
        self.index_plate = 1
        self.file_name = ""
        self.click_counter = 0
        self.points = []
        self.start_x = None
        self.start_y = None
        self.frame_temp = None
        
        menu = tk.Menu(self.master)
        archivo = tk.Menu(menu)
        archivo.add_command(label="Cargar Video", command=self.load_video)
        archivo.add_command(label="Cerrar", command=self.close_window)
        menu.add_cascade(label="Archivo", menu=archivo)
        self.master.config(menu=menu)

        self.dragging_slider = False
        self.bg_canvas = tk.Canvas(self.grid_master, width=1208, height=680)
        self.bg_canvas.config(bg='black')
        self.bg_canvas.grid(row=0,column=0, padx=10, pady=10)

        self.canvas = tk.Canvas(self.grid_master, width=1208, height=680)
        self.canvas.config(bg='skyblue')
        self.canvas.grid(row=0,column=0, padx=10, pady=10)

        self.canvas.bind("<Button-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)

        self.cap = None
        self.table = ttk.Treeview(self.grid_master)
        self.configure_table()
        self.table.grid(row=0,column=1, padx=10, pady=10)

        self.create_buttons()
        self.area_pts = np.array([])
        self.grid_master.pack(fill="both")

    def on_keypress(self,event):
        if event == ord('\r'):
            self.play_video()

    def load_video(self):
        self.file_name = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi")])
        if self.file_name:
            if self.cap:
                self.cap.release()
            self.cap = cv2.VideoCapture(self.file_name)
            ret, frame =self.cap.read()
            frame = imutils.resize(frame,height=680)
            self.frame_temp = frame
            self.add_image_to_canvas(frame)
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.current_time = 0
            self.time_slider.configure(to=self.total_frames)
            self.total_time_video()
            self.canvas.bind("<Button-3>", self.on_drag_select_area_of_interest)
            self.canvas.bind("<B3-Motion>", self.on_drag_motion_select_area_of_interest)
            self.time_slider.bind("<MouseWheel>",self.slide_mousewheel)
            self.update_frame()
            
    def create_buttons(self):
        self.buttons_frame = tk.Frame(self.grid_master)
        self.buttons_frame.grid(row=1,column=0);
        self.slider_frame = tk.Frame(self.grid_master)
        self.slider_frame.grid(row=2,column=0);

        self.btn_play = tk.Button(self.buttons_frame, text="Reproducir", command=self.play, state=tk.DISABLED)
        self.btn_play.grid(row=0, column=0, padx=10, pady=10)

        self.btn_pause = tk.Button(self.buttons_frame, text="Pausar", command=self.pause, state=tk.DISABLED)
        self.btn_pause.grid(row=0, column=1, padx=10, pady=10)

        self.btn_stop = tk.Button(self.buttons_frame, text="Detener", command=self.stop, state=tk.DISABLED)
        self.btn_stop.grid(row=0, column=2, padx=10, pady=10)

        self.btn_start = tk.Button(self.buttons_frame, text="Inicio", command=self.start, state=tk.DISABLED)
        self.btn_start.grid(row=0, column=3, padx=10, pady=10)

        self.btn_backward = tk.Button(self.buttons_frame, text="<<", command=self.backward, state=tk.DISABLED)
        self.btn_backward.grid(row=0, column=4, padx=10, pady=10)

        self.btn_forward = tk.Button(self.buttons_frame, text=">>", command=self.forward, state=tk.DISABLED)
        self.btn_forward.grid(row=0, column=5, padx=10, pady=10)

        self.time_label = tk.Label(self.slider_frame, text="00:00:00")
        self.time_label.grid(row=0,column=0,padx=10, pady=10)

        self.time_slider = tk.Scale(self.slider_frame, from_=0, orient=tk.HORIZONTAL, length=1000, command=self.slide)
        # self.time_slider.pack(side=tk.BOTTOM, pady=10)
        self.time_slider.grid(row=0,column=1,padx=10, pady=10)

        self.total_time_label = tk.Label(self.slider_frame, text="00:00:00")
        self.total_time_label.grid(row=0,column=2,padx=10, pady=10)
    
    def add_image_to_canvas(self,frame):
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = PIL.Image.fromarray(cv2image)
        new_height = 680
        ratio = float(new_height) / img.size[1]
        new_width = int(ratio * img.size[0])
        resized_img = img.resize((new_width, new_height))
        imgtk = PIL.ImageTk.PhotoImage(image=resized_img)
        self.canvas.create_image(0, 0, image=imgtk, anchor=tk.NW)
        self.canvas.image = imgtk
        
    def update_frame(self):
        if self.playing:
            if not self.paused:
                ret = self.cap.grab()
                if ret:
                    if (self.cap.isOpened()):
                        self.current_time = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                        self.time_slider.set(self.current_time)
                        self.update_time_label()

                        ret, frame = self.cap.retrieve()
                        frame = imutils.resize(frame,height=680)
                        self.frame_temp = frame
                        plate_text,frame = process_frame(frame,self.area_pts,self.texto_placas)
                        if len(plate_text) > 6 and plate_text != "":
                            self.plate = plate_text
                            self.add_text_to_table()
                        
                        self.add_image_to_canvas(frame)

                        if not self.started:
                            self.config_buttons()
                            self.started = True
                            
                else:
                    self.stop()
        self.update_time_label()
        self.time_slider.set(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
        self.master.after(1000 // self.fps, self.update_frame)

    def play(self):
        if not self.paused:
            self.playing = True
    
    def pause(self):
        if self.playing:
            self.paused = not self.paused
            self.btn_pause.config(text="Reanudar" if self.paused else "Pausar")
            if self.paused:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cap.get(cv2.CAP_PROP_POS_FRAMES) - 1 )
            else:
                self.play()

    def pause_on_drag(self):
        if self.playing:
            self.paused = not self.paused
            if self.paused:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cap.get(cv2.CAP_PROP_POS_FRAMES) - 1 )
            else:
                self.play()
    
    def stop(self):
        self.playing = False
        self.cap.release()
        self.started = False
        self.config_buttons()
        # Vuelve a reproducir desde el principio
        self.cap = cv2.VideoCapture(self.file_name)
        self.canvas.delete("all")
        self.delete_columns()

    def config_buttons(self):
        if self.playing and not self.started:
            self.btn_pause.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.NORMAL)
            self.btn_start.config(state=tk.NORMAL)
            self.btn_backward.config(state=tk.NORMAL)
            self.btn_forward.config(state=tk.NORMAL)
        else:
            self.btn_pause.config(text="Pausar", state=tk.DISABLED)
            self.btn_stop.config(state=tk.DISABLED)
            self.btn_start.config(state=tk.DISABLED)
            self.btn_backward.config(state=tk.DISABLED)
            self.btn_forward.config(state=tk.DISABLED)


    def start(self):
        #self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.paused = False
        self.btn_play.config(text="Reproducir")
    
    def backward(self):
        pos_frames = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        new_pos_frames = pos_frames - self.fps * 5
        if new_pos_frames < 0:
            new_pos_frames = 0
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_pos_frames)
    
    def forward(self):
        pos_frames = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        new_pos_frames = pos_frames + self.fps * 5
        if new_pos_frames > self.total_frames:
            new_pos_frames = self.total_frames
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_pos_frames)

    def close_window(self):
        self.paused = True
        if self.cap:
            self.cap.release()
        self.master.destroy()

    def slide(self, event):
        self.current_time = int(self.time_slider.get())
        self.update_time_label()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_time)

    def slide_mousewheel(self,event):
        if event.delta > 0:
            self.forward()
        else:
            self.backward()
    
    def update_time_label(self):
        current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        current_time = current_frame // self.fps
        hours, rem = divmod(current_time, 3600)
        minutes, seconds = divmod(rem, 60)
        time_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        self.time_label.config(text=time_str)
        # self.time_slider.set(current_frame)

    def total_time_video(self):
        all_time = self.total_frames // self.fps
        hours,rem = divmod(all_time,3600)
        minutes, seconds = divmod(rem,60)
        time_str = "{:02d}:{:02d}:{:02d}".format(hours,minutes,seconds)
        self.total_time_label.config(text=time_str)
    
    def add_text_to_table(self):
        self.table.insert(parent="",index=self.index_plate,iid=self.index_plate,text=self.index_plate,values=(self.plate))
        self.index_plate +=1
    
    def delete_columns(self):
        self.table.delete(*self.table.get_children())
        self.index_plate = 1    
       
    def configure_table(self):
        self.table.configure(columns=("placa"))
        self.table.heading("#0", text="Index")
        self.table.heading("placa", text="Placa")
        self.table.column("#0", width=50)
        self.table.column("placa", width=100)

    def on_drag_select_area_of_interest(self,event):
        print("interest area")
        self.start_x, self.start_y = event.x, event.y
        self.btn_play.config(state=tk.NORMAL)

    def on_drag_motion_select_area_of_interest(self,event):
        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x, event.y
        self.canvas.delete("all")
        self.add_image_to_canvas(self.frame_temp)
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="red")
        self.area_pts = np.array([[x1,y1],[x2,y1],[x2,y2],[x1,y2]])

    def on_drag_start(self,event):
        widget = event.widget
        widget.start_x = event.x
        widget.start_y = event.y
        
    def on_drag_motion(self,event):
        widget = event.widget
        x = widget.winfo_x() - widget.start_x + event.x
        y = widget.winfo_y() - widget.start_y + event.y
        widget.place(x=x, y=y)


def imprimir_informacion(r):
    altura = r.winfo_reqheight()
    anchura = r.winfo_reqwidth()
    altura_pantalla = r.winfo_screenheight()
    anchura_pantalla = r.winfo_screenwidth()
    print(f"Altura: {altura}\nAnchura: {anchura}\nAltura de pantalla: {altura_pantalla}\nAnchura de pantalla: {anchura_pantalla}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Reproductor de video")
    player = VideoPlayer(root)
    root.resizable(False,False)
    root.geometry("1400x820")
    #imprimir_informacion(root)
    player.start()
    root.mainloop()    
    
