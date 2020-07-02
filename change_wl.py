import reddit_access
import requests
import os
import ctypes
import time
import sys
import shutil
import random

def get_image_from_url(url, filename):
    with open(filename, "wb") as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
                print(response)

        for pixel in response.iter_content(8192):
            if not pixel:
                break
            handle.write(pixel)

def get_image_from_used_wallpapers(filename):
    if len(os.listdir(r"Wallpapers"))==0:
           return False
    else:
        image = random.choice(os.listdir(r"Wallpapers"))
        shutil.copy2(os.path.abspath(f"Wallpapers/{image}"),os.path.abspath(filename))

def get_image_from_no_wifi_wallpapers(filename):
    if not os.path.isdir(r"Wallpapers\No_wifi") or len(os.listdir(r"Wallpapers\No_wifi"))==0:
        return get_image_from_used_wallpapers(filename)
    else:                                                
        image = random.choice(os.listdir(r"Wallpapers\No_wifi"))
        shutil.move(os.path.abspath(f"Wallpapers/No_wifi/{image}"),os.path.abspath(filename))
    

def is_no_wifi_directory_complete():
    if not os.path.isdir(r"Wallpapers\No_wifi"):
        os.mkdir(r"Wallpapers\No_wifi")
    no_wifi_dir = os.listdir(r"Wallpapers\No_wifi")
    dir_length = len(no_wifi_dir)
    if dir_length < 15:
        numbers = [int(image.split(".")[0]) for image in no_wifi_dir]
        for i in range(1, len(numbers)+2):
            if not i in numbers:
                image_number = i
                main(filename=os.path.normpath(f"Wallpapers/No_wifi/{image_number}.jpg"),
                        completing_no_wifi=True)
            
    


def put_wallpaper(filename):
    path = os.path.abspath(filename)
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

def main(filename=False, completing_no_wifi=False):
    if not filename:
        right_now = time.localtime()
        date = f"{right_now[0]}-{right_now[1]}-{right_now[2]}"

        filename = os.path.normpath(f"Wallpapers/Wallpaper of {date}.jpg")
    

        if os.path.exists(filename):
            a = input("There is a wallpaper for today already, do you want to create another?(y/n)")
            if a.lower()== "n":
                put_wallpaper(filename)
                is_no_wifi_directory_complete()
                sys.exit()

        if not os.path.isdir("Wallpapers"):
            os.mkdir("Wallpapers")

    image_url = reddit_access.get_image_url()
    print(image_url)
    
    if image_url :
        get_image_from_url(image_url, filename)
        if not completing_no_wifi:
            put_wallpaper(filename)
    elif not completing_no_wifi:
        if get_image_from_no_wifi_wallpapers(filename)!= False:
            put_wallpaper(filename)
        else:
            sys.exit()
    else:
        sys.exit()
    

    if image_url:
        is_no_wifi_directory_complete()

if __name__ == "__main__":
    main()

