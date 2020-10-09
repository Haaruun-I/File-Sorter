from config import extensions_folders, folders_to_track
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import os, shutil, logging

class Handler(FileSystemEventHandler):
    def on_any_event(self, event): # here
        logging.info("Event Detected") 
        for src_folder in folders_to_track: # it loops through the folders it needs to track
            for filename in os.listdir(src_folder): # finds any files
                try:
                    if filename == "desktop.ini": continue # it will ignore files that it does not have perms to edit, thats this line
                    logging.debug("Found file " + filename)
                    folder_destination_path = self.calculate_destination(filename, src_folder) # so it will figure out where to put the file
                    new_name = self.calculate_new_name(filename, src_folder, folder_destination_path) # it will then figure out a name for it

                    self.move_file(src_folder, filename, folder_destination_path, new_name) # anyways, this moves and renames the file, duh
                except Exception as error:
                    logging.warn(str(error) +": " + filename) # its not done, just converting all the prints to logging statemnts, for better controll

    def calculate_destination(self, filename, src_folder):
        # Get Category Folder
        try:
            extension = str(os.path.splitext(src_folder + '/' + filename)[1]) # sorts by extention
            extensions_folders[extension]
        except Exception:
            extension = 'noname' # if it cant find the extention, it will default to 'noname'
        folder_destination_path = extensions_folders[extension]
        # it works :D
        # Get Creation Date (self explanitory)
        creationDate = datetime.fromtimestamp(os.path.getctime(src_folder + '/' + filename))
 
        year = creationDate.strftime("%Y")
        month = creationDate.strftime("%B")
        folder_destination_path += "/" + year + "/" + month # adds date to file path
        
        return folder_destination_path
    
    def calculate_new_name(self, filename, src_folder, folder_destination_path): # all it does is find any copies and then name it like new-file(number of copies)
        # Check For File Copies
        file_exists = os.path.isfile(folder_destination_path + "/" + filename)
        file_copies = 1
        new_name = filename
        while file_exists:
            file_copies += 1
            new_name = os.path.splitext(src_folder + '/' + filename)[0] + str(i) + os.path.splitext(src_folder + '/' + filename)[1]
            new_name = new_name.split("/")[4]
            file_exists = os.path.isfile(folder_destination_path + "/" + new_name)
        
        return new_name

    def move_file(self, src_folder, filename, folder_destination_path, new_name):
        # Create Destination Folder
        try: os.makedirs(folder_destination_path)
        except OSError: pass

        # Move & Rename File
        os.rename(src_folder + "/" + filename,  src_folder + "/" + new_name)
        shutil.move(src_folder + "/" + filename, folder_destination_path)
        logging.debug("Moving File to " + folder_destination_path)