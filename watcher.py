import sys
import time

from PyQt5.QtCore import pyqtSignal, QObject, QThread
from watchdog.observers import Observer
from events import EventHandler

class Watcher:
    def __init__(self, src_path, signal = None):
        self.__src_path = src_path
        self.__event_handler = EventHandler.FileEventHandler(signal)
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )

class WatcherThread(QThread):
    refresh = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    # run method gets called when we start the thread
    def run(self):
        src_path = sys.argv[1] if len(sys.argv) > 1 else '.'
        Watcher(src_path, self.refresh).run()

if __name__ == "__main__":
    src_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    Watcher(src_path).run()
