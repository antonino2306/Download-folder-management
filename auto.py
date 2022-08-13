from genericpath import exists
from itertools import count
from os import rename, scandir
from os.path import join, splitext
import sys
import time
import logging
from shutil import move
from tracemalloc import start
from typing import Counter
from unicodedata import name
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

download_dir = "/home/antonino/Scaricati"
image_dir = "/home/antonino/Scaricati/Immagini"
video_dir = "/home/antonino/Scaricati/Video"
audio_dir = "/home/antonino/Scaricati/Audio"
docs_dir = "/home/antonino/Scaricati/Docs"

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}-{str(counter)}{extension}"
        counter += 1

    return name


def move_file(file_, dest, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(file_, dest)


    
class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(download_dir) as source_dir:
            for element in source_dir:
                name = element.name
                destination_dir = download_dir

                if name.endswith(".jpg") or name.endswith(".jpeg") or name.endswith(".png"):
                    destination_dir = image_dir
                    move_file(element, destination_dir, name)

                elif name.endswith(".docx") or name.endswith(".pdf") or name.endswith(".xlsx"):
                    destination_dir = docs_dir
                    move_file(element, destination_dir, name)
                
                elif name.endswith(".mp3") or name.endswith(".waw"):
                    destination_dir = audio_dir
                    move_file(element, destination_dir, name)
                
                elif name.endswith(".mp4") or name.endswith(".avi") or name.endswith(".webm"):
                    destination_dir = video_dir
                    move_file(element, destination_dir, name)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    path = download_dir

    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()