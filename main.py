import re
import platform
import os
import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from frames import videos, images
from watcher import WatcherThread

class MainWindow(QtWidgets.QMainWindow):
    finished = QtCore.pyqtSignal()

    def __init__(self, master=None):
        QtWidgets.QMainWindow.__init__(self, master)

        self.files = []
        self.index = 0

        self.src_path = sys.argv[1] if len(sys.argv) > 1 else '.'

        cursor = QtGui.QCursor(QtCore.Qt.BlankCursor)

        self.setCursor(cursor)
        self.setWindowTitle("Slideshow")

        self.palette = self.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))

        self.setPalette(self.palette)

        self.ranbool = True

        self.videoframe = QtWidgets.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)

        self.watcher_thread = WatcherThread()
        self.watcher_thread.refresh.connect(self.generate_list)

        self.watcher_thread.start()

        #self.central_widget.setLayout(self.vboxlayout)

        self.showFullScreen()

        g_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('G'), self)

        g_shortcut.activated.connect(self.get_next)

        self.finished.connect(self.get_next)

        self.generate_list()

    def get_next(self):

        if self.index >= len(self.files):
            self.index = 0

        path = self.files[self.index]

        if re.match(r".*.(gif|jpg|jpeg|tiff|png)$", path):
            self.setCentralWidget(images.ImageViewer(self, path=path))
        elif re.match(r".*.(mp4|qtff|mov)$", path):
            self.setCentralWidget(videos.VideoPlayer(self, path=path))

        self.index += 1


    def generate_list(self):
        self.files = [f for f in os.listdir(self.src_path) if re.match(r".*.(gif|jpg|jpeg|tiff|png|mp4|qtff|mov)$", f)]

        self.index = 0

        self.get_next()



def main():
    """Entry point for our simple vlc player
    """
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
