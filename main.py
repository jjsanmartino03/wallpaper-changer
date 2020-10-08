import requests
import os
import sys
import ctypes
from time import localtime as get_localtime
from shutil import copy2 as copy_file_to_destination, move as move_file
from random import choice as random_choice

from reddit import get_image_url

class WallpaperSaver:
    def save_from_url(self, url, path):
        with open(path, "wb") as handle:
            response = requests.get(url, stream=True)

            if not response.ok: # Something went wrong, abort
                return

            for pixel in response.iter_content(8192): #iterate through the image
                if not pixel: # End of the image, break loop
                    break
                handle.write(pixel)

            return True

    def copy_from_location(self, copied, destination):
        copy_file_to_destination(copied, destination)

    def move_from_location(self, moved, destination):
        move_file(moved, destination)

class WallpaperChanger:
    """
    The class that handles the entire program. This object has the 
    purpose of changing the wallpaper of the pc.

    params

    filename        The name the wallpaper will have once downloaded
    default_folder  The folder which the wallpaper will be saved in 
                    (this has to be an absolute path to the folder,
                    since the whole program is based on that)
    saver           An instance of an object with a behavior that 
                    handles the saving and copying of the wallpaper 
    """
    def __init__(self, filename=None, default_folder=os.path.abspath("wallpapers"), saver=WallpaperSaver()):
        if not filename:
            filename = self.generate_filename() # generate a proper filename based on the date

        self.folder = default_folder # The wallpapers folder
        self.path = os.path.join(self.folder, filename) # The final path to the image
        self.no_wifi_folder = os.path.join(default_folder, "no-wifi") # The folder where wallpapers are saved to have images in case of not having a connection

        self.saver = saver

    def execute(self):
        """
        The main execution of the program. Doesn't need any params
        """
        if not os.path.isdir(self.folder): # If the directory isn't there, create it
            os.mkdir(self.folder)
        
        if not os.path.isdir(self.no_wifi_folder): # Same as before
            os.mkdir(self.no_wifi_folder)

        image_url = get_image_url() # Get the image url from praw

        if image_url: # If the url request was successful, continue
            self.saver.save_from_url(image_url, self.path)

            self.complete_no_wifi() # If not completed, complete the no-wifi directory
        else: # If it wasn't, use an already downloaded wallpaper
            self.offline_wallpaper() # Choose wallpaper
            
        self.use_wallpaper(self.path)

    def use_wallpaper(self, path):
        """
        The method that actually sets the image as a wallpaper. Works 
        for Windows and Gnome linux until now.

        path    the absolute path to the image
        """
        if sys.platform.startswith("win"): # If running on windows
            SPI_SETDESKWALLPAPER = 20

            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

        elif sys.platform.startswith("linux"): # If running on linux
            os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri " + path.replace(' ', '\\ '))

    def offline_wallpaper(self):
        """
        This method chooses and saves a wallpaper from the no-wifi
        folder, or if it doesn't have any files, from the wallpapers folder
        """
        no_wifi_wallpapers = os.listdir(self.no_wifi_folder)

        if no_wifi_wallpapers: # If there's any
            image_path = os.path.join(self.no_wifi_folder,random_choice(no_wifi_wallpapers))

            self.saver.move_from_location(image_path, self.path)
        else:
            used_wallpapers = os.listdir(self.folder)
            if used_wallpapers:
                image_path = os.path.join(self.folder,random_choice(used_wallpapers))
                self.saver.copy_from_location(image_path, self.path)

    def generate_filename(self):
        """
        Generate a filename based on the localtime
        """
        localtime = get_localtime() # Get the time

        string_date = "-".join(list(map(str, list(localtime)))) # Format the date so it has "-" between numbers

        filename = "wallpaper-at-" + string_date + ".jpg"

        return filename

    def complete_no_wifi(self):
        """
        If the no-wifi folder is not completed (doesn't have 15 files)
        complete it with new wallpaper
        """

        no_wifi_wallpapers = os.listdir(self.no_wifi_folder)

        if len(no_wifi_wallpapers) < 15: # If not completed
            numbers = [int(image.split(".")[0]) for image in no_wifi_wallpapers] # Already existing image numbers

            for i in range(1, 16):

                if not i in numbers: # If there isn't an image with that number
                    image_url = get_image_url() # Get url from praw

                    if not image_url: # Finish the execution
                        return

                    path = os.path.join(self.no_wifi_folder,f"{i}.jpg")

                    self.saver.save_from_url(image_url, path)        

if __name__ == "__main__":
    print(help(WallpaperChanger.complete_no_wifi))
    changer = WallpaperChanger()
    changer.execute()