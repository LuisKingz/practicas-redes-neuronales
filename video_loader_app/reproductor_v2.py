import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel,QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a timer for the video playback
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Create the video capture object
        self.capture = cv2.VideoCapture()

        # Create the main window UI
        self.initUI()

    def initUI(self):
        # Set the window title
        self.setWindowTitle('Video Player')

        # Create a label for displaying the video frame
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 640, 480)

        # Create the menu bar and actions
        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')
        open_action = filemenu.addAction('Open')
        open_action.triggered.connect(self.load_file)

        # Create the control buttons
        start_button = QPushButton('Start', self)
        start_button.setGeometry(10, 500, 75, 25)
        start_button.clicked.connect(self.start_video)

        stop_button = QPushButton('Stop', self)
        stop_button.setGeometry(90, 500, 75, 25)
        stop_button.clicked.connect(self.stop_video)

        pause_button = QPushButton('Pause', self)
        pause_button.setGeometry(170, 500, 75, 25)
        pause_button.clicked.connect(self.pause_video)

        restart_button = QPushButton('Restart', self)
        restart_button.setGeometry(250, 500, 75, 25)
        restart_button.clicked.connect(self.restart_video)

        forward_button = QPushButton('Forward', self)
        forward_button.setGeometry(330, 500, 75, 25)
        forward_button.clicked.connect(self.forward_video)

        backward_button = QPushButton('Backward', self)
        backward_button.setGeometry(410, 500, 75, 25)
        backward_button.clicked.connect(self.backward_video)

        # Set the window size and show the window
        self.setGeometry(100, 100, 640, 540)
        self.show()

    def load_file(self):
        # Open a file dialog to select a video file
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video File', '.', 'Video Files (*.avi *.mp4)')

        if filename:
            # Load the video file into the capture object
            self.capture.open(filename)

            # Set the label size to match the video frame size
            frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.label.setGeometry(0, 0, frame_width, frame_height)

            # Set the timer interval to match the video frame rate
            fps = int(self.capture.get(cv2.CAP_PROP_FPS))
            self.timer.setInterval(int(1000 / fps))

    def start_video(self):
        # Start the timer to display the video frames
        self.timer.start()

    def stop_video(self):
        # Stop the timer and reset the capture object
        self.timer.stop()
        self.capture.release()

    def pause_video(self):
        # Stop the timer without releasing the capture object
        self.timer.stop()

    def restart_video(self):
        # Stop the timer and reset the capture object to the beginning
        self.timer.stop()
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.timer.start()

    def forward_video(self):
        # Skip 5 frames forward
        current_pos = self.capture.get(cv2.CAP_PROP_POS_FRAMES)
        total_frames = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        new_pos = min(current_pos + 5, total_frames)
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, new_pos)

    def backward_video(self):
        # Skip 5 frames backward
        current_pos = self.capture.get(cv2.CAP_PROP_POS_FRAMES)
        new_pos = max(current_pos - 5, 0)
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, new_pos)
    
    def update_frame(self):
        # Read the next frame from the video capture object
        ret, frame = self.capture.read()

        if ret:
            # Convert the frame to a QImage and display it on the label
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap(q_image)
            self.label.setPixmap(pixmap)
        else:
            # Stop the timer and reset the capture object when the video ends
            self.timer.stop()
            self.capture.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())