import requests
import os
import sys
import ctypes
from time import localtime as get_localtime
from shutil import copy2 as copy_file_to_destination, move as move_file
from random import choice as random_choice

from reddit import get_image_url


def save_image_to_file_from_url(url, filename):

    with open(filename, "wb") as handle:
        response = requests.get(url, stream=True)

        if not response.ok: # Something went wrong, abort
            print(response)

        for pixel in response.iter_content(8192): #iterate through the image
            if not pixel: # End of the image, break
                break
            handle.write(pixel)



def get_image_from_no_wifi_wallpapers(filename):

    if not os.path.isdir(r"wallpapers\no-wifi") or len(os.listdir(r"wallpapers\no-wifi")) == 0:
        return copy_image_from_previous_wallpapers(filename)

    else:                                                
        image = random_choice(os.listdir(r"wallpapers\no-wifi"))

        move_file(os.path.abspath(f"wallpapers/No-wifi/{image}"),os.path.abspath(filename))



def copy_image_from_previous_wallpapers(filename):
    previous_wallpapers = os.listdir(r"wallpapers")

    if len(previous_wallpapers) == 0:  # The directory is empty, abort
           return False

    else:
        image = random_choice(previous_wallpapers)

        copy_file_to_destination(os.path.abspath(f"wallpapers/{image}"), os.path.abspath(filename))



def is_no_wifi_directory_complete():
    if not os.path.isdir(os.path.normpath("wallpapers/no-wifi")):
        os.mkdir(os.path.normpath("wallpapers/no-wifi"))
    
    no_wifi_wallpapers = os.listdir(os.path.normpath("wallpapers/no-wifi"))

    dir_length = len(no_wifi_wallpapers)

    if dir_length < 15:
        numbers = [int(image.split(".")[0]) for image in no_wifi_wallpapers]

        for i in range(1, 16):

            if not i in numbers:
                image_number = i

                main(filename=os.path.normpath(f"wallpapers/no-wifi/{image_number}.jpg"),
                        completing_no_wifi=True)

def put_wallpaper(filename):
    path = os.path.abspath(filename)

    if sys.platform.startswith("win"):
        SPI_SETDESKWALLPAPER = 20

        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

    elif sys.platform.startswith("linux"):
        os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri " + path.replace(' ', '\\ '))
        

def main(filename=False, completing_no_wifi=False):
    if not filename: #if a filename was not provided, do

        localtime_date_object = get_localtime()
        date = f"{localtime_date_object[0]}-{localtime_date_object[1]}-{localtime_date_object[2]}"

        filename = os.path.normpath(f"wallpapers/Wallpaper of {date}.jpg")    

        if os.path.exists(filename): # If the file already exists
            a = input("There is a wallpaper for today already, do you want to create another?(y/n)")

            if a.lower()== "n":
                put_wallpaper(filename) # Be sure the last wallpaper is put again. (in windows, the wallpaper is taken out on shutdown)
                is_no_wifi_directory_complete() # check whether the no-wifi directory is complete

                sys.exit()

        if not os.path.isdir("wallpapers"): # If the directory isn't there, create it
            os.mkdir("wallpapers")

    image_url = get_image_url() # Get the image url from reddit

    if image_url: # If the request was successful
        save_image_to_file_from_url(image_url, filename)

        if not completing_no_wifi: # If the purpose wasn't to complete the no-wifi directory, then use the image as a wallpaper
            put_wallpaper(filename)
            is_no_wifi_directory_complete()

    elif not completing_no_wifi:
        if get_image_from_no_wifi_wallpapers(filename) != False:
            put_wallpaper(filename)
        else:
            sys.exit()
    else:
        sys.exit()
        

if __name__ == "__main__":
    main()