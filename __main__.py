from watchdog.observers import Observer # a bunch of imports
from config import folders_to_track
from handler import Handler
from time import sleep
import os, logging

logging.basicConfig(level=logging.DEBUG)

event_handler, observer = (Handler(), Observer()) # this part makes it so that when it sees a file change it will call this function
logging.info("Starting")
for path in folders_to_track:
    observer.schedule(event_handler, path, recursive=True)
observer.start()

try: 
    while True:
        sleep(15)
except KeyboardInterrupt:
    logging.info("Stopping")
    quit(observer.stop())
observer.join()