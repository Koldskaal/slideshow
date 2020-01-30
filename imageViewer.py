
import platform
import os
import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image, ImageTk

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, master=None):
        QtWidgets.QMainWindow.__init__(self, master)

        self.setWindowTitle("Image viewer")

        self.palette = self.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))

        self.setPalette(self.palette)

        self.central_widget = ImageViewer()
        self.setCentralWidget(self.central_widget)

        self.videoframe = QtWidgets.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)

        #self.central_widget.setLayout(self.vboxlayout)

        self.showFullScreen()

class ImageViewer(QtWidgets.QWidget):
    """A simple Media Player using VLC and Qt
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


    def create_ui(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if platform.system() == "Darwin": # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()

        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)



        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)

        self.widget.setLayout(self.vboxlayout)

        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")

        # Add actions to file menu
        open_action = QtWidgets.QAction("Load Video", self)
        close_action = QtWidgets.QAction("Close App", self)
        playpause_action = QtWidgets.QAction("Play/Pause", self)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        file_menu.addAction(playpause_action)

        open_action.triggered.connect(self.open_file)
        close_action.triggered.connect(sys.exit)
        playpause_action.triggered.connect(self.play_pause)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)

    def play_pause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.is_paused = True
            self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.open_file()
                return

            self.mediaplayer.play()
            self.timer.start()
            self.is_paused = False

    def stop(self):
        """Stop player
        """
        self.mediaplayer.stop()

    def open_file(self):
        """Open a media file in a MediaPlayer
        """

        dialog_txt = "Choose Media File"
        filename = QtWidgets.QFileDialog.getOpenFileName(self, dialog_txt, os.path.expanduser('~'))
        if not filename:
            return

        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = self.instance.media_new(filename[0])

        # Put the media in the media player
        self.mediaplayer.set_media(self.media)

        # Parse the metadata of the file
        self.media.parse()

        # Set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this
        if platform.system() == "Linux": # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows": # for Windows
            self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

        self.play_pause()

    def set_volume(self, volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(volume)

    def update_ui(self):
        """Updates the user interface"""

        # Set the slider's position to its corresponding media position
        # Note that the setValue function only takes values of type int,
        # so we must first convert the corresponding media position.
        media_pos = int(self.mediaplayer.get_position() * 1000)

        # No need to call this function if nothing is played
        if not self.mediaplayer.is_playing():
            self.timer.stop()

            # After the video finished, the play button stills shows "Pause",
            # which is not the desired behavior of a media player.
            # This fixes that "bug".
            if not self.is_paused:
                self.stop()

def main():
    """Entry point for our simple vlc player
    """
    app = QtWidgets.QApplication(sys.argv)
    imageViewer = MainWindow()
    imageViewer.show()
    imageViewer.resize(640, 480)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
