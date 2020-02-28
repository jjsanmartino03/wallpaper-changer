import reddit_access
import requests
import os
import ctypes
import time
import sys



def put_wallpaper(filename):
    path = os.path.abspath(filename)
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

def main():
    right_now = time.localtime()
    date = f"{right_now[0]}-{right_now[1]}-{right_now[2]}"

    filename = os.path.normpath(f"Wallpapers/Wallpaper of {date}.jpg")

    if os.path.exists(filename):
        a = input("There is a wallpaper for today already, do you want to create another?(Y/N)")
        if a.lower()== "n":
            put_wallpaper(filename)
            sys.exit()
    
    image_url = ""
            
    while ".jpg" not in image_url:                                   
        image_url = reddit_access.get_image_url()

    if not os.path.isdir("Wallpapers"):
        os.mkdir("Wallpapers")
    with open(filename, "wb") as handle:
        response = requests.get(image_url, stream=True)

        if not response.ok:
            print(response)

        for pixel in response.iter_content(8192):
            if not pixel:
                break
            handle.write(pixel)

    put_wallpaper(filename)

if __name__ == "__main__":
    main()

