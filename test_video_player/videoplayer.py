import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel,QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # Creamos una instancia de QMediaPlayer y QVideoWidget
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        # Creamos los botones para reproducir y seleccionar un archivo de video
        openButton = QPushButton('Open')
        openButton.clicked.connect(self.openFile)
        playButton = QPushButton('Play')
        playButton.clicked.connect(self.play)

        # Creamos una etiqueta para mostrar el nombre del archivo de video seleccionado
        self.fileNameLabel = QLabel('No file selected')

        # Creamos una caja vertical para organizar nuestros widgets
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(openButton)
        vboxLayout.addWidget(self.fileNameLabel)
        vboxLayout.addWidget(playButton)
        vboxLayout.addWidget(videoWidget)

        # Establecemos el diseño de nuestra ventana principal y lo mostramos
        self.setLayout(vboxLayout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.show()

    def openFile(self):
        # Utilizamos QFileDialog para seleccionar un archivo de video
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Video")

        if fileName != '':
            # Configuramos el archivo de video en QMediaPlayer
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.fileNameLabel.setText(fileName)

    def play(self):
        # Reproducimos el video
        self.mediaPlayer.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    sys.exit(app.exec_())