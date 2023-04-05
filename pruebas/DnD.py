import tkinter as tk
from tkinter import filedialog
import os

class VideoPlayer(tk.Tk):
    def __init__(self):
        super().__init__()

        # Create the widgets
        self.video_frame = tk.Frame(self, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        # Create a label for the drag and drop functionality
        self.drop_label = tk.Label(self.video_frame, text="Drag and drop a video file here", font=("Arial", 12))
        self.drop_label.pack(expand=True)

        # Bind the drag and drop events to the label
        self.drop_label.bind("<Enter>", self.on_enter)
        self.drop_label.bind("<Leave>", self.on_leave)
        self.drop_label.bind("<Drop>", self.on_drop)

    def on_enter(self, event):
        self.drop_label.configure(bg="light gray")

    def on_leave(self, event):
        self.drop_label.configure(bg="white")

    def on_drop(self, event):
        # Get the path of the dropped file
        file_path = event.widget.tk.eval('lindex {%s}' % event.data)
    
        # Check if the file is a video file
        if file_path.endswith((".mp4", ".avi", ".mov")):
        
            # Clear the drop label
            self.drop_label.pack_forget()
    
            # Create the video player using OpenCV
            import cv2
            self.cap = cv2.VideoCapture(file_path)
            self.video_canvas = tk.Canvas(self.video_frame, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                                          height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.video_canvas.pack(fill=tk.BOTH, expand=True)
    
            # Play the video
            self.play_video()

    def play_video(self):
        import cv2
        ret, frame = self.cap.read()
        if ret:
            self.video_canvas.delete("all")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = tk.PhotoImage(master=self.video_canvas, data=frame.tobytes())
            self.video_canvas.create_image(0, 0, image=image, anchor="nw")
            self.video_canvas.image = image
            self.after(int(1000 / self.cap.get(cv2.CAP_PROP_FPS)), self.play_video)
        else:
            self.cap.release()
            self.video_canvas.delete("all")
            self.video_canvas.configure(bg="black")
            self.drop_label.pack(expand=True)

if __name__ == "__main__":
    app = VideoPlayer()
    app.mainloop()