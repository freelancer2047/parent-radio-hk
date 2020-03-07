#!/usr/bin/env python3

from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
import subprocess
import time


class FileEventHandler(FileSystemEventHandler):

    def __init__(self, event_handler):
        FileSystemEventHandler.__init__(self)
        self.event_handler = event_handler

    def on_moved(self, event):
        if event.dest_path.endswith(".mp3"):
            self.event_handler(event.dest_path)

    def on_created(self, event):
        if event.src_path.endswith(".mp3"):
            self.event_handler(event.src_path)


class DirectoryWatcher:

    def __init__(self, event_handler):
        self.event_handler = event_handler
    
    def run(self):
        observer = PollingObserver()
        file_event_handler = FileEventHandler(self.event_handler)
        observer.schedule(file_event_handler,"/opt/parent-radio-hk/queue", False)
        observer.start()
        while True:
            time.sleep(1)
        observer.join()

    
def play_file(path):
    print("Playing file: %s" % path)
    subprocess.run(
            ["gst-launch-1.0", "filesrc", "location=%s" % path, "!", "decodebin", "!", "pulsesink", "server=/tmp/pulse-socket" ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':
    w = DirectoryWatcher(play_file)
    w.run()
