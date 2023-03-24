import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk

class VideoPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Reproductor de Video")
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.playing = False
        self.paused = False
        self.started = False
        
        self.cap = cv2.VideoCapture("C:/Users/Gerardo/Downloads/15_PACBOOK.mp4")
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        self.canvas = tk.Canvas(self.master, width=640, height=480)
        self.canvas.pack()
        
        self.create_buttons()
        self.update_frame()
    
    def create_buttons(self):
        self.btn_play = tk.Button(self.master, text="Reproducir", command=self.play)
        self.btn_play.pack(side=tk.LEFT, padx=10)
        
        self.btn_pause = tk.Button(self.master, text="Pausar", command=self.pause, state=tk.DISABLED)
        self.btn_pause.pack(side=tk.LEFT)
        
        self.btn_stop = tk.Button(self.master, text="Detener", command=self.stop, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT)
        
        self.btn_start = tk.Button(self.master, text="Inicio", command=self.start, state=tk.DISABLED)
        self.btn_start.pack(side=tk.LEFT, padx=10)
        
        self.btn_backward = tk.Button(self.master, text="<<", command=self.backward, state=tk.DISABLED)
        self.btn_backward.pack(side=tk.LEFT)
        
        self.btn_forward = tk.Button(self.master, text=">>", command=self.forward, state=tk.DISABLED)
        self.btn_forward.pack(side=tk.LEFT)
    
    def update_frame(self):
        if self.playing:
            ret, frame = self.cap.read()
            
            if ret:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = PIL.Image.fromarray(cv2image)
                imgtk = PIL.ImageTk.PhotoImage(image=img)
                # img = tk.PhotoImage(data=cv2image.tobytes())
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
        
        self.master.after(1000 // self.fps, self.update_frame)
    
    def play(self):
        self.playing = True
    
    def pause(self):
        if self.playing:
            self.paused = not self.paused
            self.btn_play.config(text="Reanudar" if self.paused else "Pausar")
    
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
        self.cap = cv2.VideoCapture("C:/Users/Gerardo/Downloads/15_PACBOOK.mp4")
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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Reproductor de video")
    player = VideoPlayer(root)
    player.start()
    root.mainloop()