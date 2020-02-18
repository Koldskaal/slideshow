import os
from watchdog.events import RegexMatchingEventHandler

class FileEventHandler(RegexMatchingEventHandler):
    THUMBNAIL_SIZE = (128, 128)
    IMAGES_REGEX = [r".*.(gif|jpg|jpeg|tiff|png)$", r".*.(mp4|qtff|mov)$"]

    def __init__(self, signal):
        super().__init__(self.IMAGES_REGEX)

        self.signal = signal

    def on_any_event(self, event):
        self.process(event)

    def process(self, event):
        filename, ext = os.path.splitext(event.src_path)
        filename = f"{filename}_thumbnail.jpg"
        print(f"{event.src_path} + {event.event_type}")

        # Send QT signal to reload files!
        if self.signal:
            self.signal.emit()
