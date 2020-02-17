from PyQt5 import QtWidgets, QtGui, QtCore

class ImageViewer(QtWidgets.QWidget):
    """A simple Image displayer
    """

    def __init__(self, master=None, duration=10, path=None):
        QtWidgets.QWidget.__init__(self, master)

        self.master = master

        label = QtWidgets.QLabel(self)

        if (path):
            pixmap = QtGui.QPixmap(path)
            label.setPixmap(pixmap)

        label.setAlignment(QtCore.Qt.AlignCenter)


        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(label)

        self.setLayout(lay)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000 * duration)

        self.timer.timeout.connect(self.stop)

        self.timer.start()

    def stop(self):
        self.master.finished.emit()
