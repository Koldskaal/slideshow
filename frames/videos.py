import platform
import os
import sys

from PyQt5 import QtWidgets, QtGui, QtCore
import vlc

class VideoPlayer(QtWidgets.QWidget):

    def __init__(self, master=None, path=None):
        QtWidgets.QWidget.__init__(self, master)

        self.master = master

        # Create a basic vlc instance
        self.instance = vlc.Instance()

        self.media = None

        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        self.mediaplayer.audio_set_mute(1)

        self.create_ui()
        self.is_paused = False

        self.showFullScreen()

        self._play(path)

    def create_ui(self):
        """Set up the user interface, signals & slots
        """

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

        self.setLayout(self.vboxlayout)

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
        """Stop player and tell master it is done
        """
        self.mediaplayer.stop()
        self.master.finished.emit()

    def _play(self, path):
        self.media = self.instance.media_new(path)

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

        self.mediaplayer.play()
        self.timer.start()
        self.is_paused = False

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
    player = VideoPlayer()
    player.show()
    player.resize(640, 480)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
