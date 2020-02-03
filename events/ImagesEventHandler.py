import os
from watchdog.events import RegexMatchingEventHandler

class ImagesEventHandler(RegexMatchingEventHandler):
    THUMBNAIL_SIZE = (128, 128)
    IMAGES_REGEX = [r".*.jpg$"]

    def __init__(self):
        super().__init__(self.IMAGES_REGEX)

    def on_any_event(self, event):
        self.process(event)

    def process(self, event):
        filename, ext = os.path.splitext(event.src_path)
        filename = f"{filename}_thumbnail.jpg"
        print(f"{event.src_path} + {event.event_type}")
