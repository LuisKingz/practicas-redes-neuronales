import tkinter as tk
from tkinter import ttk
import cv2
import imutils
import PIL.Image, PIL.ImageTk
from video_loader_v3 import select_area_of_interest,process_frame

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
        
        self.cap = cv2.VideoCapture("C:/Users/Gerardo/Downloads/Untitled.avi")
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_time = 0
        self.dragging_slider = False
    
        self.canvas = tk.Canvas(self.grid_master, width=1208, height=680)
        self.canvas.grid(row=0,column=0, padx=10, pady=10)
        #self.canvas.pack()

        self.table = ttk.Treeview(self.grid_master, columns=("placa"))
        self.table.heading("#0",text="Índice")
        self.table.heading("placa",text="Placa")
        self.table.grid(row=0,column=1, padx=10, pady=10)
        #self.table.pack(side=tk.RIGHT)

        
        self.create_buttons()
        ret,frame = self.cap.read()        
        self.area_pts = select_area_of_interest(frame)
        self.update_frame()
        self.total_time_video()
        self.grid_master.pack()

    def create_buttons(self):
        self.buttons_frame = tk.Frame(self.grid_master)
        self.buttons_frame.grid(row=1,column=0);
        self.slider_frame = tk.Frame(self.grid_master)
        self.slider_frame.grid(row=2,column=0);
        #self.buttons_frame.pack()

        self.btn_play = tk.Button(self.buttons_frame, text="Reproducir", command=self.play)
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
        #self.time_label.pack(side=tk.LEFT, pady=10)
        self.time_label.grid(row=0,column=0,padx=10, pady=10)

        self.time_slider = tk.Scale(self.slider_frame, from_=0, to=self.total_frames, orient=tk.HORIZONTAL, length=1000, command=self.slide)
        # self.time_slider.pack(side=tk.BOTTOM, pady=10)
        self.time_slider.grid(row=0,column=1,padx=10, pady=10)

        self.total_time_label = tk.Label(self.slider_frame, text="00:00:00")
        #self.total_time_label.pack(side=tk.RIGHT, pady=10)
        self.total_time_label.grid(row=0,column=2,padx=10, pady=10)


    def update_frame(self):
        
        if self.playing:
            if not self.paused:
                ret, frame = self.cap.read()
                frame = imutils.resize(frame,height=680)
                plate_text,frame = process_frame(frame,self.area_pts,self.texto_placas)
                if len(plate_text) > 6 and plate_text != "":
                    self.plate = plate_text
                    self.add_text_to_table()
                
                if ret:
                    if (self.cap.isOpened()):

                        #frame = imutils.resize(frame, width=1500,height=680)
                        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img = PIL.Image.fromarray(cv2image)
                        new_height = 680
                        ratio = float(new_height) / img.size[1]
                        new_width = int(ratio * img.size[0])
                        resized_img = img.resize((new_width, new_height))
                        imgtk = PIL.ImageTk.PhotoImage(image=resized_img)
                        self.canvas.create_image(0, 0, image=imgtk, anchor=tk.NW)
                        self.canvas.image = imgtk

                        if not self.started:
                            self.started = True
                            self.btn_pause.config(state=tk.NORMAL)
                            self.btn_stop.config(state=tk.NORMAL)
                            self.btn_start.config(state=tk.NORMAL)
                            self.btn_backward.config(state=tk.NORMAL)
                            self.btn_forward.config(state=tk.NORMAL)
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
    
    def stop(self):
        self.playing = False
        self.cap.release()
        self.started = False
        self.btn_pause.config(text="Pausar", state=tk.DISABLED)
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_start.config(state=tk.DISABLED)
        self.btn_backward.config(state=tk.DISABLED)
        self.btn_forward.config(state=tk.DISABLED)
        
        # Vuelve a reproducir desde el principio
        self.cap = cv2.VideoCapture("C:/Users/Gerardo/Downloads/Untitled.avi")
        self.canvas.delete("all")

    def start(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
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
        self.cap.release()
        self.master.destroy()
    
    def slide(self, val):
        self.current_time = int(val)
        self.dragging_slider = True
    
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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Reproductor de video")
    player = VideoPlayer(root)
    player.start()
    root.mainloop()