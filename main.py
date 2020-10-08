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
    saver           An instance of an object with a behavior that handles the saving and copying of the wallpaper 

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

        image_url = get_image_url() # Get the image url from praw

        if image_url:
            self.saver.save_from_url(image_url, self.path)
            self.use_wallpaper(self.path)
            self.complete_no_wifi()
        else:
            self.offline_wallpaper()
            self.use_wallpaper(self.path)

    def use_wallpaper(self, path):
        """
        Th
        """
        if sys.platform.startswith("win"):
            SPI_SETDESKWALLPAPER = 20

            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

        elif sys.platform.startswith("linux"):
            os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri " + path.replace(' ', '\\ '))

    def offline_wallpaper(self):
        if not os.path.isdir(self.no_wifi_folder):
            os.mkdir(self.no_wifi_folder)
        
        destination = self.path
        no_wifi_wallpapers = os.listdir(self.no_wifi_folder)

        if no_wifi_wallpapers:
            image_path = os.path.join(self.no_wifi_folder,random_choice(no_wifi_wallpapers))
            self.saver.move_from_location(image_path, destination)
        else:
            used_wallpapers = os.listdir(self.folder)
            if used_wallpapers:
                image_path = os.path.join(self.folder,random_choice(used_wallpapers))
                self.saver.copy_from_location(image_path, destination)

    def generate_filename(self):
        localtime = get_localtime()

        filename = "wallpaper-at-" +"-".join(list(map(str, list(localtime)))) + ".jpg"

        return filename

    def complete_no_wifi(self):
        if not os.path.isdir(self.no_wifi_folder):
            os.mkdir(self.no_wifi_folder)

        no_wifi_wallpapers = os.listdir(self.no_wifi_folder)
        no_wifi_dir_length = len(no_wifi_wallpapers)

        if no_wifi_dir_length < 15:
            numbers = [int(image.split(".")[0]) for image in no_wifi_wallpapers]

            for i in range(1, 16):

                if not i in numbers:
                    image_url = get_image_url()

                    if not image_url:
                        return

                    path = os.path.join(self.no_wifi_folder,f"{i}.jpg")

                    self.saver.save_from_url(image_url, path)        

if __name__ == "__main__":
    print(help(WallpaperChanger))
    changer = WallpaperChanger()
    changer.execute()