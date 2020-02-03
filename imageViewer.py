
import platform
import os
import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image, ImageTk

import videoPlayer2

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, master=None):
        QtWidgets.QMainWindow.__init__(self, master)

        self.setWindowTitle("Image viewer")

        self.palette = self.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))

        self.setPalette(self.palette)

        self.image_viewer = ImageViewer(self)

        self.setCentralWidget(self.image_viewer)

        self.ranbool = True

        self.videoframe = QtWidgets.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)

        #self.central_widget.setLayout(self.vboxlayout)

        self.showFullScreen()

        g_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('G'), self)

        g_shortcut.activated.connect(self.get_next)

    def get_next(self):
        if self.ranbool:
            self.ranbool = False
            self.setCentralWidget(ImageViewer(self))
        else:
            self.ranbool = True
            self.setCentralWidget(videoPlayer2.VideoPlayer(self))

class ImageViewer(QtWidgets.QWidget):
    """A simple Image displayer
    """

    def __init__(self, master=None):
        QtWidgets.QWidget.__init__(self, master)


        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('dog-landing-hero-lg.jpg')
        label.setPixmap(pixmap)
        label.setAlignment(QtCore.Qt.AlignCenter)


        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(label)

        self.setLayout(lay)

def main():
    """Entry point for our simple vlc player
    """
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
